import pytest
from iwashi.service.tiktok import TikTok
from iwashi.visitor import Result
from tests.service_tester import service_test


@pytest.mark.asyncio
async def test_tiktok():
    service = TikTok()
    correct = Result(
        service=service,
        id="cocoyola",
        url="https://www.tiktok.com/@cocoyola",
        name="☀️🥂🫶🏻⭐️🍸",
        description="🪸🌅🥂🫶🏻🍸",
        profile_picture=".tiktokcdn.com/tos-maliva-avt-0068/7325124622654341126~c5_1080x1080.jpeg",
        links=set(),
    )
    await service_test(
        service,
        correct,
        "https://www.tiktok.com/@cocoyola?lang=ja-JP",
        "https://www.tiktok.com/@cocoyola/video/7234867719043157274?lang=ja-JP",
    )
