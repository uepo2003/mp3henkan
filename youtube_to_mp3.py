#!/usr/bin/env python3
"""
YouTube動画からMP3音声を抽出するスクリプト
yt-dlpを使用して高品質な音声ファイルをダウンロードします
"""

import sys
import os
from pathlib import Path
import yt_dlp


def download_youtube_to_mp3(url: str, output_dir: str = "downloads") -> None:
    """
    YouTube動画のURLからMP3ファイルをダウンロードする
    
    Args:
        url: YouTubeの動画URL
        output_dir: 出力先ディレクトリ（デフォルト: downloads）
    """
    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # yt-dlpのオプション設定
    ydl_opts = {
        'format': 'bestaudio/best',  # 最高品質の音声を選択
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # FFmpegで音声を抽出
            'preferredcodec': 'mp3',       # MP3形式に変換
            'preferredquality': '192',     # ビットレート192kbps
        }],
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),  # 出力ファイル名のテンプレート
        'quiet': False,  # ダウンロード情報を表示
        'no_warnings': False,
        'noplaylist': True,  # プレイリストを無視して単一の動画のみダウンロード
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],  # AndroidとWebクライアントを使用（より安定）
                'skip': ['hls', 'dash']  # HLSとDASHをスキップ
            }
        },
    }
    
    try:
        print(f"ダウンロード中: {url}")
        print(f"出力先: {output_path.absolute()}")
        print("-" * 60)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 動画情報を取得
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"タイトル: {video_title}")
            print(f"長さ: {duration // 60}分{duration % 60}秒")
            print("-" * 60)
            
            # ダウンロード実行
            ydl.download([url])
            
        print("-" * 60)
        print(f"✓ ダウンロード完了!")
        print(f"保存先: {output_path.absolute()}")
        
    except yt_dlp.utils.DownloadError as e:
        print(f"エラー: ダウンロードに失敗しました - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: 予期しないエラーが発生しました - {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python youtube_to_mp3.py <YouTube URL> [出力ディレクトリ]")
        print("\n例:")
        print("  python youtube_to_mp3.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("  python youtube_to_mp3.py https://www.youtube.com/watch?v=dQw4w9WgXcQ my_music")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    
    download_youtube_to_mp3(url, output_dir)


if __name__ == "__main__":
    main()

