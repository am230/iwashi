from __future__ import annotations

import json
import re
from typing import TypedDict

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, SiteVisitor


class Note(SiteVisitor):
    def __init__(self):
        super().__init__(
            name="Note",
            regex=re.compile(HTTP_REGEX + r"note\.com/(?P<user>[^/]+)", re.IGNORECASE),
        )

    async def resolve_id(self, context: Context, url: str) -> str:
        match = self.regex.match(url)
        if match is None:
            return url
        return f"https://note.com/{match.group('user')}"

    async def visit(self, context: Context, id: str):
        url = f"https://note.com/{id}"
        res = await context.session.get(
            url,
        )
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")

        data_element = soup.select_one("script[type='application/ld+json']")
        if data_element is None:
            return
        data: Root = json.loads(data_element.text)

        context.create_result(
            "Note",
            url=url,
            name=data["headline"],
            description=data["description"],
            profile_picture=data["image"]["url"],
        )

        links: set[str] = set()
        for element in soup.select(".m-creatorSocialLinks__item"):
            link = element.select_one("a")
            if link is None:
                continue
            if "href" not in link.attrs:
                continue
            links.add(link.attrs["href"])
        for link in links:
            context.enqueue_visit(link)


Author = TypedDict("Author", {"@type": "str", "name": "str", "url": "str"})  # TODO
Logo = TypedDict(
    "Logo", {"@type": "str", "url": "str", "width": "str", "height": "str"}
)
Publisher = TypedDict("Publisher", {"@type": "str", "name": "str", "logo": "Logo"})
Image = TypedDict(
    "Image", {"@type": "str", "url": "str", "width": "int", "height": "int"}
)
Root = TypedDict(
    "Root",
    {
        "@context": "str",
        "@type": "str",
        "mainEntityOfPage": "str",
        "headline": "str",
        "datePublished": "str",
        "dateModified": "str",
        "author": "Author",
        "publisher": "Publisher",
        "image": "Image",
        "description": "str",
    },
)
