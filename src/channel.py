import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.channel_snippet = self.channel['items'][0]['snippet']
        self.channel_statistics = self.channel['items'][0]['statistics']
        self.title = self.channel_snippet['title']
        self.description = self.channel_snippet['description']
        # self.url = self.channel_snippet['thumbnails']['default']['url']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = self.channel_statistics['subscriberCount']
        self.video_count = self.channel_statistics['videoCount']
        self.view_count = self.channel_statistics['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @staticmethod
    def get_service():
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str):
        data_dump = dict()
        data_dump['id'] = self.__channel_id
        data_dump['title'] = self.title
        data_dump['description'] = self.description
        data_dump['url'] = self.url
        data_dump['subscriberCount'] = self.subscriber_count
        data_dump['videoCount'] = self.video_count
        data_dump['viewCount'] = self.view_count
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_dump, indent=2, ensure_ascii=False))
