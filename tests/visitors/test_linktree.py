import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.linktree import Linktree
from tests.visitors.test import iterable_eq


linktree = Linktree()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://linktr.ee/fantomtracks/",
    }:
        context = Context(session=session, visitor=visitor)
        assert await linktree.resolve_id(context, url) == "fantomtracks"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://linktr.ee/fantomtracks"
    result = await linktree.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Linktree"
    assert result.title is None
    assert result.description == "Musicien\n📍Paris\n🎸Bassist\n🎥 Youtube cover maker"
    assert (
        result.profile_picture
        == "https://ugc.production.linktr.ee/7b4zQfDkSBibTW1vIctw_94n3QLNB7T5fPi02"
    )
    assert iterable_eq(
        result.links,
        {
            "https://www.instagram.com/fantomtracks/",
            "https://www.youtube.com/channel/UCOztO-bJFzphFxOUh7K01eg?sub_confirmation=1",
            "https://twitter.com/fantomtracks",
        },
    )
