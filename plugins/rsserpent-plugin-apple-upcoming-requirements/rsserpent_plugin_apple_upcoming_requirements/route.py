from typing import Any, Dict
import lxml.html
from rsserpent.utils import HTTPClient, cached
import lxml
import arrow

path = "/apple-upcoming-requirements"


async def provider() -> Dict[str, Any]:
    async with HTTPClient() as client:
        resp = await client.get('https://developer.apple.com/news/upcoming-requirements/')
        html = lxml.html.fromstring(resp.content.decode())
        # section with class name that contains "article-list"
        article_list = html.xpath('//section[contains(@class, "article-list")]')[0]
        items = []
        for article in article_list.xpath('.//article'):
            # a tag with class is article-title
            title = article.xpath('.//a[contains(@class, "article-title")]')[0].text_content().strip()
            link = 'https://developer.apple.com' + article.xpath('.//a[contains(@class, "article-title")]')[0].attrib['href']
            # span tag with class is article-text
            description = article.xpath('.//span[contains(@class, "article-text")]')[0].text_content().strip()
            # p tag with class article-date
            article_date = ' '.join(article.xpath('.//p[contains(@class, "article-date")]')[0].text_content().split(" ")[1:])
            article_date = arrow.get(article_date, "MMMM D, YYYY")

            items.append({
                "title": title,
                "link": link,
                "description": description,
                "pub_date": article_date,
            })
    return {
        "title": "Apple developer news - Upcoming requirements",
        "link": "https://developer.apple.com/news/upcoming-requirements/",
        "description": "Apple developer news - Upcoming requirements",
        "items": items,
    }
