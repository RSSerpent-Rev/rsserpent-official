from typing import Any, Dict

import arrow
from rsserpent.utils import cached
import feedparser
from starlette.exceptions import HTTPException
import hashlib


path = "/cocoapods/{pod}"


@cached
async def provider(pod: str) -> Dict[str, Any]:
    """Define a basic example data provider function."""
    md5 = hashlib.md5(pod.encode()).hexdigest()
    commit_atom = f"https://github.com/CocoaPods/Specs/commits/master/Specs/{md5[0]}/{md5[1]}/{md5[2]}/{pod}.atom"
    feed = feedparser.parse(commit_atom)
    if not feed.entries:
        raise HTTPException(status_code=404, detail="Pod not found")

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
