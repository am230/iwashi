import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.reddit import Reddit
from tests.visitors.test import iterable_eq


reddit = Reddit()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://www.reddit.com/user/MarcusFaze/"}:
        context = Context(session=session, visitor=visitor)
        assert await reddit.resolve_id(context, url) == "MarcusFaze"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.reddit.com/user/MarcusFaze"
    result = await reddit.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Reddit"
    assert result.title == "MarcusFaze"
    assert result.description == "I’m 18, I’m a Wrestling Fan,I’m from North Carolina"
    assert (
        result.profile_picture
        == "https://styles.redditmedia.com/t5_25b6em/styles/profileIcon_ym46r18i589b1.jpg?width=256&amp;height=256&amp;crop=256:256,smart&amp;s=7b7e1b4c208f847f36de445ebd5b8f0c32657071"
    )
    assert iterable_eq(
        result.links,
        {"https://twitter.com/marcus_faze"},
    )
