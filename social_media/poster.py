import os
import sys
import json
import argparse
from typing import Optional

# Note: You will need to install these packages:
# pip install tweepy praw requests

try:
    import tweepy
    import praw
    import requests
except ImportError:
    print("Missing dependencies. Please run: pip install tweepy praw requests")
    sys.exit(1)

class SocialPoster:
    def __init__(self, config_path: str = "social_config.json"):
        self.config = self._load_config(config_path)
        self.twitter_api = self._setup_twitter()
        self.reddit_api = self._setup_reddit()

    def _load_config(self, path: str) -> dict:
        if not os.path.exists(path):
            print(f"Config file {path} not found.")
            return {}
        with open(path, 'r') as f:
            return json.load(f)

    def _setup_twitter(self):
        if 'twitter' not in self.config:
            return None
        
        c = self.config['twitter']
        try:
            client = tweepy.Client(
                consumer_key=c['api_key'],
                consumer_secret=c['api_secret'],
                access_token=c['access_token'],
                access_token_secret=c['access_token_secret']
            )
            return client
        except Exception as e:
            print(f"Failed to setup Twitter: {e}")
            return None

    def _setup_reddit(self):
        if 'reddit' not in self.config:
            return None
        
        c = self.config['reddit']
        try:
            reddit = praw.Reddit(
                client_id=c['client_id'],
                client_secret=c['client_secret'],
                user_agent=c['user_agent'],
                username=c['username'],
                password=c['password']
            )
            return reddit
        except Exception as e:
            print(f"Failed to setup Reddit: {e}")
            return None

    def post_tweet(self, text: str):
        if not self.twitter_api:
            print("Twitter API not configured.")
            return
        
        try:
            response = self.twitter_api.create_tweet(text=text)
            print(f"Tweet posted successfully! ID: {response.data['id']}")
        except Exception as e:
            print(f"Error posting tweet: {e}")

    def post_reddit(self, subreddit_name: str, title: str, body: str):
        if not self.reddit_api:
            print("Reddit API not configured.")
            return

        try:
            subreddit = self.reddit_api.subreddit(subreddit_name)
            submission = subreddit.submit(title, selftext=body)
            print(f"Reddit post submitted! URL: {submission.url}")
        except Exception as e:
            print(f"Error posting to Reddit: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automated Social Media Poster for Dolphain")
    parser.add_argument("--platform", choices=['twitter', 'reddit', 'all'], required=True)
    parser.add_argument("--content", help="Path to content file (JSON)", required=True)
    args = parser.parse_args()

    poster = SocialPoster()

    # Load content
    with open(args.content, 'r') as f:
        content = json.load(f)

    if args.platform in ['twitter', 'all']:
        if 'tweet' in content:
            poster.post_tweet(content['tweet'])

    if args.platform in ['reddit', 'all']:
        if 'reddit' in content:
            r = content['reddit']
            poster.post_reddit(r['subreddit'], r['title'], r['body'])

if __name__ == "__main__":
    main()
