from __future__ import annotations

import re
from typing import List, TypedDict

import requests

from ..helper import BASE_HEADERS, HTTP_REGEX
from ..visitor import Context, SiteVisitor


class Misskey(SiteVisitor):
    NAME = "Misskey"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"(?P<host>[^.]+\.[^\/]+)/channels/(?P<channek_id>[\w]+)",
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://{match.group("host")}/channels/{match.group("channel_id")}'

    def visit(self, url, context: Context, host: str, channel_id: str):
        url = f"https://{host}/api/channels/show"
        res = requests.post(url, json={"channelId": channel_id}, headers=BASE_HEADERS)
        info: Root = res.json()
        context.create_result(
            "Misskey",
            url=f"https://{host}/channels/{channel_id}",
            name=info["name"],
            score=1.0,
            description=info["description"],
            profile_picture=info["bannerUrl"],
        )


class Root(TypedDict):
    id: str
    createdAt: str
    lastNotedAt: str
    name: str
    description: str
    userId: str
    bannerUrl: str
    pinnedNoteIds: List
    color: str
    isArchived: bool
    usersCount: int
    notesCount: int
    isFollowing: bool
    isFavorited: bool
    hasUnreadNote: bool
    pinnedNotes: List
