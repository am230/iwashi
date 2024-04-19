import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.youtube import Youtube
from tests.visitors.test import iterable_eq


youtube = Youtube()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://www.youtube.com/@TomScottGo",
        "https://www.youtube.com/@TomScottGo/community",
        "https://www.youtube.com/c/TomScottGo",
        "https://www.youtube.com/c/TomScottGo/community",
        "https://youtu.be/7DKv5H5Frt0",
        "https://www.youtube.com/watch?v=7DKv5H5Frt0",
    }:
        context = Context(session=session, visitor=visitor)
        assert await youtube.resolve_id(context, url) == "TomScottGo"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.youtube.com/@TomScottGo"
    result = await youtube.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "YouTube"
    assert result.title == "Tom Scott"
    assert result.description is not None
    assert result.profile_picture is not None
    # assert result.links == {"https://www.tomscott.com/"}
    assert iterable_eq(result.links, {"https://www.tomscott.com/"})
