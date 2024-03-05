import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.youtube import Youtube


youtube = Youtube()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://www.youtube.com/@TomScottGo",
        "https://www.youtube.com/c/TomScottGo",
        "https://youtu.be/7DKv5H5Frt0",
        "https://www.youtube.com/watch?v=7DKv5H5Frt0",
    }:
        context = Context(session=session, url=url, visitor=visitor)
        assert (
            await youtube.normalize(context, url)
            == "https://www.youtube.com/@TomScottGo"
        )


@pytest.mark.asyncio
async def test_visit():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    url = "https://www.youtube.com/@TomScottGo"
    context = Context(session=session, url=url, visitor=visitor)
    await youtube.visit(url, context)
    result = context.result
    assert result
    assert result.url == url
    assert result.site_name == "YouTube"
    assert result.title == "Tom Scott"
    assert result.description is not None
    assert result.profile_picture is not None
    assert visitor.queue == ["https://www.tomscott.com/"]
