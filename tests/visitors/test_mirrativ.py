import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.mirrativ import Mirrativ
from tests.visitors.test import iterable_eq


mirrativ = Mirrativ()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {"https://www.mirrativ.com/user/61244"}:
        context = Context(session=session, visitor=visitor)
        assert await mirrativ.resolve_id(context, url) == "61244"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.mirrativ.com/user/61244"
    result = await mirrativ.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Mirrativ"
    assert result.title == "オトメくん！"
    assert result.description == "✨経営&インフルエンサー&投資✨"
    assert (
        result.profile_picture
        == "https://cdn.mirrativ.com/mirrorman-prod/image/profile_image/89aff406cd34ceb016d854536a189467ced65a54cdd88af4e671b9baa28ffbdf_m.jpeg?1710995124"
    )
    assert iterable_eq(
        result.links,
        {"https://youtube.com/channel/UCymZH1hDOLGeyCLLf2SSy3A"},
    )
