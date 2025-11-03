#!/usr/bin/env bash
# Renderビルドスクリプト

set -o errexit

# Pythonパッケージのインストール
pip install --upgrade pip
pip install -r requirements.txt

# FFmpegのインストール（Renderの環境に応じて）
# Renderは標準でffmpegをサポートしています
echo "FFmpeg should be available in Render's environment"

