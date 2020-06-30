from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_response_has_headline_fields():
    """
    each news item in response has a headline field
    """
    response = client.get("/news")
    for news_item in json.loads(response.content):
        assert ("headline" in news_item) == True

def test_response_has_link_fields():
    """
    each news item in response has a link field
    """
    response = client.get("/news")
    for news_item in json.loads(response.content):
        assert ("link" in news_item) == True

def test_response_has_source_fields():
    """
    each news item in response has a source field
    """
    response = client.get("/news")
    for news_item in json.loads(response.content):
        assert ("source" in news_item) == True