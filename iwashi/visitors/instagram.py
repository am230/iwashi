from typing_extensions import TypedDict
from typing import List
import re

import requests

from ..visitor import Context, SiteVisitor
from ..helper import HTTP_REGEX


class Instagram(SiteVisitor):
    NAME = 'Instagram'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'instagram\.com/(?P<id>\w+)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://www.instagram.com/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        session = requests.Session()
        session.headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'https://www.instagram.com/{id}/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'x-asbd-id': '198387',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest'
        }

        url = f'https://www.instagram.com/{id}/'
        res = requests.get(url)
        match = re.search(r'\"X-IG-App-ID\": ?\"(?P<id>\d{15})\"', res.text)
        if match is None:
            print(f'No X-IG-App-ID found in {url}')
            return
        session.headers['x-ig-app-id'] = match.group('id')
        
        csrf_res = requests.get('https://www.instagram.com/ajax/bz?__d=dis')
        session.headers['x-csrftoken'] = csrf_res.cookies.get_dict()['csrftoken']

        info_res = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={id}')
        if not info_res.ok or info_res.history:
            print('[Instagram] Blocked by Instagram')
            context.create_result('Instagram', url=url, name=id, score=0.0, description='Blocked by Instagram')
            return
        info: Root = info_res.json()
        user = info['data']['user']
        context.create_result('Instagram', url=url, score=1.0, description=user['biography'])

        for link in user['bio_links']:
            context.visit(link['url'])


class BioLinksItem0(TypedDict):
    title: str
    lynx_url: str
    url: str
    link_type: str


class BiographyWithEntities(TypedDict):
    raw_text: str
    entities: List


class EdgeFollowedBy(TypedDict):
    count: int


class EdgeMutualFollowedBy(TypedDict):
    count: int
    edges: List


class User(TypedDict):
    biography: str
    bio_links: List[BioLinksItem0]
    biography_with_entities: BiographyWithEntities
    blocked_by_viewer: bool
    restricted_by_viewer: None
    country_block: bool
    external_url: str
    external_url_linkshimmed: str
    edge_followed_by: EdgeFollowedBy
    fbid: str
    followed_by_viewer: bool
    edge_follow: EdgeFollowedBy
    follows_viewer: bool
    full_name: str
    group_metadata: None
    has_ar_effects: bool
    has_clips: bool
    has_guides: bool
    has_channel: bool
    has_blocked_viewer: bool
    highlight_reel_count: int
    has_requested_viewer: bool
    hide_like_and_view_counts: bool
    id: str
    is_business_account: bool
    is_professional_account: bool
    is_supervision_enabled: bool
    is_guardian_of_viewer: bool
    is_supervised_by_viewer: bool
    is_supervised_user: bool
    is_embeds_disabled: bool
    is_joined_recently: bool
    guardian_id: None
    business_address_json: None
    business_contact_method: str
    business_email: None
    business_phone_number: None
    business_category_name: None
    overall_category_name: None
    category_enum: None
    category_name: str
    is_private: bool
    is_verified: bool
    edge_mutual_followed_by: EdgeMutualFollowedBy
    profile_pic_url: str
    profile_pic_url_hd: str
    requested_by_viewer: bool
    should_show_category: bool
    should_show_public_contacts: bool
    transparency_label: None
    transparency_product: str
    username: str
    connected_fb_page: None
    pronouns: List


class Data(TypedDict):
    user: User


class Root(TypedDict):
    data: Data
    status: str
