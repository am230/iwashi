import pytest
from iwashi.service.youtube import Youtube
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_youtube():
    service = Youtube()
    correct = Result(
        service=service,
        id="二みかげ",
        url="https://www.youtube.com/@二みかげ",
        name="二みかげ",
        description="VTuberの二と書いて『したなが』、二みかげです！\nFPSからホラー(強制)を中心に配信してます。\nお喋り大好き、月曜日は定期雑談配信\n\n■メインゲーム\nAPEX\u3000-\u3000参加型・カジュアル・ランク\u3000-\nプレゼントされしまったホラーゲーム\n龍が如く(現在停滞中)\n\n■好きなこと\n自作PC、ゲーミングデバイス、アニメ(特に主人公最強系)\n\n▼現在の自作PCスペック\nCPU intelCorei9-12900KF\nGPU NVIDIAGeForce RTX3070\nマザーボード TUFGAMINGZ690\n\n\n▽Vモデルお母さん\u3000一雀様\nX(旧Twitter) https://twitter.com/chunx2_v\nYouTube https://www.youtube.com/channel/@ninomae_suzume \n\n",
        profile_picture="https://yt3.googleusercontent.com/TyUENjbq-ea9k-6FpR11gOuSpUe7LjO_LL2uxH6S7z9DkiyrOp_QerFchciqF2NkJbSKqMi-=s900-c-k-c0x00ffffff-no-rj",
        links={
            "https://www.amazon.jp/hz/wishlist/ls/13E56V4KYMVXR?ref_=wl_share",
            "https://twitter.com/Sitanaga_Mikage",
        },
    )

    await _test_service(
        service,
        correct,
        "https://youtu.be/LnbSAhgwipA",
        "https://youtube.com/@二みかげ",
    )

    correct = Result(
        service=service,
        id="aoikuru_V",
        url="https://www.youtube.com/@aoikuru_V",
        name="あおいくる",
        description="ポテト好きの狼系VTuber 🍟🍟 紺碧 紅琉(あおい くる)と申します！！ ゲーム(基本FPS)とかアニメとか色々好きです！！",
        profile_picture="https://yt3.googleusercontent.com/WnyUeD2enKopNvf3s-oy_DSXTS76WjkDM7EcZlpqaxL2TW3J4GWvFlmWe3Y9ZBE5ln45SoN4Xw=s900-c-k-c0x00ffffff-no-rj",
        links={
            "https://www.twitch.tv/aoikuru_v",
            "https://twitter.com/aoikuru_V",
        },
    )
    await _test_service(
        service,
        correct,
        "https://www.youtube.com/live/IJCdnYoILFA",
    )