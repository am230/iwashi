import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.sketch import Sketch
from tests.visitors.test import iterable_eq


sketch = Sketch()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://sketch.pixiv.net/@par1y"}:
        context = Context(session=session, visitor=visitor)
        assert await sketch.resolve_id(context, url) == "par1y"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://sketch.pixiv.net/@par1y"
    result = await sketch.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Pixiv Sketch"
    assert result.title == "Paryi"
    assert (
        result.description
        == "お勉強と落書きがメイン\nフォロワーさんとまったり絡みたい\nhttps://twitter.com/par1y\n"
    )
    assert (
        result.profile_picture
        == "https://img-sketch.pixiv.net/uploads/user_icon/file/1980676/5116648097160323811.jpg"
    )
    assert iterable_eq(
        result.links,
        {"https://twitter.com/par1y", "https://www.pixiv.net/users/par1y"},
    )
