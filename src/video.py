import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        """Инициализация по id видео Ютуб"""
        self.video_id = video_id
        try:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.video_url: str = 'https://youtu.be/' + self.video_id
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except:
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    @property
    def video_response(self):
        return youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.video_id).execute()

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    """Дочерний класс от Video с добавлением id плейлиста"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return super().__str__()
