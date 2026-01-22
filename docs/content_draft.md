# 【随時更新】コピペで使える業務効率化Pythonスクリプト全集

*Last Updated: 2026/01/22 (Tool #03 Added)*

こんにちわ。
「退屈な作業はすべてPythonにやらせる」をモットーに、日々自動化スクリプトを書き溜めています。

このnoteでは、私がGitHubで公開している**「実戦で使える自動化コード」**を日本語で丁寧に解説・紹介していきます。

ソースコードは全て無料で公開しています。
👉 **[GitHub Repository: Awesome-Business-Automation-Python](https://github.com/maco1031/Awesome-Business-Automation-Python)**

---

## ⚠️ 実行環境について（重要）

紹介するスクリプトは非常に強力ですが、自宅のPCで24時間稼働させると**「WebサイトからのIPブロック」**や**「PCのスリープによる停止」**のリスクがあります。

ビジネスとして安定稼働させる場合、月額数百円で使える**VPS（仮想専用サーバー）**の利用を強く推奨します。
私は以下の環境で動作確認をしています。

*   **Xserver VPS**: [こちらは最強スペック](https://px.a8.net/svt/ejp?a8mat=4AVB46+81COS2+CO4+25ES2Q) (推奨)
*   **ConoHa VPS**: [公式サイト](https://www.conoha.jp/vps/) (初心者向け)

---

## 📁 収録ツール一覧

### 01. Google Maps Leads Scraper
指定した「場所」と「キーワード（例：カフェ）」から、店舗名・住所・電話番号を自動収集し、リスト化（Excel保存）するツールです。

*   **活用例**: 営業リスト作成、競合調査
*   **使い方**: `python src/01_google_maps_leads/scraper.py`
    *キーワードとエリアを入力するだけで、Chromeが自動で立ち上がり収集を開始します。*

### 02. Text-to-Video Generator
テキストを入力するだけで、SNS（YouTube Shorts / Pinterest）用の動画を自動生成するツールです。Remotionエンジンを使用しています。

*   **活用例**: ニュースの動画化、名言bot運用
*   **使い方**: `python src/02_text_to_video/generator.py`
    *Pinterest用の縦長動画(9:16)にも対応しました！*

---

### 03. Instagram Auto Liker
指定したハッシュタグの投稿を自動で「いいね」していくツールです。Seleniumを使ってブラウザを自動操作します。

*   **活用例**: アカウントの認知拡大、フォロワー増加
*   **使い方**: `python src/03_instagram_auto_like/auto_like.py --username "user" --password "pass" --hashtag "python"`
    *BAN対策として、ランダムな待機時間を設けています。*

---

*(以下、更新のたびに新しいツールを追記していきます)*
