import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.nicovideo import Nicovideo
from tests.visitors.test import iterable_eq


nicovideo = Nicovideo()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://www.nicovideo.jp/user/128134532"}:
        context = Context(session=session, visitor=visitor)
        assert await nicovideo.resolve_id(context, url) == "128134532"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.nicovideo.jp/user/128134532"
    result = await nicovideo.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Nicovideo"
    assert result.title == "ラベンダーP"
    assert (
        result.description
        == "鉄道、東方、艦これ、ボカロ、ボイロ、野球、応援歌、阪神タイガース、千葉ロッテマリーンズ、埼玉西武ライオンズ、オリックスバファローズ、東方のすくすく白沢、艦これの連装砲ちゃんが好きな人です<br><br>2006年4月17日生まれで岡山県備前市日生町(カキオコで有名な町)に住んでます"
    )
    assert (
        result.profile_picture
        == "https://secure-dcdn.cdn.nimg.jp/nicoaccount/usericon/12813/128134532.jpg?1710066983"
    )
    assert iterable_eq(
        result.links,
        {
            "https://www.youtube.com/channel/UC4jehnRY1GBPBpg-Np4WFNg",
            "https://twitter.com/lavenderp2018",
        },
    )
