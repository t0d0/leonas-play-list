import json

import tornado
from tornado.escape import json_decode

from lpl_handler.lpl_api_base_handler import LPLAPIBaseHandler
from lpl_handler.lpl_base_handler import LPLIndexBaseHandler
from lpl_util import util, youtube_util


class LPLAPISearchSuggestionHandler(LPLAPIBaseHandler):

    async def query(self) -> None:
        """QUERYメソッド
        検索候補の検索処理を行う。
        """
        search_word = self.get_argument('search', '')
        print(search_word)
        if search_word:
            content_data_list = await self.application.content_db.get_search_suggestions(search_word)
            self.write(json.dumps(content_data_list))

        else:
            self.write(json.dumps([]))
