from __future__ import annotations

import abc
import re
from dataclasses import dataclass, field
from typing import List, Optional, Protocol

import aiohttp

HTTP_REGEX = "(https?://)?(www.)?"


@dataclass
class Result:
    url: str
    site_name: Optional[str]
    title: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]

    children: List[Result] = field(default_factory=list)
    links: List[str] = field(default_factory=list)

    def to_list(self) -> List[Result]:
        links: List[Result] = [self]
        for child in self.children:
            links.extend(child.to_list())
        return links


class Visitor(Protocol):
    async def visit(self, url: str, context: Context, **kwargs) -> Result:
        ...

    def mark_visited(self, url: str) -> None:
        ...

    def push(self, url: str, context: Context) -> None:
        ...


class FakeVisitor(Visitor):
    def __init__(self):
        self.visited = []

    async def visit(self, url, context, **kwargs):
        self.visited.append(url)

    async def tree(self, url, context, **kwargs):
        raise NotImplementedError

    def push(self, url, context):
        raise NotImplementedError

    def mark_visited(self, url):
        raise NotImplementedError


@dataclass
class Context:
    session: aiohttp.ClientSession
    url: str
    visitor: Visitor
    parent: Optional[Context] = None
    result: Optional[Result] = None

    def create_result(
        self,
        site_name: str,
        url: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        profile_picture: Optional[str] = None,
    ) -> Result:
        self.result = Result(
            site_name=site_name,
            url=url,
            title=name,
            description=description,
            profile_picture=profile_picture,
        )

        if self.parent and self.parent.result:
            self.parent.result.children.append(self.result)

        return self.result

    def link(self, url: str) -> None:
        if self.result is not None:
            self.result.links.append(url)

    def mark_visited(self, url: str) -> None:
        self.visitor.mark_visited(url)

    def new_context(self, url: str) -> Context:
        return Context(session=self.session, url=url, visitor=self.visitor, parent=self)

    def push(self, url: str) -> None:
        self.visitor.push(url, self)


class SiteVisitor(abc.ABC):
    NAME: Optional[str] = None
    URL_REGEX: Optional[re.Pattern] = None

    def match(self, url, context: Context) -> Optional[re.Match]:
        if self.URL_REGEX is None:
            raise NotImplementedError()
        return self.URL_REGEX.match(url)

    async def normalize(self, context: Context, url: str) -> str | None:
        return url

    @abc.abstractmethod
    async def visit(self, url, context: Context, **kwargs) -> Optional[Result]:
        raise NotImplementedError()
