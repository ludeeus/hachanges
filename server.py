"""Run the server for hachanges."""
from aiohttp import web
from bs4 import BeautifulSoup
from github import Github
import extra_info
import json
import os
import re
import requests
import static

from const import CACHE, RELEASEPOST, MIN_VERSION, URL_PULL_BASE, URL_INTEGRATION_BASE

def init():
    CACHE["releaseposts"] = {}
    CACHE["changes"] = {}
    releaseposts()

def releaseposts():
    github = Github(os.environ["GHTOKEN"])
    repo = github.get_repo("home-assistant/home-assistant.io")
    posts = repo.get_contents("source/_posts", "current")
    releaseposts = [x for x in posts if re.match(RELEASEPOST, x.path)]
    for release in releaseposts:
        reg = re.match(RELEASEPOST, release.path)
        CACHE["releaseposts"][reg.group(1)] = release

def get_breaking_changes(releasenumber):
    if int(releasenumber) < MIN_VERSION:
        return []
    if str(releasenumber) not in CACHE["releaseposts"]:
        print(f"No post for {releasenumber} in cahce, trying to refresh")
        releaseposts()
        if str(releasenumber) not in CACHE["releaseposts"]:
            return []
    if str(releasenumber) in CACHE["changes"] and CACHE["changes"][str(releasenumber)]:
        return CACHE["changes"][str(releasenumber)]

    CACHE["changes"][str(releasenumber)] = []
    release = CACHE["releaseposts"][str(releasenumber)]
    bs = BeautifulSoup(requests.get(release.html_url).text, features="html.parser")
    breaking_changes = [x for x in bs.find_all("details") if x.summary.b and x.p]
    changes = []
    for soup in breaking_changes:
        change = {}

        change["title"] = soup.summary.b.get_text()
        change["integration"] = None
        change["pull"] = None

        content = soup.get_text().split("\n")
        for x in list(content):
            if x == "":
                content.remove(x)
            if "@" in x and "#" in x:
                if ") (" in x:
                    change["integration"] = x.split(") (")[1].replace(" docs)", "")
                if "- #" in x:
                    change["pull"] = x.split("- #")[1].split(")")[0]
                content.remove(x)


        change["description"] = "".join(
            [
                x
                for x in content
                if change["title"] not in x
                and x != ""
            ]
        )

        change["component"] = change["integration"]
        change["pull_request"] = change["pull"]

        if change["integration"]:
            change["doclink"] = URL_INTEGRATION_BASE + change["integration"]
        else:
            change["doclink"] = "https://www.home-assistant.io/"
        if change["pull"]:
            change["prlink"] = URL_PULL_BASE + change["pull"]
        else:
            change["prlink"] = URL_PULL_BASE


        CACHE["changes"][str(releasenumber)].append(change)
    return CACHE["changes"][str(releasenumber)]


async def defaultsite(request):
    """Serve root."""
    content = static.STYLE
    content += static.DEFAULT
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")


async def html(request):
    """Serve a HTML site."""
    content = static.STYLE
    version = request.match_info["version"]
    if "." in version:
        content += static.WRONG_VERSION.format(version=version)
        content += static.FOOTER
        return web.Response(body=content, content_type="text/html")

    content += static.HEADER.format(version=version)

    content += "<main>"

    if version in extra_info.EXTRA:
        for item in extra_info.EXTRA[version]:
            title = item["title"]
            body = item["content"]
            more_info = item["more_info"]
            more_info_type = item["more_info_type"]
            if more_info is not None:
                link = more_info
                if more_info_type != "int":
                    target = 'target="_blank"'
                else:
                    target = ""
                links = static.EXTRA_LINK.format(link=link, target=target)
            else:
                links = ""

            content += static.EXTRA.format(title=title, content=body, links=links)

    changes = get_breaking_changes(version)

    if not changes:
        content += static.NO_CHANGES.format(version=version)
        content += static.FOOTER
        return web.Response(body=content, content_type="text/html")

    for change in changes:
        comp = change.get("component")

        pull = change.get("pull_request")

        if comp is None:
            comp = "homeassistant"
        elif comp == "None":
            comp = "homeassistant"

        if comp == "homeassistant":
            doclink = "https://www.home-assistant.io/"
        else:
            doclink = change.get("doclink")

        content += static.CARD.format(
            pull=pull,
            title=comp,
            content=change.get("description"),
            docs=doclink,
            prlink=change.get("prlink"),
        )
    content += "</main>"
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")


async def json(request):
    """Serve the response as JSON."""
    version = request.match_info["version"]
    if "." in version:
        return web.json_response({"error": "Wrong version format."})

    json_data = get_breaking_changes(version)

    if not json_data:
        return web.json_response({"error": "No changes found."})

    return web.json_response(json_data)


if __name__ == "__main__":
    init()
    APP = web.Application()
    APP.router.add_route("GET", r"/", defaultsite, name="defaultsite")
    APP.router.add_route("GET", r"/{version}", html, name="html")
    APP.router.add_route("GET", r"/{version}/json", json, name="json")
    web.run_app(APP, port=9999)
