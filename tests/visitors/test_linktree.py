import pytest
from iwashi.visitors.linktree import Linktree
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_linktree():
    visitor = Linktree()
    correct = Result(
        visitor=visitor,
        id="fantomtracks",
        url="https://linktr.ee/fantomtracks",
        name=None,
        description="Musicien\n📍Paris\n🎸Bassist\n🎥 Youtube cover maker",
        profile_picture="https://ugc.production.linktr.ee/7b4zQfDkSBibTW1vIctw_94n3QLNB7T5fPi02",
        links={
            "https://www.instagram.com/fantomtracks/",
            "https://www.youtube.com/channel/UCOztO-bJFzphFxOUh7K01eg?sub_confirmation=1",
            "https://twitter.com/fantomtracks",
        },
    )
    await _test(visitor, correct, "https://linktr.ee/fantomtracks")
