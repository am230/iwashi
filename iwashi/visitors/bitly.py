import re

import requests

from ..visitor import Context, SiteVisitor
from ..helper import HTTP_REGEX


class Bitly(SiteVisitor):
    NAME = 'Bitly'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'bit\.ly/(?P<id>\w+)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://bit.ly/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        res = requests.get(f'https://bit.ly/{id}')
        context.create_result('Bitly', url=url, score=1.0)
        context.visit(res.url)