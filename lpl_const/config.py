#!/usr/bin/python
# -*- coding: utf-8 -*-
"""サーバー設定に関する設定場所"""
port: int = 8899
"""サーバーの起動ポート"""
mongo_host: str = 'mongo'
# mongo_host: str = 'localhost'

"""mongoのホスト名"""
mongo_port: str = 27017
"""mongoのポート番号"""
mongo_backup_path: str = ""
"""mongoのバックアップファイル出力先"""

channel_json_file_path: str = "/apps/channel_videos.json"
"""公式チャンネルのコンテンツ一覧ファイルのパス"""
