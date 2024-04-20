import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.twitter import Twitter
from tests.visitors.test import iterable_eq


twitter = Twitter()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://twitter.com/VALIGHT1"}:
        context = Context(session=session, visitor=visitor)
        assert await twitter.resolve_id(context, url) == "VALIGHT1"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://twitter.com/VALIGHT1"
    result = await twitter.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Twitter"
    assert result.title == "VALIGHT_YT"
    assert (
        result.description
        == "Hi, I'm Valight, a creative Fortnite mappeur\nWelcome to my twiter account.\nCODE VALIGHT"
    )
    assert (
        result.profile_picture
        == "https://pbs.twimg.com/profile_images/1512100269831639049/R4AjwP-9_normal.jpg"
    )
    assert iterable_eq(
        result.links,
        {"https://youtube.com/channel/UCDRIfKm06-e1dwSbnU1H9Rw"},
    )
