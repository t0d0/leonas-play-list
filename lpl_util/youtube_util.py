import datetime
from dateutil.relativedelta import relativedelta
from apiclient.discovery import build
from lpl_const import secret

youtube = build('youtube', 'v3', developerKey=secret.YOUTUBE_API_KEY)

def search(video_id):
    search_response = youtube.videos().list(
        id=video_id,
        part='snippet'
    ).execute()
    return search_response['items'][0]['snippet']['publishedAt']

def get_video_list(channel_id):
    responce = None
    page_token = None
    result_videos = []
    before_date = datetime.datetime.now(datetime.timezone.utc)
    after_date = before_date - relativedelta(years=1)
    while True:
        if page_token is None:
            responce = youtube.search().list(
                channelId=channel_id,
                part='snippet',
                maxResults=50,
                order="date",
                publishedBefore=before_date.isoformat(),
                publishedAfter=after_date.isoformat()
            ).execute()
        else :
            responce = youtube.search().list(
                channelId=channel_id,
                part='snippet',
                maxResults=50,
                pageToken=page_token,
                order="date",
                publishedBefore=before_date.isoformat(),
                publishedAfter=after_date.isoformat()
            ).execute()
        result_videos.extend(responce["items"])
        if  "nextPageToken" in responce.keys():
            page_token = responce["nextPageToken"]
        elif responce["items"]:
            page_token = None
            before_date = before_date - relativedelta(years=1)
            after_date = before_date - relativedelta(years=1)
        else:
            break
    return result_videos
