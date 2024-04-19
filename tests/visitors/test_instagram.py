import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.fanbox import Fanbox
from tests.visitors.test import iterable_eq


fanbox = Fanbox()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://masahiro-emotion.fanbox.cc/",
        "https://masahiro-emotion.fanbox.cc/posts/7382756",
    }:
        context = Context(session=session, visitor=visitor)
        assert await fanbox.resolve_id(context, url) == "masahiro-emotion"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://masahiro-emotion.fanbox.cc"
    result = await fanbox.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Fanbox"
    assert result.title == "Masahiro Emoto"
    assert (
        result.description
        == "English text is shown below\r\n\r\n私はアニメーション監督、キャラクターデザイナー、作画監督、イラスレーター、ロボットのビヘイビアデザインなど活動しているクリエイターです。\r\n参加作品は\r\n・攻殻機動隊\r\n・カウボーイビバップ\r\n・Animatrix\r\n・REDLINE\r\n・BLEACH\r\n\r\nなど様々なプロジェクトに参加してました。\r\n\r\nI am a creator involved in various roles such as animation director, character designer, animation supervisor, illustrator, and robot behavior design.\r\nI have contributed to projects such as Ghost in the Shell, Cowboy Bebop, Animatrix, REDLINE, BLEACH, and many others."
    )
    assert (
        result.profile_picture
        == "https://pixiv.pximg.net/c/160x160_90_a2_g5/fanbox/public/images/user/91970939/icon/aAE8bJoSKtAtHhWK17NUmMFI.jpeg"
    )
    assert iterable_eq(
        result.links,
        {"https://x.com/masahiroemotion/"},
    )
