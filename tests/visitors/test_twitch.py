import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.twitch import Twitch
from tests.visitors.test import iterable_eq


twitch = Twitch()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://www.twitch.tv/thechief1114"}:
        context = Context(session=session, visitor=visitor)
        assert await twitch.resolve_id(context, url) == "thechief1114"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.twitch.tv/thechief1114"
    result = await twitch.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Twitch"
    assert result.title == "TheChief1114"
    assert result.description == "I stream."
    assert (
        result.profile_picture
        == "https://static-cdn.jtvnw.net/jtv_user_pictures/7a7f1681-f8ea-424d-bbce-38cac15e3328-profile_image-300x300.png"
    )
    assert iterable_eq(
        result.links,
        {"https://twitter.com/The_Chief1114"},
    )
