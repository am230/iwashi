import pytest
from iwashi.visitors.tiktok import TikTok
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_tiktok():
    visitor = TikTok()
    correct = Result(
        visitor=visitor,
        id="cocoyola",
        url="https://www.tiktok.com/@cocoyola",
        name="☀️🥂🫶🏻⭐️🍸",
        description="-everything you’re looking for and more-\n\n🪸🌅🥂🫶🏻🍸",
        profile_picture=".tiktokcdn.com/tos-maliva-avt-0068/7325124622654341126~c5_1080x1080.jpeg",
        links=set(),
    )
    await _test(
        visitor,
        correct,
        "https://www.tiktok.com/@cocoyola?lang=ja-JP",
        "https://www.tiktok.com/@cocoyola/video/7234867719043157274?lang=ja-JP",
    )
