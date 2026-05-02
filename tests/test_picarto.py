import pytest
from iwashi.visitor import Result
from iwashi.service.picarto import Picarto
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_picarto():
    service = Picarto()
    correct = Result(
        service=service,
        id="1300",
        url="https://picarto.tv/RaptorARTStudios",
        name="RaptorARTStudios",
        description="Drawer of sexy anthro pinups, \nand i make custom adopts for sell as well!  \nCommissions are generally always open,",
        profile_picture="https://images.picarto.tv/ptvimages/1/13/1300/avatars/ceb80e7a54bf53cc08e1f117.png",
        links={
            "http://raptor007.deviantart.com/",
            "https://www.patreon.com/RaptorARTStudios",
            "http://raptor007.tumblr.com/",
            "https://toyhou.se/RaptorartStudios",
            "https://twitter.com/RaptorARTStudio",
            "http://www.furaffinity.net/user/raptorart/",
            "https://www.facebook.com/RaptorArtStudios/?ref=bookmarks",
        },
    )
    await _test_service(
        service,
        correct,
        "https://picarto.tv/RaptorARTStudios",
    )
