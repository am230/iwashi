import pytest
from iwashi.visitor import Result
from iwashi.visitors.bandcamp import Bandcamp
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_bandcamp():
    visitor = Bandcamp()
    correct_result = Result(
        visitor=visitor,
        id="toxicholocaust",
        url="https://toxicholocaust.bandcamp.com",
        name="Toxic Holocaust",
        description="Toxic Thrash Metal\nEst. 1999",
        profile_picture="https://f4.bcbits.com/img/0032604396_21.jpg",
        links={"http://toxicholocaust.com"},
    )
    await _test(visitor, correct_result, "https://toxicholocaust.bandcamp.com")
