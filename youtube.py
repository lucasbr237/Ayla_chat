from googleapiclient.discovery import build
from config import API_KEY_YOUTUBE

def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY_YOUTUBE)
    request = youtube.videos().list(
        part="snippet, statistics, contentDetails, liveStreamingDetails",
        id=video_id
    )
    response = request.execute()
    
    if 'items' in response:
        video_info = response['items'][0]
        result = {
            'title': video_info['snippet']['title'],
            'channel_title': video_info['snippet']['channelTitle'],
            'views': video_info['statistics']['viewCount'],
            'likes': video_info['statistics']['likeCount'],
            'published_at': video_info['snippet']['publishedAt'],
            'duration': video_info['contentDetails']['duration']
        }
        
        if 'liveStreamingDetails' in video_info:
            live_stream_info = video_info['liveStreamingDetails']
            result['actual_start_time'] = live_stream_info.get('actualStartTime')
            result['actual_end_time'] = live_stream_info.get('actualEndTime')
            result['concurrent_viewers'] = live_stream_info.get('concurrentViewers')
        
        return result
    else:
        return None
