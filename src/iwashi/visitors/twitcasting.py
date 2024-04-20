import re

import bs4
from loguru import logger

from iwashi.helper import HTTP_REGEX, normalize_url
from iwashi.visitor import Context, SiteVisitor


class TwitCasting(SiteVisitor):
    def __init__(self) -> None:
        super().__init__(
            name="TwitCasting",
            regex=re.compile(
                HTTP_REGEX + r"twitcasting\.tv/(?P<id>[-\w]+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://twitcasting.tv/{id}"
        res = await context.session.get(
            url,
        )
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        # name: .tw-user-nav-name
        element = soup.select_one(".tw-user-nav-name")
        if element is None:
            logger.warning(f"[TwitCasting] Could not find name for {url}")
            return
        name = element.text.strip()
        # icon: .tw-user-nav-icon > img
        element = soup.select_one(".tw-user-nav-icon > img")
        profile_picture = None
        if element is not None:
            attr = element["src"]
            if isinstance(attr, str):
                profile_picture = normalize_url(attr)

        context.create_result(
            "TwitCasting",
            url=url,
            name=name,
            description=None,
            profile_picture=profile_picture,
        )

        links = set()  # TODO
        for element in soup.select(".tw-follow-list-row-icon"):
            links.add(element["href"])
        for link in links:
            if link.startswith("/"):
                continue
            context.enqueue_visit(link)
