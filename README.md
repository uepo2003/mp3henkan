# YouTube to MP3 変換ツール

yt-dlpを使用してYouTube動画からMP3音声ファイルを抽出するPythonスクリプトです。

## 必要なもの

- Python 3.7以上
- FFmpeg（音声変換に必要）

## インストール

### 1. 仮想環境のセットアップ（推奨）

プロジェクト専用の仮想環境を作成することをお勧めします。

#### 仮想環境の作成と有効化

**macOS/Linux:**
```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate
```

**Windows:**
```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
venv\Scripts\activate
```

仮想環境を有効化すると、プロンプトの先頭に `(venv)` が表示されます。

仮想環境を終了するには:
```bash
deactivate
```

### 2. FFmpegのインストール

#### macOS (Homebrew使用)
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
[FFmpeg公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストール

### 3. Pythonパッケージのインストール

⚠️ **重要**: 仮想環境を有効化した状態で以下のコマンドを実行してください。

```bash
pip install -r requirements.txt
```

または

```bash
pip install yt-dlp
```

## 使い方

⚠️ **重要**: スクリプトを実行する前に、必ず仮想環境を有効化してください。

```bash
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 基本的な使い方

```bash
python youtube_to_mp3.py <YouTube URL>
```

例:
```bash
python youtube_to_mp3.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 出力先を指定する

```bash
python youtube_to_mp3.py <YouTube URL> <出力ディレクトリ>
```

例:
```bash
python youtube_to_mp3.py https://www.youtube.com/watch?v=dQw4w9WgXcQ my_music
```

## 出力形式

- **形式**: MP3
- **ビットレート**: 192kbps
- **ファイル名**: 動画のタイトル.mp3
- **デフォルト保存先**: `downloads/`ディレクトリ

## 機能

- ✅ YouTube動画から音声のみを抽出
- ✅ 高品質MP3変換（192kbps）
- ✅ 動画情報の表示（タイトル、長さ）
- ✅ 進捗状況の表示
- ✅ エラーハンドリング
- ✅ カスタム出力ディレクトリ対応

## トラブルシューティング

### FFmpegがインストールされていない場合

以下のエラーが表示される場合は、FFmpegをインストールしてください:
```
ERROR: ffmpeg not found
```

### ダウンロードできない場合

- URLが正しいか確認してください
- インターネット接続を確認してください
- 動画が削除されていないか確認してください
- yt-dlpを最新版にアップデートしてください:
  ```bash
  pip install --upgrade yt-dlp
  ```

## ライセンス

このスクリプトは教育目的で作成されています。ダウンロードする動画の著作権を尊重し、適切に使用してください。

