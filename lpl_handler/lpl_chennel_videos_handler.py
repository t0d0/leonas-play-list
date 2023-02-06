import tornado
import json
import pprint


class LPLChannelVideosHandler(tornado.web.RequestHandler):
    async def get(self):
        import time
        with open("channel_videos.json", mode="r", encoding='utf-8') as f:
            raw_channel_video_list = json.load(f)
            channel_video_list = []
            for video in raw_channel_video_list:
                if video["id"]["kind"] == "youtube#video":
                    channel_video_list.append(video)

            login_flg = False
            user = self.get_secure_cookie("user")
            if user:
                login_flg = True

            registrated_video_dict = {}
            time_sta = time.time()

            for video in channel_video_list:

                video_id = video["id"]["videoId"]
                # print(video_id)
                registrated_video_dict[video_id] = list(
                    await self.application.content_db.get_data_by_video_id(video_id))

            # pprint.pprint(registrated_video_dict)
            time_end = time.time()
            tim = time_end - time_sta
            print("search")
            print(tim)

            time_sta = time.time()

            self.render(
                "channel_videos.html",
                login_flg=login_flg,
                channel_video_list=channel_video_list,
                registrated_video_dict=registrated_video_dict
            )
            time_end = time.time()
            tim = time_end - time_sta
            print("render")
            print(tim)

