import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.twitcasting import TwitCasting
from tests.visitors.test import iterable_eq


twitcasting = TwitCasting()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://twitcasting.tv/kaizi0817",
        "https://twitcasting.tv/kaizi0817/archive/",
    }:
        context = Context(session=session, visitor=visitor)
        assert await twitcasting.resolve_id(context, url) == "kaizi0817"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://twitcasting.tv/kaizi0817"
    result = await twitcasting.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "TwitCasting"
    assert result.title == "細貝直心"
    assert (
        result.description
        == "細貝直心 / 1996年8月17日24歳/2021年2月〜メンズスキンケアD2Cブランド@serra_adsonをリリース中‼︎/若い人達が挑戦するきっかけを作りたい/フォローお願いします/tiktokも始めました！"
    )
    assert result.profile_picture and (
        result.profile_picture
        == "https://imagegw02.twitcasting.tv/image3s/pbs.twimg.com/profile_images/1412219689615302662/Gxz3711a_bigger.jpg"
    )
    assert iterable_eq(
        result.links,
        {"https://twitter.com/kaizi0817"},
    )
