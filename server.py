"""Run the server for hachanges."""
from aiohttp import web
from furystoolbox.cli.hass import breaking_change
import static
import extra_info

CACHE = {}

async def defaultsite(request):
    """Serve root."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = static.STYLE
    content += static.DEFAULT
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")

async def html(request):
    """Serve a HTML site."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = static.STYLE
    version = request.match_info['version']
    if '.' in version:
        content += static.WRONG_VERSION.format(version=version)
        content += static.FOOTER
        return web.Response(body=content, content_type="text/html")

    previous = int(version) - 1
    next_version = int(version) + 1

    content += static.HEADER.format(version=version, previous=previous,
                                    next=next_version)

    content += '<main>'

    if version in extra_info.EXTRA:
        for item in extra_info.EXTRA[version]:
            title = item['title']
            body = item['content']
            content += static.EXTRA.format(title=title, content=body)

    changes = await get_data(version)

    if not changes:
        content += static.NO_CHANGES.format(version=version,
                                            previous=previous,
                                            next=next_version)
        content += static.FOOTER
        return web.Response(body=content, content_type="text/html")

    for change in changes:
        comp = change.get('component')

        pull = change.get('pull_request')

        if comp is None:
            comp = 'homeassistant'
        elif comp == 'None':
            comp = 'homeassistant'

        if comp == 'homeassistant':
            doclink = 'https://www.home-assistant.io/'
        else:
            doclink = change['doclink']

        content += static.CARD.format(pull=pull, title=comp,
                                      content=change['description'],
                                      docs=doclink,
                                      prlink=change['prlink'])
    content += '</main>'
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")

async def json(request):
    """Serve the response as JSON."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    version = request.match_info['version']
    if '.' in version:
        return web.json_response({'error': 'Wrong version format.'})

    json_data = await get_data(version)

    if not json_data:
        return web.json_response({'error': 'No changes found.'})

    return web.json_response(json_data)


async def get_data(version):
    """Get version data."""
    print("Requesting breaking change for version", version)

    if version in CACHE:
        print("Loading data for", version, "from cache")
        data = CACHE[version]
    else:
        try:
            data = breaking_change(version)
        except:
            data = None
        if data:
            print("Adding data for", version, "to cache")
            CACHE[version] = data

    print("Request sucessful:", bool(data))

    if data:
        value = data.get('data')
    else:
        value = None

    return value

if __name__ == "__main__":
    APP = web.Application()
    APP.router.add_route('GET', r'/', defaultsite, name='defaultsite')
    APP.router.add_route('GET', r'/{version}', html, name='html')
    APP.router.add_route('GET', r'/{version}/json', json, name='json')
    web.run_app(APP, port=9999)
