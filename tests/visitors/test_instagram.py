import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.instagram import Instagram
from tests.visitors.test import iterable_eq


instagram = Instagram()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://www.instagram.com/ismsx_/",
    }:
        context = Context(session=session, visitor=visitor)
        assert await instagram.resolve_id(context, url) == "ismsx_"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://www.instagram.com/ismsx_"
    result = await instagram.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Instagram"
    assert result.title == "いっしん"
    assert result.description == "Isshin Tanaka\nmotion designer / visual artist"
    assert (
        result.profile_picture
        == "https://scontent-nrt1-2.cdninstagram.com/v/t51.2885-19/252132732_925276874749701_2338460024889750642_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-nrt1-2.cdninstagram.com&_nc_cat=109&_nc_ohc=9zhwfo0l1JUAb4kjQ9-&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AfDFhH0vtf75VqtZ6MXSNkczWc-WMtJzVm9xxF2rIrbN8Q&oe=66293E40&_nc_sid=8b3546"
    )
    assert iterable_eq(
        result.links,
        {"https://ismsx.jp/"},
    )
