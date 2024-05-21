from typing import Any, Dict

import arrow
from rsserpent.utils import HTTPClient, cached
from lxml import html
import feedparser


path = "/cocoapods/{pod}"


# @cached
async def provider(pod: str) -> Dict[str, Any]:
    """Define a basic example data provider function."""
    url = f"https://cocoapods.org/pods/{pod}"
    async with HTTPClient() as client:
        pod_resp = await client.get(url)
        if pod_resp.status_code != 200:
            feed = feedparser.parse("https://github.com/CocoaPods/Specs/commits/master.atom")
            items = list(filter(lambda x: pod in x.title, feed.entries))
            return {
                "title": f"{pod} Changelog",
                "link": feed.feed.link,
                "description": feed.feed.title,
                "items": list(map(lambda x: {
                    "title": x.title,
                    "description": x.content[0].value,
                    "link": x.link,
                    "pub_date": arrow.get(x.updated),
                }, items))
            }

        else:
            html_text = pod_resp.content.decode("utf-8")
            tree = html.fromstring(html_text)
            # https://github.com/CocoaPods/Specs/blob/master/Specs/5/9/a/Google-Mobile-Ads-SDK/11.5.0/Google-Mobile-Ads-SDK.podspec.json
            spec_link = tree.xpath("//ul[@class='links']")[0].xpath(".//li")[0].xpath(".//a")[0].attrib["href"]
            # https://github.com/CocoaPods/Specs/commits/master/Specs/5/9/a/Google-Mobile-Ads-SDK.atom
            commit_atom = '/'.join(spec_link.split('/')[:12]) + '.atom'
            commit_atom = commit_atom.replace('blob/', 'commits/')
            feed = feedparser.parse(commit_atom)

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
