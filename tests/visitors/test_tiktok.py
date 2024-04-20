import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.tiktok import TikTok
from tests.visitors.test import iterable_eq


tiktok = TikTok()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://www.tiktok.com/@cocoyola?lang=ja-JP",
        "https://www.tiktok.com/@cocoyola/video/7234867719043157274?lang=ja-JP",
    }:
        context = Context(session=session, visitor=visitor)
        assert await tiktok.resolve_id(context, url) == "cocoyola"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.tiktok.com/@cocoyola"
    result = await tiktok.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "TikTok"
    assert result.title == "☀️🥂🫶🏻⭐️🍸"
    assert (
        result.description == "-everything you’re looking for and more-\n\n🪸🌅🥂🫶🏻🍸"
    )
    assert result.profile_picture and (
        "tos-maliva-avt-0068/7325124622654341126~c5_1080x1080.jpeg"
        in result.profile_picture
    )
    assert iterable_eq(
        result.links,
        {},
    )
