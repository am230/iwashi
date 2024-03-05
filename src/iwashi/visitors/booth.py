import re

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, SiteVisitor


class Booth(SiteVisitor):
    NAME = "Booth"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"(?P<id>[\w-]+)\.booth\.pm", re.IGNORECASE
    )

    async def normalize(self, context: Context, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://{match.group("id")}.booth.pm'

    async def visit(self, url, context: Context, id: str):
        res = await context.session.get(f"https://{id}.booth.pm")
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        name_element = soup.select_one(".home-link-container__nickname")
        name = name_element is not None and name_element.find("a") or None
        desc_element = soup.select_one(".description")
        description = (
            desc_element is not None
            and desc_element.find(attrs={"v-html": "formattedDescription"})
            or None
        )
        avater_element = soup.select_one(".avatar-image")

        context.create_result(
            "Booth",
            url=url,
            name=name.text if name is not None else None,
            description=description.text if description is not None else None,
            profile_picture=avater_element.attrs["style"].split("url(")[1].split(")")[0]
            if avater_element is not None
            else None,
        )

        if desc_element is None:
            return
        for link in desc_element.select(".shop-contacts__link"):
            link = link.select_one("a")
            if link is None:
                continue
            if "href" in link.attrs:
                context.enqueue(link.attrs["href"])
