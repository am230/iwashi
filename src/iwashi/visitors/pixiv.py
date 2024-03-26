import json
import re
from typing import Dict, List, Optional, TypeAlias, TypedDict

import bs4
from loguru import logger

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, SiteVisitor


class Pixiv(SiteVisitor):
    NAME = "Pixiv"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"pixiv\.net/users/(?P<id>\d+)", re.IGNORECASE
    )

    async def normalize(self, context: Context, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://pixiv.net/users/{match.group("id")}'

    async def visit(self, url, context: Context, id: str):
        res = await context.session.get(
            f"https://pixiv.net/users/{id}",
        )
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        meta_element = soup.select_one(
            'meta[name="preload-data"][id="meta-preload-data"]'
        )
        if meta_element is None:
            logger.warning(f"[Pixiv] meta-preload-data not found: {id}")
            return
        info: Root = json.loads(meta_element.attrs["content"])

        if len(info["user"].values()) > 1:
            logger.warning(f"[Pixiv] User is must be unique: {id}")
            return

        for user in info["user"].values():
            context.create_result(
                "Pixiv",
                url=url,
                name=user["name"],
                description=user["comment"],
                profile_picture=user["imageBig"],
            )
            if "webpage" in user and user["webpage"] is not None:
                context.enqueue_visit(user["webpage"])
            if user["social"]:
                for link in user["social"].values():
                    context.enqueue_visit(link["url"])

            resp = await context.session.get(
                f"https://sketch.pixiv.net/api/pixiv/user/posts/latest?user_id={id}"
            )
            if resp.status == 200:
                data = await resp.json()
                context.enqueue_visit(data["data"]["user"]["url"])


class Background(TypedDict):
    repeat: None
    color: None
    url: str
    isPrivate: bool


class Social(TypedDict):
    url: str


class Region(TypedDict):
    name: str
    region: str
    prefecture: str
    privacyLevel: str


class Age(TypedDict):
    name: Optional[str]
    privacyLevel: Optional[str]


class UserDetail(TypedDict):
    userId: str
    name: str
    image: str
    imageBig: str
    premium: bool
    isFollowed: bool
    isMypixiv: bool
    isBlocking: bool
    background: Background
    sketchLiveId: None
    partial: int
    acceptRequest: bool
    sketchLives: List
    following: int
    mypixivCount: int
    followedBack: bool
    comment: str
    commentHtml: str
    webpage: str
    social: Dict[str, Social]
    canSendMessage: bool
    region: Region
    age: Age
    birthDay: Age
    gender: Age
    job: Age
    workspace: None
    official: bool
    group: None


User: TypeAlias = Dict[str, UserDetail]


class Root(TypedDict):
    timestamp: str
    user: User
