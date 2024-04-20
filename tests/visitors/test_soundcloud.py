import pytest
from iwashi.visitors.soundcloud import Soundcloud
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_soundcloud():
    visitor = Soundcloud()
    correct = Result(
        visitor=visitor,
        id="speder2",
        url="https://soundcloud.com/speder2",
        name="Speder2",
        description="ゲーム製作サークルの音楽・SEを担当しています",
        profile_picture="https://i1.sndcdn.com/avatars-000125467778-jpowym-large.jpg",
        links={
            "http://kohada.ushimairi.com/",
        },
    )
    await _test(
        visitor,
        correct,
        "https://soundcloud.com/speder2",
        "https://soundcloud.com/speder2/tracks",
    )
