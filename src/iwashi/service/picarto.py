from typing import TypedDict, Literal, List, Optional
import re
from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Picarto(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Picarto",
            regex=re.compile(HTTP_REGEX + r"picarto\.tv/(?P<id>\w+)", re.IGNORECASE),
        )

    async def resolve_id(self, context: Context, url: str) -> str | None:
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = await context.session.get(
            "https://ptvintern.picarto.tv/api/channel/profile/raptorartstudios",
            headers=headers,
        )
        profile_response: ProfileResponse = await response.json()
        return str(profile_response["data"]["id"])

    async def visit(self, context: Context, id: str):
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = await context.session.get(
            "https://ptvintern.picarto.tv/api/channel/profile/raptorartstudios",
            headers=headers,
        )

        profile_response: ProfileResponse = await response.json()
        profile = profile_response["data"]

        context.create_result(
            self,
            id=id,
            url=f"https://picarto.tv/{profile['name']}",
            name=profile["name"],
            description=profile["bio"],
            profile_picture=profile["avatar"],
        )

        for social in profile["social_medias"]:
            context.enqueue_visit(social["link"])


class Category(TypedDict):
    id: int
    name: str


class Language(TypedDict):
    id: int
    name: str
    code: str
    image: str


class SocialMedia(TypedDict):
    icon: str
    link: str


class Tag(TypedDict):
    name: str


class Software(TypedDict):
    id: int
    name: str


class Tool(TypedDict):
    id: int
    name: str


class Banner(TypedDict):
    id: int
    image: str
    link: Optional[str]
    type: str


class DMSetting(TypedDict):
    allow_message_every_one: bool


class UserData(TypedDict):
    id: int
    name: str
    account_type: Literal["PREMIUM"]
    avatar: str
    bio: str
    verified: bool
    total_views: int
    profile_color: Optional[str]
    enable_subscription: bool
    created_at: str  # ISO 8601 形式
    followers_count: int
    videos_count: int
    categories: List[Category]
    languages: List[Language]
    social_medias: List[SocialMedia]
    tags: List[Tag]
    softwares: List[Software]
    tools: List[Tool]
    banners: List[Banner]
    ubanned: bool
    subscribed: bool
    following: bool
    gifted: bool
    dm_setting: DMSetting


class ProfileResponse(TypedDict):
    data: UserData
