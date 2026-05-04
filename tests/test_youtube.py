import pytest
from iwashi.service.youtube import Youtube
from iwashi.visitor import Result
from tests.service_tester import service_test


@pytest.mark.asyncio
async def test_youtube():
    service = Youtube()
    correct = Result(
        service=service,
        id="UC4QobU6STFB0P71PMvOGN5A",
        unique_id="UC4QobU6STFB0P71PMvOGN5A",
        screen_id="jawed",
        url="https://www.youtube.com/channel/UC4QobU6STFB0P71PMvOGN5A",
        name="jawed",
        description="",
        profile_picture="https://yt3.googleusercontent.com/uI3VE4PVqvCy0xnWLqMJnEzyBUm3T8VHOCp4ee-1RxdHqKXCdUE_qXYQnpf9AfuEoIPactVyDhM=s900-c-k-c0x00ffffff-no-rj",
        links=set(),
    )

    await service_test(
        service,
        correct,
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "https://www.youtube.com/@jawed/videos",
    )

    correct = Result(
        service=service,
        id="UCwYlcr-s1mr4FPzDxUMN9Vg",
        unique_id="UCwYlcr-s1mr4FPzDxUMN9Vg",
        screen_id="aoikuru_V",
        url="https://www.youtube.com/channel/UCwYlcr-s1mr4FPzDxUMN9Vg",
        name="あおいくる",
        description="ポテト好きの狼系VTuber 🍟🍟 紺碧 紅琉(あおい くる)と申します！！ ゲーム(基本FPS)とかアニメとか色々好きです！！",
        profile_picture="https://yt3.googleusercontent.com/WnyUeD2enKopNvf3s-oy_DSXTS76WjkDM7EcZlpqaxL2TW3J4GWvFlmWe3Y9ZBE5ln45SoN4Xw=s900-c-k-c0x00ffffff-no-rj",
        links={
            "https://www.twitch.tv/aoikuru_v",
            "https://twitter.com/aoikuru_V",
        },
    )
    await service_test(
        service,
        correct,
        "https://www.youtube.com/live/IJCdnYoILFA",
    )

    correct = Result(
        service=service,
        id="UCNkU0frQxqDUWYzDENP0Bzg",
        unique_id="UCNkU0frQxqDUWYzDENP0Bzg",
        screen_id="RomoloDisconzi",
        url="https://www.youtube.com/channel/UCNkU0frQxqDUWYzDENP0Bzg",
        name="Romolo Disconzi",
        description="Stream de Axie Infinity, comentários sobre criptoativos e análise de times.\n",
        profile_picture="https://yt3.googleusercontent.com/ERS1lb8FGu_dIxhUF0YLFZjhsSj6TSAcJEKXVr6GbOT04RQIMXout-3NYOpYjtQcLpzRjR5shg=s900-c-k-c0x00ffffff-no-rj",
        links=set(),
    )
    await service_test(
        service,
        correct,
        "https://www.youtube.com/user/DisconziRomolo",
    )
