import os

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist_data = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.title = self.playlist_data['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.video_ids = self.get_video_ids()
        self.video_data = self.get_video_data()

    def get_video_ids(self) -> list[str]:
        """ Получить все id видеороликов из плейлиста """
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        return [video['contentDetails']['videoId'] for video in playlist_videos['items']]

    def get_video_data(self) -> dict[str, dict]:
        """ Получить статистику видео по его id """
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_ids
                                               ).execute()
        video_data = {}
        for item in video_response['items']:
            video_id = item['id']
            title = item['snippet']['title']
            view_count = item['statistics']['viewCount']
            like_count = item['statistics']['likeCount']
            comment_count = item['statistics']['commentCount']
            video_data[video_id] = {
                'title': title,
                'view_count': int(view_count),
                'like_count': int(like_count),
                'comment_count': int(comment_count)
            }
        return video_data

    @property
    def total_duration(self):
        """ Возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста """
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()
        total_duration = isodate.parse_duration('PT0S')

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self) -> str:
        """ Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков) """
        most_liked_video_id = max(self.video_data, key=lambda video_id: self.video_data[video_id]['like_count'])
        return f"https://youtu.be/{most_liked_video_id}"
