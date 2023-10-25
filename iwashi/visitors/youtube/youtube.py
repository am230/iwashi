import json
import re
from typing import Any
from urllib import parse

import bs4
import requests
from loguru import logger

from ...helper import BASE_HEADERS, HTTP_REGEX
from ...visitor import Context, SiteVisitor
from .types import about, channels


class Youtube(SiteVisitor):
    NAME = "Youtube"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"((m|gaming)\.)?(youtube\.com|youtu\.be)", re.IGNORECASE
    )

    def _channel_by_video(self, video_id: str) -> str | None:
        res = requests.get(
            "https://www.youtube.com/watch",
            params={"v": video_id},
            headers=BASE_HEADERS,
        )
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        author = soup.select_one("span[itemprop=author]")
        if author is None:
            return None
        author_url = author.select_one("link[itemprop=url]")
        if author_url is None:
            return None
        uri = parse.urlparse(author_url.attrs["href"])
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return f"https://www.youtube.com/{type}"
        raise Exception("Could not find channel")

    def _channel_by_url(self, url: str) -> str | None:
        res = requests.get(
            url,
            headers=BASE_HEADERS
            | {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "ja",
            },
        )
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        """
        metadata.channelMetadataRenderer.vanityChannelUrl
        """
        for script in soup.find_all("script"):
            if script.text.startswith("var ytInitialData = "):
                break
        else:
            raise Exception("Could not find ytInitialData")
        root: about.Root = json.loads(script.text[script.text.index("{") : -1])
        uri = parse.urlparse(
            root["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"]
        )
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return f"https://www.youtube.com/{type}"
        raise Exception("Could not find channel")

    def normalize(self, url: str) -> str | None:
        uri = parse.urlparse(url)
        if uri.hostname == "youtu.be":
            return self._channel_by_video(uri.path[1:])
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return f"https://www.youtube.com/{type}"
        if type == "watch":
            return self._channel_by_video(parse.parse_qs(uri.query)["v"][0])
        if type in ("channel", "user", "c"):
            return self._channel_by_url(url)
        return url

    def _extract_initial_data(self, url: str) -> Any:
        about_res = requests.get(f"{url}/about", headers=BASE_HEADERS)
        soup = bs4.BeautifulSoup(about_res.text, "html.parser")
        for script in soup.find_all("script"):
            if script.text.startswith("var ytInitialData = "):
                break
        else:
            logger.warning(f"[Youtube] Could not find ytInitialData {url}")
            raise Exception("Could not find ytInitialData")
        return json.loads(script.text[len("var ytInitialData = ") : -1])

    def _extract_tab(
        self, root: about.Root | channels.Root, name: str
    ) -> about.TabsItem0 | channels.TabsItem0 | None:
        name = name.lower()
        for tab in root["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]:
            if "content" in tab:
                pass
            if "tabRenderer" not in tab:
                continue
            endpoint = tab["tabRenderer"]["endpoint"]["commandMetadata"][
                "webCommandMetadata"
            ]["url"].split("/")[-1]
            if endpoint.lower() != name:
                continue
            if "content" not in tab["tabRenderer"]:
                raise Exception("Could not find content")
            return tab  # type: ignore
        else:
            raise Exception("Could not find about")

    def _extract_links(self, root: about.Root) -> set[str]:
        links = set()
        about_tab = self._extract_tab(root, "about")
        if about_tab is None:
            raise Exception("Could not find about")
        for section in about_tab["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"
        ]:
            for item in section["itemSectionRenderer"]["contents"]:
                if "channelAboutFullMetadataRenderer" not in item:
                    raise Exception("Could not find channelAboutFullMetadataRenderer")
                about_tab = item["channelAboutFullMetadataRenderer"]
                if "links" not in about_tab:
                    break
                for link in about_tab["links"]:
                    if "channelExternalLinkViewModel" not in link:
                        continue
                    for command in link["channelExternalLinkViewModel"]["link"][
                        "commandRuns"
                    ]:
                        link = command["onTap"]["innertubeCommand"]["urlEndpoint"][
                            "url"
                        ]
                        uri = parse.urlparse(link)
                        if uri.path == "/redirect":
                            link = parse.unquote(parse.parse_qs(uri.query)["q"][0])
                        links.add(link)
        return links

    def visit(self, url, context: Context):
        about_data: about.Root = self._extract_initial_data(f"{url}/about")

        profile_picture = None
        if "avatar" in about_data["header"]["c4TabbedHeaderRenderer"]:
            profile_picture = about_data["header"]["c4TabbedHeaderRenderer"]["avatar"][
                "thumbnails"
            ][0]["url"]

        about_tab = self._extract_tab(about_data, "about")
        description = None
        if about_tab and "description" in about_tab:
            description = about_tab["description"]["simpleText"]

        name = about_data["header"]["c4TabbedHeaderRenderer"]["title"]

        context.create_result(
            "Youtube",
            url=url,
            score=1.0,
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        for link in self._extract_links(about_data):
            context.visit(link)
        channels_data: channels.Root = self._extract_initial_data(f"{url}/channels")
        channels_tab = self._extract_tab(channels_data, "channels")
        if channels_tab is None:
            raise Exception("Could not find channels")
        for section in channels_tab["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"
        ]:
            for item in section["itemSectionRenderer"]["contents"]:
                if "gridRenderer" not in item:
                    continue
                for channel in item["gridRenderer"]["items"]:
                    channel = channel["gridChannelRenderer"]
                    channel_id = channel["navigationEndpoint"]["commandMetadata"][
                        "webCommandMetadata"
                    ]["url"].split("@")[-1]
                    context.visit(f"https://www.youtube.com/@{channel_id}")
