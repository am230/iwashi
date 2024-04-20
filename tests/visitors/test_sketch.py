import pytest
from iwashi.visitors.sketch import Sketch
from iwashi.visitor import Result
from tests.visitors.test import _test


@pytest.mark.asyncio
async def test_sketch():
    visitor = Sketch()
    correct = Result(
        visitor=visitor,
        id="par1y",
        url="https://sketch.pixiv.net/@par1y",
        name="Paryi",
        description="お勉強と落書きがメイン\nフォロワーさんとまったり絡みたい\nhttps://twitter.com/par1y\n",
        profile_picture="https://img-sketch.pixiv.net/uploads/user_icon/file/1980676/5116648097160323811.jpg",
        links={"https://twitter.com/par1y", "https://www.pixiv.net/users/par1y"},
    )
    await _test(visitor, correct, "https://sketch.pixiv.net/@par1y")
