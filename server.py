"""Run the server for hachanges."""
from aiohttp import web
import json
import requests
import os
from github import Github
import static
import extra_info

CACHE = {}

def get_changes(number: str):
    comp_base = "https://www.home-assistant.io/components/"
    pull_base = "https://github.com/home-assistant/core/pull/"
    github = Github(os.environ["GHTOKEN"])
    repo = github.get_repo("home-assistant/home-assistant.io")
    posts = repo.get_contents("source/_posts", "current")
    this_post = None
    for post in posts:
        if "release" in post.path:
            name = post.path.split("/")[-1].split(".")[0]
            name = name.split("-")
            rel_number = name[-1]
            if rel_number == number:
                this_post = post.html_url
    if this_post is None:
        print("Release for", number, "not found")
        return
    url = this_post
    url_data = requests.get(url).text.split("\n")
    raw_changes = []
    changes = {}
    changes["version"] = "0.{}.x".format(url.split(".markdown")[0].split("-")[-1])
    changes["data"] = []
    control = []
    for line in url_data:
        if "(breaking change)" in line:
            raw_changes.append(line)
    for change in raw_changes:
        if change[0:3] == "<p>":
            pass
        else:
            this = {}
            try:
                pull = str(change)
                if "home-assistant/home-assistant/pull/" in pull:
                    pull = pull.split("home-assistant/home-assistant/pull/")[1]
                else:
                    pull = pull.split("home-assistant/core/pull/")[1]
                pull = pull.split('"')[0]
            except:
                pull = None
            if pull not in control and pull is not None:
                prlink = "{}{}".format(pull_base, pull)
                try:
                    component = str(change)
                    splitbase = '<a href="/home-assistant/home-assistant.io/blob/'
                    if f"{splitbase}current/integrations/" in component:
                        component = component.split(f"{splitbase}current/integrations/")[1]
                    else:
                        component = component.split(f"{splitbase}current/components/")[1]
                    component = component.split('">')[0]
                except:
                    component = None
                doclink = "{}{}".format(comp_base, component)
                if len(change.split("<li>")) == 1:
                    desc = change.split("<li>")[0]
                else:
                    desc = change.split("<li>")[1]
                desc = desc.split("(<a ")[0]
                desc = desc.replace("</code>", "")
                desc = desc.replace('<code class="highlighter-rouge">', "")
                desc = desc.replace("\u2019", "`")
                desc = desc.replace("\u201c", "")
                desc = desc.replace("\u201d", "")
                this["pull_request"] = pull
                this["prlink"] = prlink
                this["component"] = component
                this["doclink"] = doclink
                this["description"] = desc
                changes["data"].append(this)
                control.append(pull)
    return changes['data']


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

    content += static.HEADER.format(version=version)

    content += '<main>'

    if version in extra_info.EXTRA:
        for item in extra_info.EXTRA[version]:
            title = item['title']
            body = item['content']
            more_info = item['more_info']
            more_info_type = item['more_info_type']
            if more_info is not None:
                link = more_info
                if more_info_type != 'int':
                    target = 'target="_blank"'
                else:
                    target = ''
                links = static.EXTRA_LINK.format(link=link, target=target)
            else:
                links = ''

            content += static.EXTRA.format(title=title, content=body,
                                           links=links)

    changes = await get_data(version)

    if not changes:
        content += static.NO_CHANGES.format(version=version)
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
            doclink = change.get('doclink')

        content += static.CARD.format(pull=pull, title=comp,
                                      content=change.get('description'),
                                      docs=doclink,
                                      prlink=change.get('prlink'))
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
            data = get_changes(version)
        except Exception as err:
            print(err)
            data = None
        if data:
            print("Adding data for", version, "to cache")
            CACHE[version] = data

    print("Request sucessful:", bool(data))

    if isinstance(data, list):
        value = data
    else:
        value = None

    return value

if __name__ == "__main__":
    APP = web.Application()
    APP.router.add_route('GET', r'/', defaultsite, name='defaultsite')
    APP.router.add_route('GET', r'/{version}', html, name='html')
    APP.router.add_route('GET', r'/{version}/json', json, name='json')
    web.run_app(APP, port=9999)
