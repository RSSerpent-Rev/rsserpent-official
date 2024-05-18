from typing import Any, Dict

import arrow
from rsserpent.utils import HTTPClient, cached


path = "/applovin/sdk-update/{platform}"


@cached
async def provider(platform: str) -> Dict[str, Any]:
    map_dict = {
        "ios": "iOS",
        "android": "Android",
        "unity": "Unity",
        "react-native": "React Native",
        "flutter": "Flutter",
        "godot": "Godot",
    }
    if platform.lower() not in map_dict:
        raise ValueError(f"Unsupported platform: {platform}")

    async with HTTPClient() as client:
        platform_in_url = platform.replace("-", "_")
        url = f"https://docs.applovin.com/max/api/1.0/changelog/{platform_in_url}"
        user_info = (await client.get(url)).json()

    # {
    #     "published_at": "May 16, 2024",
    #     "version": "12.5.0",
    #     "content": "<ul>\n<li>Various fixes to the <a href=\"https://developers.applovin.com/en/ios/overview/new-sdk-initialization-api\">new init APIs</a>.</li>\n<li>Fix <code>+[ALLogger isVerboseForSdk:]</code> crash.</li>\n</ul>\n"
    # },

    return {
        "title": f"AppLovin {map_dict[platform.lower()]} SDK 更新日志",
        "link": url,
        "description": f"最新更新日期：{arrow.get(user_info[0]['published_at'], 'MMMM D, YYYY').format('YYYY-MM-DD')}",
        "items": [
            {
                "title": f"AppLovin {map_dict[platform.lower()]} SDK {item['version']} 更新",
                "description": item["content"],
                "link": url,
                "pub_date": arrow.get(item["published_at"], "MMMM D, YYYY"),
            }
            for item in user_info
        ],
    }
