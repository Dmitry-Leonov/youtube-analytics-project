import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        # self.api_key: str = os.getenv('YT_API_KEY')
        # self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.channel_snippet = self.channel['items'][0]['snippet']
        self.channel_statistics = self.channel['items'][0]['statistics']
        self.title = self.channel_snippet['title']
        self.description = self.channel_snippet['description']
        # self.url = self.channel_snippet['thumbnails']['default']['url']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = int(self.channel_statistics['subscriberCount'])
        self.video_count = int(self.channel_statistics['videoCount'])
        self.view_count = int(self.channel_statistics['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_data(self):
        """ Получаем список из данных по API - запросу """
        # channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        channel = build('youtube', 'v3', developerKey=api_key)
        return channel

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API """
        channel = cls.channel_data
        return channel

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

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """возвращает общее кол-во подписчиков двух каналов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """возвращает разницу в подписчиках"""
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """возвращает булево от сравнения двух каналов self > other"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """возвращает булево от сравнения двух каналов self >= other"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """возвращает булево от сравнения двух каналов self < other"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """возвращает булево от сравнения двух каналов self <= other"""
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """возвращает булево от сравнения двух каналов self == other"""
        return self.subscriber_count == other.subscriber_count
