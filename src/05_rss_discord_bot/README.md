# RSS Discord Bot

指定したRSSフィード（ニュースサイトやブログ）を24時間監視し、更新があったらDiscordに通知するBotです。
**このツールは「常駐型」です。PCを閉じても動き続ける必要があります。**

## ⚠️ なぜ自宅PCではダメなのか？
このBotは「常に新しい情報を待ち構える」必要があります。
自宅のノートPCで動かした場合：
1. **スリープモードで止まる**: 夜間や外出中にPCがスリープすると、その間のニュースを逃します。
2. **電気代と排熱**: 24時間つけっぱなしはPCの寿命を縮めます。

👉 **解決策: VPS (Virtual Private Server)**
月額数百円のVPS（Xserver VPSなど）を使えば、クラウド上で24時間365日、あなたの代わりに監視を続けてくれます。

## インストール
```bash
pip install -r requirements.txt
```

## 使い方
VPS上のターミナルで以下を実行します。

```bash
python bot.py --webhook "YOUR_DISCORD_WEBHOOK_URL"
```

### バックグラウンド実行（推奨）
ターミナルを閉じても実行し続けるには `nohup` を使います。

```bash
nohup python bot.py --webhook "YOUR_DISCORD_WEBHOOK_URL" &
```
これで、あなたが寝ている間もBotは働き続けます。

## オプション
- `--feed`: 監視するRSSのURL (デフォルト: YahooニュースIT)
- `--interval`: チェック間隔（分） (デフォルト: 10分)
