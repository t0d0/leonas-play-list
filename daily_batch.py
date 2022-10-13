import lpl_batch.daily_get_channel_videos
from lpl_batch import daily_get_channel_videos
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

lpl_batch.daily_get_channel_videos.get_channel_videos()