import pytest
from iwashi.visitors.mirrativ import Mirrativ
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_mirrativ():
    visitor = Mirrativ()
    correct = Result(
        visitor=visitor,
        id="61244",
        url="https://www.mirrativ.com/user/61244",
        name="オトメくん！",
        description="✨経営&インフルエンサー&投資✨",
        profile_picture="https://cdn.mirrativ.com/mirrorman-prod/image/profile_image/89aff406cd34ceb016d854536a189467ced65a54cdd88af4e671b9baa28ffbdf_m.jpeg?1710995124",
        links={"https://youtube.com/channel/UCymZH1hDOLGeyCLLf2SSy3A"},
    )
    await _test(visitor, correct, "https://www.mirrativ.com/user/61244")
