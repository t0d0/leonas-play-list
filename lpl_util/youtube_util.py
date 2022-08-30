import pprint
from apiclient.discovery import build

from lpl_const import secret

youtube = build('youtube', 'v3', developerKey=secret.youtube_api_key)

def search(video_id):
    search_response = youtube.videos().list(
        id=video_id,
        part='snippet'
    ).execute()
    return search_response['items'][0]['snippet']['publishedAt']
