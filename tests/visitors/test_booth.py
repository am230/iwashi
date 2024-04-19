import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.booth import Booth
from tests.visitors.test import iterable_eq


booth = Booth()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://miluda.booth.pm/",
        "https://miluda.booth.pm/items/397",
    }:
        context = Context(session=session, visitor=visitor)
        assert await booth.resolve_id(context, url) == "miluda"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://miluda.booth.pm"
    result = await booth.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Booth"
    assert result.title == "Sunshine Mill 太陽光工場"
    assert (
        result.description
        == "Welcome to 太陽光工場.\r\nMiludaと申します。同人初心者アメリカ人ですけどどうぞよろしくお願いします。メインは東方や艦これです。\r\n\r\nよろしくお願いします！"
    )
    assert (
        result.profile_picture
        == "https://booth.pximg.net/c/128x128/users/274/icon_image/41f84dbd-19af-49b9-8cf5-888eb389e500_base_resized.jpg"
    )
    assert iterable_eq(
        result.links,
        {
            "https://miluda.com",
            "https://twitter.com/Miluda",
            "https://www.pixiv.net/users/161480",
        },
    )
