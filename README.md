# iwashi

プロフィールの取得を一つのライブラリで可能にします。

## インストール

```bash
pip install iwashi
```

## 使用例

### CLI

```bash
python -m iwashi https://example.com/profile
```

### Python API

```python
import asyncio
from iwashi import tree

result = asyncio.run(tree("https://example.com/profile"))
print(result)
```

## サポートサービス(2026年5月4日)

| サービス      | テスト |
| ------------- | ------ |
| Bandcamp      | ✅      |
| Booth         | ❌      |
| Fanbox        | ✅      |
| Github        | ✅      |
| Instagram     | ✅      |
| Itchio        | ✅      |
| Kofi          | ✅      |
| Linktree      | ❌      |
| LitLink       | ❌      |
| MarshmallowQA | ❌      |
| Mirrativ      | ❌      |
| Nicovideo     | ❌      |
| Note          | ❌      |
| Patreon       | ❌      |
| Picarto       | ✅      |
| Pixiv         | ❌      |
| Reddit        | ❌      |
| Skeb          | ❌      |
| Sketch        | ✅      |
| Soundcloud    | ✅      |
| Spotify       | ❌      |
| TikTok        | ❌      |
| Twitch        | ✅      |
| TwitCasting   | ❌      |
| X (Twitter)   | ❌      |
| Youtube       | ✅      |
