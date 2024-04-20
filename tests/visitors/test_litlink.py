import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.litlink import LitLink
from tests.visitors.test import iterable_eq


litlink = LitLink()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://lit.link/leftpory5n",
    }:
        context = Context(session=session, visitor=visitor)
        assert await litlink.resolve_id(context, url) == "leftpory5n"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://lit.link/leftpory5n"
    result = await litlink.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "LitLink"
    assert result.title == "左ポリ５ン"
    assert result.description == "ひだりぽりごんと読みます。"
    assert (
        result.profile_picture
        == "https://prd.storage.lit.link/images/creators/3f1f9feb-8603-46ff-a038-b2a29021beaa/687f1d68-9516-4e61-b38f-7a4377657687.png"
    )
    assert iterable_eq(
        result.links,
        {
            "https://skeb.jp/@leftpory5n",
            "https://twitter.com/leftpory5n",
            "https://giftee.com/u/odenpo",
            "https://odaibako.net/u/leftpory5n",
            "https://www.pixiv.net/users/259841",
        },
    )
