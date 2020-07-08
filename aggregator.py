import requests
from news_apis.reddit import RedditNews
from news_apis.newsapi import NewsapiNews
import config
import functools

SIZE_LRU_CACHES = 128

class NewsAggregator:
    def __init__(self):
        self.apis = []
        self.apis.append(RedditNews(config.reddit_client_id, config.reddit_client_secret, config.reddit_user_agent, 5))
        self.apis.append(NewsapiNews(config.news_api_key, 5))

    @functools.lru_cache(maxsize=SIZE_LRU_CACHES)
    def listing(self):
        news = []
        for api in self.apis:
            news.append(api.listing())
        return news

    @functools.lru_cache(maxsize=SIZE_LRU_CACHES)
    def search(self, query):
        news = []
        for api in self.apis:
            news.append(api.search(query))
        return news