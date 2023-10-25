from __future__ import annotations

import json
import re
from typing import TypedDict

import bs4
import requests

from ..helper import BASE_HEADERS, HTTP_REGEX
from ..visitor import Context, SiteVisitor


class Note(SiteVisitor):
    NAME = "Note"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"note\.com/(?P<user>[^/]+)", re.IGNORECASE
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f"https://note.com/{match.group('user')}"

    def visit(self, url: str, context: Context, user: str):
        res = requests.get(url, headers=BASE_HEADERS)
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        data_element = soup.select_one("script[type='application/ld+json']")
        if data_element is None:
            return
        data: Root = json.loads(data_element.text)

        context.create_result(
            "Note",
            url=url,
            score=1.0,
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
            context.visit(link)


Author = TypedDict("author", {"@type": "str", "name": "str", "url": "str"})
Logo = TypedDict(
    "logo", {"@type": "str", "url": "str", "width": "str", "height": "str"}
)
Publisher = TypedDict("publisher", {"@type": "str", "name": "str", "logo": "Logo"})
Image = TypedDict(
    "image", {"@type": "str", "url": "str", "width": "int", "height": "int"}
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
