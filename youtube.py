from googleapiclient.discovery import build
from config import API_KEY_YOUTUBE

def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY_YOUTUBE)
    request = youtube.videos().list(
        part="snippet, statistics",
        id=video_id
    )
    response = request.execute()
    if 'items' in response:
        video_info = response['items'][0]
        return {
            'title': video_info['snippet']['title'],
            'views': video_info['statistics']['viewCount'],
            'likes': video_info['statistics']['likeCount']
        }
    else:
        return None
