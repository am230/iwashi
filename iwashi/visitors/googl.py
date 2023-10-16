import re

import requests

from ..helper import BASE_HEADERS, HTTP_REGEX
from ..visitor import Context, SiteVisitor


class Googl(SiteVisitor):
    NAME = "Googl"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"goo\.gl/(?P<id>\w+)", re.IGNORECASE
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        res = requests.get(f"https://goo.gl/{id}", headers=BASE_HEADERS)
        context.create_result("Googl", url=url, score=1.0)
        context.visit(res.url)
