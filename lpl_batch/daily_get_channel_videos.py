from lpl_const import constants
from lpl_util import youtube_util
import json
def get_channel_videos():
    result = youtube_util.get_video_list(constants.channnel_id)
    with open("channel_videos.json",mode="w",encoding="utf-8") as f:
        f.write(json.dumps(result,ensure_ascii=False))