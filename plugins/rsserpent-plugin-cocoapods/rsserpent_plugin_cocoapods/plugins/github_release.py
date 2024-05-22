from typing import Any, Dict
from rsserpent.utils import HTTPClient
from lxml import html
import arrow
import feedparser

async def get_changelog(pod: str):

    url = f"https://cocoapods.org/pods/{pod}"
    async with HTTPClient() as client:
        pod_resp = await client.get(url)
        if pod_resp.status_code == 200:
            html_text = pod_resp.content.decode("utf-8")
            tree = html.fromstring(html_text)
            home_link = tree.xpath("//ul[@class='links']")[0].xpath(".//li")[1].xpath(".//a")[0].attrib["href"]
            # is github repo link
            if home_link.startswith("https://github.com"):
                feed = feedparser.parse(home_link + "/releases.atom")
                if len(feed.entries) == 0:
                    return None

                return {
                    "title": f"{pod} Changelog",
                    "link": feed.feed.link,
                    "description": feed.feed.title,
                    "items": list(map(lambda x: {
                        "title": x.title,
                        "description": x.content[0].value,
                        "link": x.link,
                        "pub_date": arrow.get(x.updated),
                    }, feed.entries))
                }

    return None

