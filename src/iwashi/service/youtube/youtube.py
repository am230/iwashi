import json
import re
from typing import Any, Optional
from urllib import parse

import bs4

from iwashi.helper import HTTP_REGEX, normalize_url
from iwashi.service.youtube.types.ytinitialdata2 import ProfileRes2
from iwashi.service.youtube.types.ytinitialdata3 import ProfileRes3
from iwashi.visitor import Context, Service

from .types import thumbnails, ytinitialdata
from .types.about import AboutRes

VANITY_ID_REGEX = re.compile(r"youtube\.com/@(?P<id>[^/]+)")
CHANNEL_ID_REGEX = re.compile(r"youtube\.com/channel/(?P<id>[^/]+)")


class Youtube(Service):
    def __init__(self):
        super().__init__(
            name="Youtube",
            regex=re.compile(
                HTTP_REGEX + r"((m|gaming)\.)?(youtube\.com|youtu\.be)",
            ),
        )

    async def resolve_id(self, context: Context, url: str) -> Optional[str]:
        normalized_url = normalize_url(url)
        if not normalized_url:
            return None

        uri = parse.urlparse(normalized_url)
        if uri.hostname == "youtu.be":
            return await self._channel_by_oembed(context, uri.path[1:])

        path_parts = list(filter(None, uri.path.split("/")))
        if not path_parts:
            return None

        url_type = path_parts[0]

        if url_type.startswith("@"):
            return await self._id_from_vanity_url(context, url)
        if url_type == "playlist":
            return None
        if url_type == "watch":
            query_v = parse.parse_qs(uri.query).get("v")
            if query_v:
                return await self._channel_by_oembed(context, query_v[0])
        if url_type in {"live", "shorts"}:
            return await self._channel_by_oembed(context, path_parts[-1])
        if url_type in {"channel", "user", "c"}:
            return await self._channel_by_url(context, url)

        if len(path_parts) > 1:
            maybe_vanity = path_parts[1]
            return await self._id_from_vanity_url(
                context, f"https://youtube.com/@{maybe_vanity}"
            )
        return None

    async def _channel_by_oembed(
        self, context: Context, video_id: str
    ) -> Optional[str]:
        res = await context.session.get(
            "https://www.youtube.com/oembed",
            params={
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "format": "json",
            },
        )
        if not res.ok:
            return None

        data = await res.json()
        author_url = data.get("author_url")
        if not author_url:
            return None

        return await self._id_from_vanity_url(context, author_url)

    async def _channel_by_url(self, context: Context, url: str) -> Optional[str]:
        res = await context.session.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        vanity_url = data["metadata"]["channelMetadataRenderer"]["channelUrl"]

        return self._parse_channel_id(vanity_url)

    def _parse_channel_id(self, channel_url: str) -> Optional[str]:
        match = CHANNEL_ID_REGEX.search(channel_url)
        return parse.unquote(match.group("id")) if match else None

    def _vanity_id_from_url(self, url: str) -> str | None:
        match = VANITY_ID_REGEX.search(url)
        if not match:
            return None
        return parse.unquote(match.group("id"))

    async def _id_from_vanity_url(self, context: Context, url: str) -> Optional[str]:
        vanity_id = self._vanity_id_from_url(url)
        if vanity_id is None:
            return None
        res = await context.session.get(f"https://www.youtube.com/@{vanity_id}")
        res.raise_for_status()

        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        channel_url = data["metadata"]["channelMetadataRenderer"]["channelUrl"]

        return self._parse_channel_id(channel_url)

    def parse_thumbnail(self, thumbnails_data: thumbnails) -> str:
        """最大の幅を持つサムネイルのURLを取得する"""
        thumb_list = thumbnails_data.get("thumbnails", [])
        if not thumb_list:
            raise RuntimeError("Thumbnail not found")

        best_thumb = max(thumb_list, key=lambda t: t.get("width", 0))
        return best_thumb["url"]

    async def get_token(self, data: Any) -> Optional[str]:
        header = data.get("header", {})
        if "pageHeaderRenderer" in header:
            return self._get_token_from_page_header(data)
        elif "c4TabbedHeaderRenderer" in header:
            return self._get_token_from_c4_header(data)
        return None

    def _extract_token_from_endpoints(self, contents: list) -> Optional[str]:
        """深くネストされた構造からcontinuationTokenを抽出するヘルパー"""
        for item in contents:
            sections = item.get("itemSectionRenderer", {}).get("contents", [])
            for section in sections:
                endpoint = section.get("continuationItemRenderer", {}).get(
                    "continuationEndpoint", {}
                )

                # トークンが直接存在する場合
                token = endpoint.get("continuationCommand", {}).get("token")
                if token:
                    return token

                # API URLのパスから判別する場合
                api_url = (
                    endpoint.get("commandMetadata", {})
                    .get("webCommandMetadata", {})
                    .get("apiUrl", "")
                )
                if api_url.startswith("/youtubei/v1/browse"):
                    return endpoint.get("continuationCommand", {}).get("token")
        return None

    def _get_token_from_page_header(self, data: ProfileRes2) -> Optional[str]:
        view_model = (
            data.get("header", {})
            .get("pageHeaderRenderer", {})
            .get("content", {})
            .get("pageHeaderViewModel", {})
        )

        # 1. description経由での探索
        try:
            contents = (
                view_model.get("description", {})
                .get("descriptionPreviewViewModel", {})
                .get("rendererContext", {})
                .get("commandContext", {})
                .get("onTap", {})
                .get("innertubeCommand", {})
                .get("showEngagementPanelEndpoint", {})
                .get("engagementPanel", {})
                .get("engagementPanelSectionListRenderer", {})
                .get("content", {})
                .get("sectionListRenderer", {})
                .get("contents", [])
            )
            token = self._extract_token_from_endpoints(contents)
            if token:
                return token
        except KeyError:
            pass

        # 2. attribution経由での探索
        try:
            command_runs = (
                view_model.get("attribution", {})
                .get("attributionViewModel", {})
                .get("suffix", {})
                or {}
            ).get("commandRuns", {})
            for run in command_runs:
                contents = run["onTap"]["innertubeCommand"][
                    "showEngagementPanelEndpoint"
                ]["engagementPanel"]["engagementPanelSectionListRenderer"]["content"][
                    "sectionListRenderer"
                ]["contents"]
                token = self._extract_token_from_endpoints(contents)
                if token:
                    return token
        except KeyError:
            pass

        return None

    def _get_token_from_c4_header(self, data: ProfileRes3) -> Optional[str]:
        try:
            command_runs = data["header"]["c4TabbedHeaderRenderer"]["headerLinks"][
                "channelHeaderLinksViewModel"
            ]["more"]["commandRuns"]
            for run in command_runs:
                contents = run["onTap"]["innertubeCommand"][
                    "showEngagementPanelEndpoint"
                ]["engagementPanel"]["engagementPanelSectionListRenderer"]["content"][
                    "sectionListRenderer"
                ]["contents"]
                token = self._extract_token_from_endpoints(contents)
                if token:
                    return token
        except KeyError:
            pass

        return None

    def parse_redirect(self, url: str) -> str:
        uri = parse.urlparse(url)
        if uri.hostname == "www.youtube.com" and uri.path == "/redirect":
            query_q = parse.parse_qs(uri.query).get("q")
            if query_q:
                return query_q[0]
        return url

    async def visit(self, context: Context, id: str):
        url = f"https://www.youtube.com/channel/{id}"
        res = await context.session.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        metadata = data["metadata"]["channelMetadataRenderer"]

        channel_id = await self._id_from_vanity_url(
            context, metadata["vanityChannelUrl"]
        )

        screen_id = self._vanity_id_from_url(metadata["vanityChannelUrl"])

        context.create_result(
            self,
            id=id,
            unique_id=id,
            screen_id=screen_id,
            url=f"https://www.youtube.com/channel/{channel_id}",
            name=metadata["title"],
            description=metadata["description"],
            profile_picture=self.parse_thumbnail(metadata["avatar"]),
        )

        token = await self.get_token(data)
        if token:
            await self._fetch_and_enqueue_about_links(context, token)

    async def _fetch_and_enqueue_about_links(self, context: Context, token: str):
        """概要欄のリンクを取得し、キューに追加する"""
        res = await context.session.post(
            "https://www.youtube.com/youtubei/v1/browse",
            json={
                "context": {
                    "client": {
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36,gzip(gfe)",
                        "clientName": "WEB",
                        "clientVersion": "2.20240509.00.00",
                    },
                },
                "continuation": token,
            },
        )
        res.raise_for_status()
        about_data: AboutRes = await res.json()

        try:
            for endpoint in about_data.get("onResponseReceivedEndpoints", []):
                for item in endpoint.get("appendContinuationItemsAction", {}).get(
                    "continuationItems", []
                ):
                    links_data = (
                        item.get("aboutChannelRenderer", {})
                        .get("metadata", {})
                        .get("aboutChannelViewModel", {})
                        .get("links", [])
                    )

                    for link_obj in links_data:
                        for run in (
                            link_obj.get("channelExternalLinkViewModel", {})
                            .get("link", {})
                            .get("commandRuns", [])
                        ):
                            extracted_url = (
                                run.get("onTap", {})
                                .get("innertubeCommand", {})
                                .get("urlEndpoint", {})
                                .get("url")
                            )
                            if extracted_url:
                                context.enqueue_visit(
                                    self.parse_redirect(extracted_url)
                                )
        except Exception:
            # データ構造がない・変更された場合はスキップ
            pass

    def extract_initial_data(self, soup: bs4.BeautifulSoup) -> ytinitialdata:
        for script in soup.select("script"):
            if not script.string:
                continue
            match = re.search(r"ytInitialData\s*=\s*(\{.+\});", script.string)
            if match:
                return json.loads(match.group(1))
        raise RuntimeError("ytInitialData not found")
