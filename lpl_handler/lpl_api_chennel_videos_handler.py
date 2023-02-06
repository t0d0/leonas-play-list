import json
from lpl_handler.lpl_api_base_handler import LPLAPIBaseHandler


class LPLAPIChannelVideosHandler(LPLAPIBaseHandler):

    async def query(self) -> None:
        """QUERYメソッド
        公式配信の検索処理を行う。
        """

        channel_video_list = self.get_argument('video-list', [])
        registrated_video_dict = {}
        for video in channel_video_list:

            video_id = video["id"]["videoId"]
            # print(video_id)
            registrated_video_dict[video_id] = list(
                await self.application.content_db.get_data_by_video_id(video_id))

        # pprint.pprint(registrated_video_dict)
        self.write(json.dumps(registrated_video_dict))

        # self.render(
        #     "channel_videos.html",
        #     login_flg=login_flg,
        #     channel_video_list=channel_video_list,
        #     registrated_video_dict=registrated_video_dict
        # )
        #
