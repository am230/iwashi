import pytest


@pytest.mark.asyncio
async def test_tree():
    import iwashi

    result = await iwashi.tree("http://youtube.com/@OMUAPPS")
    assert result
    assert result.children
    assert result.screen_id == "OMUAPPS"
    assert result.unique_id == "UCdKQmSjz0fxFpjXoaeMyArw"
    assert len(result.children) == 1
    child = result.children[0]
    assert child.id == "omuapps"


@pytest.mark.asyncio
async def test_visit():
    import iwashi

    result = await iwashi.visit("http://youtube.com/@OMUAPPS")
    assert result
    assert not result.children
    assert result.screen_id == "OMUAPPS"
    assert result.unique_id == "UCdKQmSjz0fxFpjXoaeMyArw"
    assert len(result.children) == 0
