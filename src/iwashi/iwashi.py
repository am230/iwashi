import asyncio
from typing import List, MutableSet, Optional
import aiohttp

from loguru import logger

from .helper import BASE_HEADERS, DEBUG, normalize_url, parse_host
from .visitor import Context, Result, SiteVisitor, Visitor


class Iwashi(Visitor):
    def __init__(self) -> None:
        self.visitors: List[SiteVisitor] = []
        self.visited: MutableSet[str] = set()
        self.tasks: List[asyncio.Task] = []
        self.session = aiohttp.ClientSession(headers=BASE_HEADERS)

    def add_visitor(self, visitor: SiteVisitor) -> None:
        self.visitors.append(visitor)

    def is_visited(self, url: str) -> bool:
        return url in self.visited

    def mark_visited(self, url: str) -> bool:
        url = url.lower()
        if self.is_visited(url):
            return False
        self.visited.add(url)
        return True

    async def tree(self, url: str, context: Optional[Context] = None) -> Result | None:
        context = context or Context(session=self.session, url=url, visitor=self)
        context = context.new_context(url)
        result = await self.visit(url, context)
        while self.tasks:
            await self.tasks.pop()

        return result

    def push(self, url: str, context: Context) -> None:
        coro = self.visit(url, context)
        task = asyncio.create_task(coro)
        self.tasks.append(task)

    async def visit(
        self, _url: str, context: Optional[Context] = None
    ) -> Optional[Result]:
        url = normalize_url(_url)
        if url is None:
            return None
        if context is None:
            context = Context(session=self.session, url=url, visitor=self)
        else:
            context = context.new_context(url)
        if self.is_visited(url):
            return None
        for visitor in self.visitors:
            match = visitor.match(url, context)
            if match is None:
                continue

            try:
                normalized = await visitor.normalize(context, url)
                if normalized is None:
                    continue
                if self.mark_visited(normalized):
                    match = visitor.match(normalized, context)
                    if match is not None:
                        await visitor.visit(normalized, context, **match.groupdict())
                elif context.parent is not None:
                    context.parent.link(normalized)
            except Exception as e:
                logger.warning(f"[Visitor Error] {url} {visitor.__class__.__name__}")
                logger.exception(e)
                if DEBUG:
                    raise e
                continue
            break
        else:
            context.create_result(site_name=parse_host(url), url=url)
            self.mark_visited(url)
            if await self.try_redirect(url, context):
                return context.result
            else:
                logger.warning(f"[No Visitor Found] {url}")

        return context.result

    async def try_redirect(self, url: str, context: Context) -> bool:
        try:
            res = await context.session.get(
                url, headers=BASE_HEADERS, allow_redirects=True, timeout=5
            )
        except aiohttp.ClientError as e:
            logger.exception(e)
            logger.warning(f"[Redirect] failed to redirect {url}")
            return False
        except asyncio.TimeoutError as e:
            logger.exception(e)
            logger.warning(f"[Redirect] failed to redirect {url}")
            return False
        new_url = str(res.url)
        if new_url == url:
            return False
        context.create_result(site_name=parse_host(url), url=url)
        context.enqueue(new_url)
        logger.info(f"[Redirect] {url} -> {new_url}")
        return True


def get_iwashi():
    iwashi = Iwashi()
    add_visitors(iwashi)
    return iwashi


def add_visitors(iwashi):
    from . import visitors

    for attr in dir(visitors):
        value = getattr(visitors, attr)
        if attr.startswith("_"):
            continue
        if isinstance(value, type) and issubclass(value, SiteVisitor):
            iwashi.add_visitor(value())


async def visit(url: str, iwashi: Optional[Iwashi] = None) -> Optional[Result]:
    iwashi = iwashi or get_iwashi()
    return await iwashi.tree(url)
