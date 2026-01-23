# YouTube Transcriber

YouTube動画の字幕（書き起こし）を自動で取得し、テキストファイルとして保存するツールです。
会議の議事録作成や、動画の内容をテキストでサクッと確認したい時に便利です。

## 必要要件
- Python 3.x
- `youtube-transcript-api`

## インストール
```bash
pip install -r requirements.txt
```

## 使い方
動画のURL、またはIDを渡すだけです。

```bash
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

実行すると、カレントディレクトリに `transcript_dQw4w9WgXcQ.txt` が生成されます。

### オプション
- `--lang`: 言語コードを指定します（デフォルト: `ja`）。英語の動画なら `--lang en` としてください。
