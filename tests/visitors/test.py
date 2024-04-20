from typing import Iterable

import aiohttp

from iwashi.visitor import Context, FakeVisitor, Result, SiteVisitor


def iterable_eq(a: Iterable, b: Iterable) -> bool:
    # Compare two iterables for equality
    # ignoring the order of elements
    for item in a:
        if item not in b:
            return False
    for item in b:
        if item not in a:
            return False
    return True


async def _test(site_visitor: SiteVisitor, correct_result: Result, *urls: str) -> None:
    # resolve id
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()
    for url in urls:
        context = Context(session=session, visitor=visitor)
        assert (
            await site_visitor.resolve_id(context, url) == correct_result.id
        ), f"Failed to resolve id for {url}"

    # visit
    for url in urls:
        result = await site_visitor.visit_url(session, url)
        assert result, f"Failed to visit {url}"
        assert result.url == correct_result.url, f"URL mismatch for {url}"
        assert result.visitor == correct_result.visitor, f"Visitor mismatch for {url}"
        assert result.name == correct_result.name, f"Name mismatch for {url}"
        assert (
            result.description == correct_result.description
        ), f"Description mismatch for {url}"
        assert (
            correct_result.profile_picture
            and result.profile_picture
            and (correct_result.profile_picture in result.profile_picture)
        ), f"Profile picture mismatch for {url}"
        assert iterable_eq(
            result.links, correct_result.links
        ), f"Links mismatch for {url}"
