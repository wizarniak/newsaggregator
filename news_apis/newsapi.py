import requests
import json

class NewsapiNews:
    def __init__(self, api_key, max_results = 5):
        self.api_key = api_key
        self.max_results = max_results

    def listing(self):
        '''
        get top headlines from newsapi's general category
        '''
        url = "https://newsapi.org/v2/top-headlines"
        params = {"category": "general", "pageSize": self.max_results}
        response = requests.get(url,
        headers={"Authorization": "bearer " + self.api_key},
        params = params)
        news = []
        for item in json.loads(response.content)["articles"]:
            news_item = {"headline": item["title"],
            "link": item["url"],
            "source": "newsapi"}
            news.append(news_item)
        return news

    def search(self, query):
        '''
        search "everything" on newsapi for most relevant results in english for the query term
        '''
        url = "https://newsapi.org/v2/everything" # everything endpoint gets better search results than top-headlines
        params = {"pageSize": self.max_results, "q": query, "language": "en", "sortBy": "relevancy"}
        response = requests.get(url,
        headers={"Authorization": "bearer " + self.api_key},
        params = params)
        news = []
        for item in json.loads(response.content)["articles"]:
            news_item = {"headline": item["title"],
            "link": item["url"],
            "source": "newsapi"}
            news.append(news_item)
        return news