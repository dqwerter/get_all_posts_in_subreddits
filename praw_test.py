import os
import praw
import pandas as pd

reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                     client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                     user_agent='What this script is for',
                     username=os.environ.get('REDDIT_USER_NAME'),
                     password=os.environ.get('REDDIT_USER_PASSWORD'))

start_subreddits = ['COVID19positive',
                    'COVID19_support']


for subreddit in start_subreddits:
    # get latest posts from all subreddits
    latest_posts = reddit.subreddit('COVID19positive').new(limit=1000)
    for post in latest_posts:
        print(post.created_utc)
