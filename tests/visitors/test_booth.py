import pytest
from iwashi.visitor import Result
from iwashi.visitors.booth import Booth
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_booth():
    visitor = Booth()
    correct_result = Result(
        visitor=visitor,
        id="miluda",
        url="https://miluda.booth.pm",
        name="Sunshine Mill 太陽光工場",
        description="Welcome to 太陽光工場.\r\nMiludaと申します。同人初心者アメリカ人ですけどどうぞよろしくお願いします。メインは東方や艦これです。\r\n\r\nよろしくお願いします！",
        profile_picture="https://booth.pximg.net/c/128x128/users/274/icon_image/41f84dbd-19af-49b9-8cf5-888eb389e500_base_resized.jpg",
        links={
            "https://miluda.com",
            "https://twitter.com/Miluda",
            "https://www.pixiv.net/users/161480",
        },
    )
    await _test(
        visitor,
        correct_result,
        "https://miluda.booth.pm/",
        "https://miluda.booth.pm/items/397",
    )
