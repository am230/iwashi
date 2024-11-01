import pytest
from iwashi.service.skeb import Skeb
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_skeb():
    service = Skeb()
    correct = Result(
        service=service,
        id="bet_neb",
        url="https://skeb.jp/@bet_neb",
        name="ベトベト",
        description="重度の足フェチと匂いフェチ \n【skeb】https://skeb.jp/@bet_neb \n【fanbox】https://betbet.fanbox.cc/",
        profile_picture="https://pbs.twimg.com/profile_images/1829489713310224385/5hgzLi7Y.jpg",
        links={
            "https://betbet.fanbox.cc",
            "https://www.pixiv.net/member.php?id=85335130",
            "https://twitter.com/bet_neb",
        },
    )
    await _test_service(
        service,
        correct,
        "https://skeb.jp/@bet_neb",
    )
