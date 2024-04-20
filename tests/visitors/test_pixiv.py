import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.pixiv import Pixiv
from tests.visitors.test import iterable_eq


pixiv = Pixiv()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://www.pixiv.net/users/137796"}:
        context = Context(session=session, visitor=visitor)
        assert await pixiv.resolve_id(context, url) == "137796"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.pixiv.net/users/137796"
    result = await pixiv.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Pixiv"
    assert result.title == "画力欠乏症／妄想屋（仮名）"
    assert (
        result.description
        == "属性はロボ娘系。『日常』とか『らき☆すた』、『えす☆えふ』（らき☆すた二次創作）、『けものフレンズ』とかやってます。よろしくお願いします。\r\n\r\nメインのＨＮの略称は、「がけつ」または「ＧＫ２」。\r\nなお、状況？によってＨＮを変えてますが、なんとゆーか、けじめのようなものです(ぉ\r\nコメント、評価等大歓迎でございます。お気軽にお声がけください（￣▽￣)ノ\r\n\r\nマイピクにつきましては、作品を投稿されている方に限らせていただいております。悪しからずご了承ください。\r\n（その代わりといってはなんですが、マイピク限定での投稿はしておりません）\r\n\r\n※オリキャラ(二次創作含む)については、基本的に『描いてもいいのよ』、というか『描いてほしいのよ』ということでお願いします。\r\n※なお、拙作の無断転載および改変はご遠慮ください。"
    )
    assert (
        result.profile_picture
        == "https://i.pximg.net/user-profile/img/2014/08/13/23/24/44/8259429_6f34e70e29290fdb5f0f8a66bc429203_170.jpg"
    )
    assert iterable_eq(
        result.links,
        {
            "http://www.lares.dti.ne.jp/~gaketsu",
            "https://pawoo.net/oauth_authentications/137796?provider=pixiv",
            "https://sketch.pixiv.net/@gaketsu_gk2",
            "https://twitter.com/gaketsu_gk2",
        },
    )
