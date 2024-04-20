import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.soundcloud import Soundcloud
from tests.visitors.test import iterable_eq


soundcloud = Soundcloud()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://soundcloud.com/speder2",
        "https://soundcloud.com/speder2/tracks",
    }:
        context = Context(session=session, visitor=visitor)
        assert await soundcloud.resolve_id(context, url) == "speder2"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://soundcloud.com/speder2"
    result = await soundcloud.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Soundcloud"

    assert result.title == "Speder2"

    assert result.description == "ゲーム製作サークルの音楽・SEを担当しています"
    assert (
        result.profile_picture
        == "https://i1.sndcdn.com/avatars-000125467778-jpowym-large.jpg"
    )
    assert iterable_eq(
        result.links,
        {
            "http://kohada.ushimairi.com/",
        },
    )
