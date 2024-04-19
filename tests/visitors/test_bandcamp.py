import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.bandcamp import Bandcamp
from tests.visitors.test import iterable_eq


bandcamp = Bandcamp()


@pytest.mark.asyncio
async def test_normalize():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://thebuddysystemlabel.bandcamp.com/",
        "https://thebuddysystemlabel.bandcamp.com/track/zimlife",
    }:
        context = Context(session=session, visitor=visitor)
        assert await bandcamp.resolve_id(context, url) == "thebuddysystemlabel"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://thebuddysystemlabel.bandcamp.com"
    result = await bandcamp.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Bandcamp"
    assert result.title == "The Buddy System Project"
    assert result.description is not None
    assert result.profile_picture is not None
    assert len(result.links) == 0

    url = "https://toxicholocaust.bandcamp.com"
    result = await bandcamp.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Bandcamp"
    assert result.title == "Toxic Holocaust"
    assert result.description == "Toxic Thrash Metal\nEst. 1999"
    assert result.profile_picture == "https://f4.bcbits.com/img/0032604396_21.jpg"
    assert iterable_eq(result.links, {"http://toxicholocaust.com"})
