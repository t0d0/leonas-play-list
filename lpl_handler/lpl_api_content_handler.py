import json

import tornado
from tornado.escape import json_decode

from lpl_handler.lpl_api_base_handler import LPLAPIBaseHandler
from lpl_handler.lpl_base_handler import LPLIndexBaseHandler
from lpl_util import util, youtube_util


class LPLAPIContentHandler(LPLAPIBaseHandler):

    async def query(self) -> None:
        """QUERYメソッド
        コンテンツの検索処理を行う。
        POSTでコンテンツ取得を行うのは直感的ではないが、クエリパラメータの長大化が懸念されるため、
        QUERYメソッドを定義しています。
        TODO:でかすぎる。どうにかしたい。
        """
        search_word = self.get_argument('search', '')
        print(search_word)
        #        完全一致
        perfect = self.get_argument('perfect', '')
        exist_id = self.get_argument('exist', '')
        exist_id = exist_id.split(',')
        if perfect == "true":
            perfect = True

        artist = self.get_argument('artist', '')

        favorite_flg = self.get_argument('favorite', '')

        if favorite_flg == "true":
            favorite_flg = True

        login_flg = False

        user = self.get_secure_cookie("user")
        if user:
            print('ログイン済みユーザ')
            login_flg = True
            user = user.decode('utf-8')
            favorited_list = await self.application.favorite_db.get_data(user)
            if favorited_list is not None:
                favorited_list = favorited_list['favorites']
            else:
                favorited_list = []
        else:
            print('ログインしてないユーザ')
            print(self.get_argument('local-favorite', '[]'))
            favorited_list = json.loads(self.get_argument('local-favorite', '[]'))
            #            pprint.pprint(favorited_list)

            if favorited_list is not None:
                print(favorited_list)
                # favorited_list = favorited_list['favorites']

        print('artist')
        print(artist)
        if favorite_flg:
            if exist_id[0] == '':
                exist_id = []

            content_data_list = list(await self.application.content_db.get_data_by_ids(favorited_list, exist_id))

        elif artist != '':
            if exist_id[0] == '':
                exist_id = []
            if artist == 'unknown':
                artist = ''
            content_data_list = await self.application.content_db.get_data_by_artist(artist, exist_id)
            content_data_list = list(content_data_list)
        else:
            if exist_id[0] == '':
                exist_id = []
            content_data_list = await self.application.content_db.get_data(search_word, exist_id, perfect)
        print(content_data_list),

        for i, data in enumerate(content_data_list):
            if login_flg and favorited_list is not None:
                if util.is_favorited_content(content_data_list[i]['_id'], favorited_list):
                    content_data_list[i]['isFavorite'] = True
                else:
                    content_data_list[i]['isFavorite'] = False

        self.write(json.dumps(content_data_list))

    async def post(self) -> None:
        """POSTメソッド
        コンテンツの新規投稿を行う。

        """
        titles = util.split_vertical_bar(self.get_argument('title', ''))
        times = util.split_vertical_bar(self.get_argument('time', ''))
        content_db = self.application.content_db
        inserted_ids = []
        video_id = util.get_video_id(self.get_argument('url', ''))
        published_at = youtube_util.search(video_id)
        for (title, time) in zip(titles, times):
            data = content_db.ContentDataFormat(title=title,
                                                video_id=video_id,
                                                time=util.convert_time(time),
                                                published_at=published_at)
            insert_result = await content_db.set_data(data)
            inserted_ids.append(str(insert_result.inserted_id))

        content_data_list = []
        for inserted_id in inserted_ids:
            content_data_list.extend(list(await content_db.get_data_by_id(inserted_id)))
        print(content_data_list)
        for data in content_data_list:
            data['_id'] = str(data['_id'])

        self.write(json.dumps(content_data_list))

    async def put(self) -> None:
        """PUTメソッド
        コンテンツの更新を行う。

        """
        print('edit')
        content_db = self.application.content_db
        update_data = content_db.ContentDataFormat(_id=self.get_argument('target', ''),
                                                   title=self.get_argument('title', ''),
                                                   artist=self.get_argument('artist', ''),
                                                   video_id=util.get_video_id(self.get_argument('url', '')),
                                                   time=util.convert_time(self.get_argument('time', '')))

        update_result = await content_db.update_data(update_data)
        for i, data in enumerate(update_result):
            print(update_result[i])
            update_result[i]['_id'] = str(data['_id'])

        print(update_result)
        print(type(update_result))
        self.write(json.dumps(update_result[0]))

    def delete(self):
        print('delete')
        target_id = self.get_argument('target')
        self.application.content_db.erase_data(target_id)
        #        data = list(content_db.get_data())
        #        self.redirect("/leonas_play_list")
        self.write(json.dumps({"result": "complete"}))
