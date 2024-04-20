import json
import re
from typing import Tuple
from urllib import parse

import bs4

from iwashi.helper import BASE_HEADERS, HTTP_REGEX
from iwashi.visitor import Context, Service

from .types import thumbnails, ytinitialdata
from .types.about import AboutRes

VANITY_ID_REGEX = re.compile(r"youtube.com/@(?P<id>[\w-]+)")


class Youtube(Service):
    def __init__(self):
        super().__init__(
            name="Youtube",
            regex=re.compile(
                HTTP_REGEX + r"((m|gaming)\.)?(youtube\.com|youtu\.be)",
            ),
        )

    async def resolve_id(self, context: Context, url: str) -> str | None:
        uri = parse.urlparse(url)
        if uri.hostname == "youtu.be":
            return await self._channel_by_video(context, uri.path[1:])
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return self._id_from_vanity_url(url)
        if type == "playlist":
            return None
        if type == "watch":
            return await self._channel_by_video(
                context, parse.parse_qs(uri.query)["v"][0]
            )
        if type in ("channel", "user", "c"):
            return await self._channel_by_url(context, url)
        return uri.path.split("/")[1]

    async def _channel_by_video(self, context: Context, video_id: str) -> str | None:
        result = await self._channel_by_oembed(context, video_id)
        if result is not None:
            return result
        response = await context.session.get(
            f"https://www.youtube.com/watch?v={video_id}"
        )
        response.raise_for_status()
        soup = bs4.BeautifulSoup(await response.text(), "html.parser")
        element = soup.select_one('span[itemprop="author"] > link[itemprop="url"]')
        if element is None:
            return None
        href = element.attrs.get("href")
        if href is None:
            return None
        return self._id_from_vanity_url(href)

    async def _channel_by_oembed(self, context: Context, video_id: str) -> str | None:
        res = await context.session.get(
            "https://www.youtube.com/oembed",
            params={
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "format": "json",
            },
        )
        res.raise_for_status()
        data = await res.json()
        author_url = data.get("author_url")
        if author_url is None:
            return None
        return self._id_from_vanity_url(author_url)

    async def _channel_by_url(self, context: Context, url: str) -> str | None:
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        vanity_url = data["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"]
        return self._id_from_vanity_url(vanity_url)

    def _id_from_vanity_url(self, url: str) -> str | None:
        match = VANITY_ID_REGEX.search(url)
        if match is None:
            return None
        return match.group("id")

    def parse_thumbnail(self, thumbnails: thumbnails) -> str:
        size = 0
        url: str | None = None
        for thumbnail in thumbnails["thumbnails"]:
            if thumbnail["width"] > size:
                size = thumbnail["width"]
                url = thumbnail["url"]
        if url is None:
            raise RuntimeError("Thumbnail not found")
        return url

    def parse_token(
        self, data: ytinitialdata
    ) -> Tuple[str | None, Tuple[str, str] | None]:
        # TODO: 地獄
        first_link = None
        c4TabbedHeaderRenderer = data["header"]["c4TabbedHeaderRenderer"]
        if "headerLinks" not in c4TabbedHeaderRenderer:
            return (first_link, None)
        channelHeaderLinksViewModel = c4TabbedHeaderRenderer["headerLinks"][
            "channelHeaderLinksViewModel"
        ]
        if "firstLink" in channelHeaderLinksViewModel:
            first_link = channelHeaderLinksViewModel["firstLink"]["commandRuns"][0][
                "onTap"
            ]["innertubeCommand"]["urlEndpoint"]["url"]
        if "more" not in channelHeaderLinksViewModel:
            return (first_link, None)
        runs = channelHeaderLinksViewModel["more"]["commandRuns"]
        command = runs[0]["onTap"]["innertubeCommand"]
        if "showEngagementPanelEndpoint" not in command:
            raise RuntimeError("token not found")
        contents1 = command["showEngagementPanelEndpoint"]["engagementPanel"][
            "engagementPanelSectionListRenderer"
        ]["content"]["sectionListRenderer"]["contents"]
        contents2 = contents1[0]["itemSectionRenderer"]["contents"]
        endpoint = contents2[0]["continuationItemRenderer"]["continuationEndpoint"]
        api_url = endpoint["commandMetadata"]["webCommandMetadata"]["apiUrl"]
        token = endpoint["continuationCommand"]["token"]
        return (first_link, (api_url, token))

    def parse_redirect(self, url: str) -> str:
        uri = parse.urlparse(url)
        if uri.hostname != "www.youtube.com":
            return url
        if uri.path == "/redirect":
            return parse.parse_qs(uri.query)["q"][0]
        return url

    async def visit(self, context: Context, id: str):
        url = f"https://www.youtube.com/@{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        vanity_id = data["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"]
        name = data["metadata"]["channelMetadataRenderer"]["title"]
        description = data["metadata"]["channelMetadataRenderer"]["description"]
        profile_picture = self.parse_thumbnail(
            data["metadata"]["channelMetadataRenderer"]["avatar"]
        )
        context.create_result(
            self,
            id=id,
            url=f"https://www.youtube.com/@{vanity_id.split('@')[1]}",
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        first_link, api = self.parse_token(data)
        if first_link is not None:
            context.enqueue_visit(self.parse_redirect(first_link))
        if api is None:
            return
        api_url, token = api
        about_res = await context.session.post(
            f"https://www.youtube.com{api_url}",
            data=json.dumps(
                {
                    "context": {
                        "client": {
                            "userAgent": context.session.headers.get(
                                "User-Agent", BASE_HEADERS["User-Agent"]
                            ),
                            "clientName": "WEB",
                            "clientVersion": "2.20231219.04.00",
                        }
                    },
                    "continuation": token,
                }
            ),
        )
        about_res.raise_for_status()
        about_data: AboutRes = await about_res.json()
        links = about_data["onResponseReceivedEndpoints"][0][
            "appendContinuationItemsAction"
        ]["continuationItems"][0]["aboutChannelRenderer"]["metadata"][
            "aboutChannelViewModel"
        ]["links"]
        for link in links:
            link_url = link["channelExternalLinkViewModel"]["link"]["content"]
            context.enqueue_visit(self.parse_redirect(link_url))

    def extract_initial_data(self, soup: bs4.BeautifulSoup) -> ytinitialdata:
        for script in soup.select("script"):
            if script.string is None:
                continue
            match = re.search(r"ytInitialData\s*=\s*({.*?});", script.string)
            if match is not None:
                data: ytinitialdata = json.loads(match.group(1))
                break
        else:
            raise RuntimeError("ytInitialData not found")
        return data
