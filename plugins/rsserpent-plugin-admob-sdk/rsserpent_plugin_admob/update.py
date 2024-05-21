from typing import Any, Dict

import arrow
from rsserpent.utils import HTTPClient, cached
from lxml import html


path = "/admob/sdk-update/{platform}"


def get_date(date_str: str) -> arrow.Arrow:
    formats = ["YYYY-MM-DD", "YYYY-M-DD", "MMMM D, YYYY", "YYYY‑MM‑DD"]
    print('date_str:', date_str)
    for fmt in formats:
        try:
            date = arrow.get(date_str.strip(), fmt)
            print('date:', date)
            break
        except Exception as e:
            print(e)
            date = arrow.now()

    print("final date:", date)
    return date

@cached
async def provider(platform: str) -> Dict[str, Any]:
    map_dict = {
        "ios": "iOS",
        "android": "Android",
        "cpp": "C++",
    }
    if platform.lower() not in map_dict:
        raise ValueError(f"Unsupported platform: {platform}")

    async with HTTPClient() as client:
        platform_in_url = platform.replace("-", "_")
        url = f"https://developers.google.com/admob/{platform_in_url}/rel-notes"
        html_text = (await client.get(url)).content.decode("utf-8")
        tree  = html.fromstring(html_text)
        table = tree.xpath("//table")[0]

        items = []
        for row in table.xpath(".//tr"):
            if not row.xpath(".//td"):
                continue
            version = row.xpath(".//td")[0].text_content()
            date_str = row.xpath(".//td")[1].text_content().strip()
            note = row.xpath(".//td")[2].text_content()
            items.append({
                "title": f"AdMob SDK {map_dict[platform]} {version} Update",
                "description": note,
                "link": url,
                "pub_date": get_date(date_str),
            })

    print("items:", items)

    return {
        "title": f"AdMob SDK {map_dict[platform]} Update",
        "link": url,
        "description": "Latest AdMob SDK update.",
        "pub_date": items[0]["pub_date"],
        "items": items
    }


