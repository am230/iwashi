import aiohttp
import pytest
from iwashi.visitor import Context, FakeVisitor
from iwashi.visitors.spotify import Spotify
from tests.visitors.test import iterable_eq


spotify = Spotify()


@pytest.mark.asyncio
async def test():
    visitor = FakeVisitor()
    session = aiohttp.ClientSession()

    for url in {
        "https://open.spotify.com/artist/0CLW5934vy2XusynS1px1S",
        "https://open.spotify.com/intl-ja/artist/0CLW5934vy2XusynS1px1S",
    }:
        context = Context(session=session, visitor=visitor)
        assert await spotify.resolve_id(context, url) == "0CLW5934vy2XusynS1px1S"


@pytest.mark.asyncio
async def test_visit():
    session = aiohttp.ClientSession()

    url = "https://open.spotify.com/artist/0CLW5934vy2XusynS1px1S"
    result = await spotify.visit_url(session, url)
    assert result
    assert result.url == url
    assert result.site_name == "Spotify"
    assert result.title == "Flyana Boss"
    assert (
        result.description
        == "Two besties, one duo! Reporting to you live from LA.\nTEXT US (310) 742-0879 &#x1f643;"
    )
    assert (
        result.profile_picture
        == "https://i.scdn.co/image/ab6761610000e5ebcd0271f5501c3e4064d0f6ec"
    )
    assert iterable_eq(
        result.links,
        {
            "https://facebook.com/Flyanaboss-1100179700191258",
            "https://instagram.com/flyanaboss",
        },
    )
