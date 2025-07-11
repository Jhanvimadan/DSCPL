# utils/api_integration.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FLIC_TOKEN = os.getenv("FLIC_TOKEN")

def get_all_posts():
    url = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
    headers = {
        "Flic-Token": FLIC_TOKEN
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return {"posts": []}
    except Exception as e:
        print("API call failed:", e)
        return {"posts": []}

def get_video_url(topic):
    posts_data = get_all_posts()
    posts = posts_data.get("posts", [])

    # Try to find the first post that matches the topic in title
    for post in posts:
        title = post.get("title", "").lower()
        if topic.lower() in title:
            return post.get("video_url", "https://youtu.be/dQw4w9WgXcQ")

    # If nothing matched, return a fallback
    return "https://youtu.be/dQw4w9WgXcQ"


def get_video_url(search_term="Faith"):
    url = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
    headers = {
        "Flic-Token": "flic_b1c6b09d98e2d4884f61b9b3131dbb27a6af84788e4a25db067a22008ea9cce5"
    }
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json().get("data", [])
        for post in data:
            if search_term.lower() in post["title"].lower():
                return post.get("video_url") or post.get("videoLink") or ""
    except:
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Fallback funny video 😄
