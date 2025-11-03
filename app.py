#!/usr/bin/env python3
"""
YouTube MP3ダウンロードAPIサーバー
RenderにデプロイしてURLを叩くだけでMP3をダウンロードできるサービス
"""

import os
import tempfile
import shutil
from pathlib import Path
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import yt_dlp

app = Flask(__name__)

# 環境変数からポート番号を取得（Renderではこれが設定される）
PORT = int(os.environ.get('PORT', 10000))


def download_youtube_to_mp3(url: str, output_dir: str) -> tuple[str, str]:
    """
    YouTube動画のURLからMP3ファイルをダウンロードする
    
    Args:
        url: YouTubeの動画URL
        output_dir: 出力先ディレクトリ
        
    Returns:
        (ファイルパス, ファイル名)のタプル
    """
    # yt-dlpのオプション設定
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['hls', 'dash']
            }
        },
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 動画情報を取得
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', 'Unknown')
        
        # ダウンロード実行
        ydl.download([url])
        
        # 生成されたファイル名を特定
        safe_title = secure_filename(video_title)
        mp3_filename = f"{video_title}.mp3"
        mp3_path = os.path.join(output_dir, mp3_filename)
        
        return mp3_path, mp3_filename


@app.route('/')
def index():
    """ホームページ - 使い方を表示"""
    return jsonify({
        'service': 'YouTube to MP3 Converter',
        'version': '1.0',
        'usage': {
            'endpoint': '/download',
            'method': 'GET',
            'parameter': 'url (YouTube video URL)',
            'example': f'{request.url_root}download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        },
        'note': 'MP3ファイルはリクエストごとに生成され、ダウンロード後は自動的に削除されます。'
    })


@app.route('/download')
def download():
    """YouTube動画をMP3に変換してダウンロード"""
    # URLパラメータを取得
    youtube_url = request.args.get('url')
    
    if not youtube_url:
        return jsonify({
            'error': 'URLパラメータが必要です',
            'example': f'{request.url_root}download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }), 400
    
    # 一時ディレクトリを作成
    temp_dir = tempfile.mkdtemp()
    
    try:
        # YouTubeからMP3をダウンロード
        mp3_path, mp3_filename = download_youtube_to_mp3(youtube_url, temp_dir)
        
        # ファイルが存在するか確認
        if not os.path.exists(mp3_path):
            return jsonify({
                'error': 'ファイルの生成に失敗しました'
            }), 500
        
        # ファイルを送信（送信後に自動削除）
        return send_file(
            mp3_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=mp3_filename
        )
        
    except yt_dlp.utils.DownloadError as e:
        return jsonify({
            'error': 'ダウンロードエラー',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'error': '予期しないエラーが発生しました',
            'message': str(e)
        }), 500
        
    finally:
        # 一時ディレクトリをクリーンアップ（少し遅延させる）
        # send_fileが完了してからクリーンアップ
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass


@app.route('/health')
def health():
    """ヘルスチェックエンドポイント"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # ローカル開発用
    app.run(host='0.0.0.0', port=PORT, debug=False)

