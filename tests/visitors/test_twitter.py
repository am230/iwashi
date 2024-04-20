import pytest
from iwashi.visitors.twitter import Twitter
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_twitter():
    visitor = Twitter()
    correct = Result(
        visitor=visitor,
        id="VALIGHT1",
        url="https://twitter.com/VALIGHT1",
        name="VALIGHT_YT",
        description="Hi, I'm Valight, a creative Fortnite mappeur\nWelcome to my twiter account.\nCODE VALIGHT",
        profile_picture="https://pbs.twimg.com/profile_images/1512100269831639049/R4AjwP-9_normal.jpg",
        links={"https://youtube.com/channel/UCDRIfKm06-e1dwSbnU1H9Rw"},
    )
    await _test(visitor, correct, "https://twitter.com/VALIGHT1")
