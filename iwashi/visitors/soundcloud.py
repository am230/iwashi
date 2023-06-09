import json
import re
from typing import List

import requests
from typing_extensions import TypedDict

from ..visitor import Context, SiteVisitor
from ..helper import HTTP_REGEX


class Soundcloud(SiteVisitor):
    NAME = 'Soundcloud'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'soundcloud\.com/(?P<id>[-\w]+)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://soundcloud.com/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        url = f'https://soundcloud.com/{id}'
        res = requests.get(url)
        info_json = re.search(r'window\.__sc_hydration ?= ?(?P<info>.+);', res.text)
        if info_json is None:
            print(f'[Soundcloud] Could not find info for {url}')
            return
        info_list: Root = json.loads(info_json.group('info'))
        for info in info_list:
            if info['hydratable'] == 'user':
                break
        else:
            print(f'[Soundcloud] Could not find user info for {url}')
            return

        context.create_result('Soundcloud', url=url, name=info['data']['username'], score=1.0, description=info['data']['description'], profile_picture=info['data']['avatar_url'])
        pass
        client_id_res = requests.get("https://a-v2.sndcdn.com/assets/0-bf97f26a.js")
        match = re.search(r"client_id: ?\"(?P<client_id>\w{32})\"", client_id_res.text)
        if match is None:
            print(f'[Soundcloud] Could not find client_id for {url}')
            return
        client_id = match.group('client_id')

        "https://api-v2.soundcloud.com/users/soundcloud:users:104832223/web-profiles?client_id=SDvic69dtCia3c4tYqKIhC6j7UfTPHLC&app_version=1678362857&app_locale=en"
        profile_res = requests.get(f'https://api-v2.soundcloud.com/users/{info["data"]["urn"]}/web-profiles?client_id={client_id}&app_version=1678362857&app_locale=en', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'
        })
        profile: List[ProfileItem] = profile_res.json()
        for item in profile:
            context.visit(item['url'])


class ProfileItem(TypedDict):
    url: str
    network: str
    title: str


class Product(TypedDict):
    id: str


class CreatorSubscriptionsItem0(TypedDict):
    product: Product


class VisualsItem0(TypedDict):
    urn: str
    entry_time: int
    visual_url: str


class Visuals(TypedDict):
    urn: str
    enabled: bool
    visuals: List[VisualsItem0]
    tracking: None


class Badges(TypedDict):
    pro: bool
    pro_unlimited: bool
    verified: bool


class Data4(TypedDict):
    avatar_url: str
    city: str
    comments_count: int
    country_code: str
    created_at: str
    creator_subscriptions: List[CreatorSubscriptionsItem0]
    creator_subscription: CreatorSubscriptionsItem0
    description: str
    followers_count: int
    followings_count: int
    first_name: str
    full_name: str
    groups_count: int
    id: int
    kind: str
    last_modified: str
    last_name: str
    likes_count: int
    playlist_likes_count: int
    permalink: str
    permalink_url: str
    playlist_count: int
    reposts_count: None
    track_count: int
    uri: str
    urn: str
    username: str
    verified: bool
    visuals: Visuals
    badges: Badges
    station_urn: str
    station_permalink: str
    url: str


class RootItem0(TypedDict):
    hydratable: str
    data: Data4


Root = List[RootItem0]
