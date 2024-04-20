import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.note import Note
from tests.visitors.test import iterable_eq


note = Note()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://note.com/pocketpair"}:
        context = Context(session=session, visitor=visitor)
        assert await note.resolve_id(context, url) == "pocketpair"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://note.com/pocketpair"
    result = await note.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Note"
    assert result.title == "ポケットペア"
    assert result.description == "最高のゲームを作っています"
    assert (
        result.profile_picture
        == "https://assets.st-note.com/production/uploads/images/127793817/profile_28ad4f05e11a0fc2d9117a7e530bc6bf.jpg?fit=bounds&format=jpeg&quality=85&width=330"
    )
    assert iterable_eq(
        result.links,
        {"https://twitter.com/Palworld_JP"},
    )
