from datetime import datetime
from psaw import PushshiftAPI

api = PushshiftAPI()

i = 0
for post in api.search_submissions(subreddit='COVID19', limit=2000):
    print(i, post.id)
    i += 1
