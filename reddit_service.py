import requests
from requests.auth import HTTPBasicAuth

# Reddit API credentials
CLIENT_ID = 'mKFqGORGhs4DhfGypWeg7A'
SECRET_KEY = 'dZ-JC84p5hAWgYFHFv9kpk6aCTFtLw'
USERNAME = 'Antique_Stretch_3632'
PASSWORD = 'aetrigo@123'

def fetch_reddit_data(keyword, limit=10):
    """
    Fetch Reddit posts based on a keyword.

    Args:
        keyword (str): The search keyword.
        limit (int): The number of posts to fetch.

    Returns:
        list: A list of dictionaries containing post data.
    """
    # Authentication
    auth = HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    headers = {"User-Agent": "MyRedditApp/0.1 by Antique_Stretch_3632"}
    data = {
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD,
    }

    # Get access token
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.status_code}, {response.json()}")
    
    token = response.json().get("access_token")
    headers["Authorization"] = f"bearer {token}"

    # Fetch posts from Reddit
    url = f"https://oauth.reddit.com/search?q={keyword}&limit={limit}"
    reddit_response = requests.get(url, headers=headers)

    if reddit_response.status_code == 200:
        posts = []
        for post in reddit_response.json()["data"]["children"]:
            post_data = post["data"]
            posts.append({
                "title": post_data["title"],
                "author": post_data["author"],
                "score": post_data["score"],
                "comments": post_data["num_comments"],
                "url": post_data["url"],
                "created_utc": post_data["created_utc"],
            })
        return posts
    else:
        raise Exception(f"Failed to fetch posts: {reddit_response.status_code}, {reddit_response.json()}")
