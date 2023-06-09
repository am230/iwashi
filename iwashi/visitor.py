import re
from dataclasses import dataclass, field
from typing import List, Optional, Protocol

HTTP_REGEX = f'(https?://)?(www.)?'


@dataclass
class Result:
    site_name: Optional[str]
    url: str
    score: float
    title: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]

    children: List['Result'] = field(default_factory=list)
    links: List['str'] = field(default_factory=list)


class Visitor(Protocol):
    def visit(self, url: str, context: 'Context', **kwargs) -> Result: ...

    def mark_visited(self, url: str) -> None: ...


class Context:
    def __init__(self, url: str, visitor: Visitor, parent: Optional['Context'] = None):
        self.url = url
        self.visitor = visitor
        self.parent = parent
        self.result: Optional[Result] = None

    def create_result(self, site_name: str, url: str, score: float = 1.0, name: Optional[str] = None, description: Optional[str] = None, profile_picture: Optional[str] = None) -> Result:
        self.result = Result(site_name=site_name, url=url, score=score, title=name, description=description, profile_picture=profile_picture)

        if self.parent and self.parent.result:
            self.parent.result.children.append(self.result)

        return self.result

    def link(self, url: str) -> None:
        if self.result is not None:
            self.result.links.append(url)

    def mark_visited(self, url: str) -> None:
        self.visitor.mark_visited(url)

    def create(self, url: str) -> 'Context':
        return Context(url=url, visitor=self.visitor, parent=self)

    def visit(self, url: str) -> None:
        self.visitor.visit(url, self.create(url))

    def __repr__(self) -> str:
        return f'Context(url={self.url!r})'


class SiteVisitor:
    NAME: Optional[str] = None
    URL_REGEX: Optional[re.Pattern] = None

    def match(self, url, context: Context) -> Optional[re.Match]:
        if self.URL_REGEX is None:
            raise NotImplementedError()
        return self.URL_REGEX.match(url)

    def normalize(self, url: str) -> str:
        return url

    def visit(self, url, context: Context, **kwargs) -> Optional[Result]:
        raise NotImplementedError()
