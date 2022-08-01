import json

import tornado

from lpl_util import util


class LPLContentHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        """

        Args:
            *args: フレームワークの規定
            **kwargs: フレームワークの規定
        """
        self.write('test')

    async def post(self, *args, **kwargs):
        """

        Args:
            *args: フレームワークの規定
            **kwargs: フレームワークの規定
        """
        search_word = self.get_argument('search', '')

        #        完全一致
        perfect = self.get_argument('perfect', '')

        exist_id = self.get_argument('exist')
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
            favorited_list = json.loads(self.get_argument('local-favorite'))
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

        for i, data in enumerate(content_data_list):
            print(content_data_list[i])
            content_data_list[i]['_id'] = str(data['_id'])

            if login_flg and favorited_list is not None:
                if util.is_favorited_content(content_data_list[i]['_id'], favorited_list):
                    content_data_list[i]['isFavorite'] = True
                else:
                    content_data_list[i]['isFavorite'] = False

        self.write(json.dumps(content_data_list))
