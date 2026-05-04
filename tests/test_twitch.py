import pytest
from iwashi.service.twitch import Twitch
from iwashi.visitor import Result
from tests.service_tester import service_test


@pytest.mark.asyncio
async def test_twitch():
    service = Twitch()
    correct = Result(
        service=service,
        id="venzogames",
        url="https://www.twitch.tv/venzogames",
        name="venzogames",
        description="As melhores dicas de Fortnite do YouTube Brasileiro!",
        profile_picture="https://static-cdn.jtvnw.net/jtv_user_pictures/bf1acd78-493e-4b49-8a4f-7ad51c473881-profile_image-300x300.png",
        links={
            "https://www.youtube.com/user/DisconziRomolo",
            "https://www.youtube.com/c/CryptoGamersBrasil",
            "https://www.youtube.com/c/CarlosHung/featured",
        },
    )
    await service_test(service, correct, "https://www.twitch.tv/venzogames/about")
