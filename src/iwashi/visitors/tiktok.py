from __future__ import annotations

import json
import re
from typing import List, TypedDict

import bs4
from loguru import logger

from iwashi.helper import HTTP_REGEX, normalize_url
from iwashi.visitor import Context, SiteVisitor


class TikTok(SiteVisitor):
    def __init__(self) -> None:
        super().__init__(
            name="TikTok",
            regex=re.compile(
                HTTP_REGEX + r"tiktok\.com/@(?P<id>[-\w]+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str) -> None:
        url = f"https://tiktok.com/@{id}"
        res = await context.session.get(
            url,
        )
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        # icon: <meta property="og:image"
        element = soup.select_one('meta[property="og:image"]')
        profile_picture = None
        if element is not None:
            attr = element["content"]
            if isinstance(attr, str):
                profile_picture = normalize_url(attr)

        # data: #Person
        element = soup.select_one("script#Person")
        if element is None:
            logger.warning(f"[TikTok] Could not find data for {url}")
            return
        data: Root = json.loads(element.text)

        context.create_result(
            "TikTok",
            url=url,
            name=data["name"],
            description=data["description"],
            profile_picture=profile_picture,
        )


InteractionType = TypedDict("InteractionType", {"@type": "str"})
InteractionStatisticItem = TypedDict(
    "InteractionStatisticItem",
    {
        "@type": "str",
        "interactionType": "InteractionType",
        "userInteractionCount": "int",
    },
)
Mainentityofpage = TypedDict("Mainentityofpage", {"@id": "str", "@type": "str"})
Root = TypedDict(
    "Root",
    {
        "@context": "str",
        "@type": "str",
        "name": "str",
        "description": "str",
        "alternateName": "str",
        "url": "str",
        "knowsLanguage": "str",
        "nationality": "str",
        "interactionStatistic": "List[InteractionStatisticItem]",
        "mainEntityOfPage": "Mainentityofpage",
    },
)
