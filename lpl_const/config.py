#!/usr/bin/python
# -*- coding: utf-8 -*-
# サーバー設定に関する設定場所
SERVER_PORT: int = 8899
"""サーバーの起動ポート"""

# mongodbに関する設定場所
MONGO_HOST: str = 'mongo'
"""mongoのホスト名。基本的に変更は必要ありません。"""
MONGO_PORT: str = 27017
"""mongoのポート番号。基本的に変更は必要ありません。"""

# youtubeの情報に関連する設定場所
YOUTUBE_CHANNEL_JSON_FILE_PATH: str = '/apps/channel_videos.json'
"""公式チャンネルのコンテンツ一覧ファイルのパス。基本的に変更は必要ありません。"""
YOUTUBE_CHANNEL_ID: str = "UCB1s_IdO-r0nUkY2mXeti-A"
"""公式配信一覧画面で表示対象となるチャンネルのID。"""

# WEBアプリに関する情報の設定場所
WEB_VIEW_APPLICATION_NAME: str = "Leona'sPlayList"
"""WEBアプリ名"""
WEB_VIEW_APPLICATION_ABOUT: list[dict[str]] = [
    {
        'title': 'このWEBページについて',
        'content': ''''本WEBページは獅子神レオナさんのYoutubeでの歌枠配信歌ってみたなどの動画を横断検索することができるファンサイトです。
本WEBページのコンテンツはYouTubeの埋め込み機能を利用しており、転載、切り抜き等には当たりません。
再生された動画が収益化されている場合、YouTubeの規約に準拠して各権利者へ収益が配分されます。
また、すべてのコンテンツの著作権は各動画の配信元に準拠します。
製作者に著作権侵害の意図は一切ございません。各種お問い合わせに関しましては、以下メールアドレスまでご連絡願います。
hiroya@t0d0.jp
'''},
    {
        'title': 'Special Thanks',
        'content': '''イラスト提供：佑希さん
イラスト提供：柊さん
データ登録：Ayuの塩焼きさん
参考情報：コメント欄にタイムスタンプを貼ってくださっている方々'''
    },
    {
        'title': 'Open Source Library',
        'content': '''Name                           Version    License
Babel                          2.10.3     BSD License
Jinja2                         3.1.2      BSD License
MarkupSafe                     2.1.1      BSD License
Pygments                       2.12.0     BSD License
Sphinx                         5.1.1      BSD License
alabaster                      0.7.12     BSD License
certifi                        2022.6.15  Mozilla Public License 2.0 (MPL 2.0)
charset-normalizer             2.1.0      MIT License
click                          8.1.3      BSD License
colorama                       0.4.5      BSD License
groundwork-sphinx-theme        1.1.1      MIT License
idna                           3.3        BSD License
imagesize                      1.4.1      MIT License
livereload                     2.6.3      BSD License
lpl                            0.2        MIT
mccabe                         0.7.0      MIT License
motor                          3.0.0      Apache Software License
packaging                      21.3       Apache Software License; BSD License
prettytable                    3.3.0      BSD License
pycodestyle                    2.9.0      MIT License
pyflakes                       2.5.0      MIT License
pymongo                        4.2.0      Apache Software License
pyparsing                      3.0.9      MIT License
pytz                           2022.1     MIT License
requests                       2.28.1     Apache Software License
six                            1.16.0     MIT License
snowballstemmer                2.2.0      BSD License
sphinx-autobuild               2021.3.14  MIT License
sphinxcontrib-applehelp        1.0.2      BSD License
sphinxcontrib-devhelp          1.0.2      BSD License
sphinxcontrib-htmlhelp         2.0.0      BSD License
sphinxcontrib-jsmath           1.0.1      BSD License
sphinxcontrib-qthelp           1.0.3      BSD License
sphinxcontrib-serializinghtml  1.1.5      BSD License
termcolor                      1.1.0      MIT License
tornado                        6.2        Apache Software License
urllib3                        1.26.11    MIT License
wcwidth                        0.2.5      MIT License
docutils                       0.19       BSD License; GNU General Public License (GPL); Public Domain; Python Software Foundation License
flake8                         5.0.3      MIT License
UIkit                          3.3.3      MIT License
materialize                    1.1.0      MIT License
iconify                        2.2.1      Apache 2.0 license
lite-youtube-embed             0.2.0      Apache 2.0 license
'''
    }
]
"""このWEBアプリについての説明"""
WEB_VIEW_HEADER_IMAGES: list[str] = [
    'yuki_leona_header_trim.avif',
    'hiiragisan_leona.avif',
    'yuki_leona_woy_large.avif'
]
"""ヘッダー部分の画像のファイル名。static/image配下に格納すること"""
