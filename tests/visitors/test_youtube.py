import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.youtube import Youtube


youtube = Youtube()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()
    context = Context(
        session=session, url="https://www.youtube.com/@TomScottGo", visitor=visitor
    )
    assert (
        await youtube.normalize(context, "https://www.youtube.com/@TomScottGo")
        == "https://www.youtube.com/@TomScottGo"
    )
    assert (
        await youtube.normalize(context, "https://www.youtube.com/c/TomScottGo")
        == "https://www.youtube.com/@TomScottGo"
    )
    assert (
        await youtube.normalize(
            context, "https://www.youtube.com/channel/UCBa659QWEk1AI4Tg--mrJ2A"
        )
        == "https://www.youtube.com/@TomScottGo"
    )
