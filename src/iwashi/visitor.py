from __future__ import annotations

import abc
import re
from dataclasses import dataclass, field
from typing import List, Optional, Protocol, Set

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
    links: Set[str] = field(default_factory=set)

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

    def enqueue_visit(self, url: str, context: Context) -> None:
        ...


class FakeVisitor(Visitor):
    def __init__(self):
        self.queue = []

    async def visit(self, url, context, **kwargs):
        raise NotImplementedError

    async def tree(self, url, context, **kwargs):
        raise NotImplementedError

    def enqueue_visit(self, url, context):
        self.queue.append(url)

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
        if self.result is None:
            raise ValueError("Result is not created yet")
        self.result.links.add(url)

    def mark_visited(self, url: str) -> None:
        self.visitor.mark_visited(url)

    def create_context(self, url: str) -> Context:
        return Context(session=self.session, url=url, visitor=self.visitor, parent=self)

    def enqueue_visit(self, url: str) -> None:
        self.link(url)
        self.visitor.enqueue_visit(url, self)


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

    async def visit_url(
        self, url: str, session: aiohttp.ClientSession
    ) -> Result | None:
        visitor = FakeVisitor()
        context = Context(session=session, url=url, visitor=visitor)
        await self.visit(url, context)
        return context.result
