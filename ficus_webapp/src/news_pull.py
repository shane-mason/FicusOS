
import secret
import json
import urllib.request
from datetime import datetime

news_data_file = "news.json"
seconds_to_stale = 3600
def pull_news():
    # https://newsapi.org/docs/endpoints
    url = "https://newsapi.org/v2/top-headlines?country=us&sortBy=popularity&apiKey=" + secret.news_api_key
    contents = urllib.request.urlopen(url).read()
    data = json.loads(contents)

    if data["status"] == "ok":
        if data["totalResults"] > 0:
            output = {
                "timestamp": datetime.now().timestamp(),
                "articles": data['articles']
            }
            out_json= json.dumps(output)
            with open(news_data_file, 'w') as fp:
                fp.write(out_json)
                return True
    return False


def get_articles():
    data = get_news_data_from_file()
    diff = datetime.now().timestamp() - data['timestamp']
    if diff > seconds_to_stale:
        print("News is stale - reloading")
        worked = pull_news()
        if worked:
            print("Update completed - loading fresh data")
            data = get_news_data_from_file()
        else:
            print("Update failed - returning stale data")
    
    return data["articles"]

def curate_articles():
    all_articles = get_articles()
    curated = []
    for article in all_articles:
        if article["source"]["name"] != "[Removed]":
            sparse = {
                "source": article["source"]["name"],
                "title" : article["title"],
                "description": article["description"],
                "content": article["content"]
            }
            curated.append(sparse)
    return curated

def get_news_data_from_file():
    with open(news_data_file) as fp:
        contents = fp.read();
    
    return json.loads(contents)
    

