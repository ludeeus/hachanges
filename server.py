"""Run the server for hachanges."""
from aiohttp import web
from furystoolbox.cli.hass import breaking_change
import static


async def defaultsite(request):
    """Serve this for root."""
    print(request)
    return web.Response(body=static.DEFAULT, content_type="text/html")

async def html(request):
    """Serve a HTML site."""
    version = request.match_info['version']
    if '.' in version:
        return web.Response(body=static.WRONG_VERSION,
                            content_type="text/html")

    changes = await get_data(version)

    if not changes:
        return web.Response(body=static.NO_CHANGES.format(version),
                            content_type="text/html")

    content = static.STYLE
    content += static.HEADER.format(request.match_info['version'])

    for change in changes:
        comp = change.get('component')

        if comp is None:
            comp = 'homeassistant'
        elif comp == 'None':
            comp = 'homeassistant'

        if comp == 'homeassistant':
            doclink = 'https://www.home-assistant.io/'
        else:
            doclink = change['doclink']

        content += "<b>{}</b></br>".format(comp)
        content += "<div><i>{}</i></br>".format(change['description'])

        content += static.LINKS.format(change['prlink'], doclink)
        content += "</div></br>"

    return web.Response(body=content, content_type="text/html")

async def json(request):
    """Serve the response as JSON."""
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

    data = breaking_change(version)

    print(data)

    if data:
        vaulue = data.get('data')
    else:
        vaulue = None

    return vaulue

if __name__ == "__main__":
    APP = web.Application()
    APP.router.add_route('GET', r'/', defaultsite, name='defaultsite')
    APP.router.add_route('GET', r'/{version}', html, name='html')
    APP.router.add_route('GET', r'/{version}/json', json, name='json')
    web.run_app(APP, port=9999)
