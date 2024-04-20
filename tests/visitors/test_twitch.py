import pytest
from iwashi.visitors.twitch import Twitch
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_twitch():
    visitor = Twitch()
    correct = Result(
        visitor=visitor,
        id="thechief1114",
        url="https://www.twitch.tv/thechief1114",
        name="TheChief1114",
        description="I stream.",
        profile_picture="https://static-cdn.jtvnw.net/jtv_user_pictures/7a7f1681-f8ea-424d-bbce-38cac15e3328-profile_image-300x300.png",
        links={"https://twitter.com/The_Chief1114"},
    )
    await _test(visitor, correct, "https://www.twitch.tv/thechief1114")
