import requests
import os
import sys
from requests import auth
import logging
import json
import time
from pathlib import Path
from psaw import PushshiftAPI


class RedditApi:
    def __init__(self, client_id, client_secret, user_name, user_password, usage_purpose):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_name = user_name
        self.user_password = user_password
        self.usage_purpose = usage_purpose
        self.base_url = 'https://www.reddit.com/'
        self.api_url = 'https://oauth.reddit.com'
        self.update_access_token()
        self.headers = {'Authorization': self.access_token, 'User-Agent': usage_purpose}
        print('[RedditApi] initialized')

    def update_access_token(self):
        data = {'grant_type': 'password', 'username': self.user_name, 'password': self.user_password}
        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        response = requests.post(self.base_url + 'api/v1/access_token',
                                 data=data,
                                 headers={'User-Agent': self.usage_purpose},
                                 auth=client_auth)
        if response.status_code == 200:
            self.access_token = 'bearer ' + response.json()['access_token']
            # print('[update_access_token] get access_token: ', self.access_token)
        else:
            print('[update_access_token] failed')

    def get_subreddit_posts_response(self, subreddit, limit, after_filename=''):
        if after_filename:
            params = {'limit': limit, 'after': after_filename}
        else:
            params = {'limit': limit}
        response = requests.get(self.api_url + '/r/' + subreddit + '/new', headers=self.headers, params=params)
        if response.status_code == 200:
            return response
        else:
            logger.warning('[get_subreddit_posts_response] status code: {}, not 200.'.format(response.status_code))

    def get_subreddit_posts_filename_helper(self, subreddit, limit, after_filename=''):
        filename_list = []
        response = self.get_subreddit_posts_response(subreddit, limit, after_filename)
        for post in response.json()['data']['children']:
            filename_list.append(post['data']['name'])
        return filename_list

    def get_subreddit_posts_filename(self, subreddit, limit=0):
        if limit == 0:
            limit = int("inf")
        filename_list = []
        remaining_post_number = limit - len(filename_list)
        helper_after_filename = ''
        while remaining_post_number > 0:
            if remaining_post_number > 100:
                helper_limit = 100
            else:
                helper_limit = remaining_post_number
            filename_list += self.get_subreddit_posts_filename_helper(subreddit,
                                                                      helper_limit,
                                                                      helper_after_filename)
            helper_after_filename = filename_list[-1]
            remaining_post_number = limit - len(filename_list)
            print('[get_subreddit_posts_filename] remaining_post_number', remaining_post_number)
        return filename_list

    def get_post_response(self, subreddit, post_id):
        response = requests.get(self.api_url + '/r/' + subreddit + '/comments/' + post_id, headers=self.headers)
        return response

    def save_post_json_data(self, subreddit, post_id):
        response = self.get_post_response(subreddit, post_id)
        if response.status_code == 200:
            with open(os.path.join('post_data_of_subreddit_' + subreddit, post_id + '.json'), 'w+', encoding='utf-8') as output:
                json.dump(response.json(), output)
                print('[save_post_json_data] r/' + subreddit, post_id, 'collected.')
        else:
            time.sleep(3)
            print('[save_post_json_data] r/' + subreddit, post_id, 'empty json with code ' + str(response.status_code) + ', recursively restart.')
            main()

def get_collected_post_set(dir):
    post_collected_id = set()
    for post_id in os.listdir(dir):
        post_collected_id.add(post_id.split('.')[0])
    return post_collected_id


def crawl_subreddit(subreddit, reddit_api, pushshift_api):
    # creat directory when nesessary
    Path(os.path.join('post_data_of_subreddit_' + subreddit)).mkdir(parents=True, exist_ok=True)
    post_collected_id = get_collected_post_set('post_data_of_subreddit_' + subreddit)

    i = 0
    j = float('inf')
    for post in pushshift_api.search_submissions(subreddit=subreddit, limit=j):
        if post.id not in post_collected_id:
            time.sleep(response_interval)
            print('[' + str(i) + '] \t', end='')
            reddit_api.save_post_json_data(subreddit, post.id)
            i += 1

def main():
    reddit_api = RedditApi(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                        user_name=os.environ.get('REDDIT_USER_NAME'),
                        user_password=os.environ.get('REDDIT_USER_PASSWORD'),
                        usage_purpose='COVID19 analysis')
    pushshift_api = PushshiftAPI()

    if subreddit == 'otherSubs':
        print('[list mode]')
        subreddit_list = ['COVID19', 'COVID19_support', 'COVID19positive', 'COVIDProjects', 'PandemicPreps']
        for listed_subreddit in subreddit_list:
            crawl_subreddit(listed_subreddit, reddit_api, pushshift_api)
    else:
        crawl_subreddit(subreddit, reddit_api, pushshift_api)



subreddit = sys.argv[1]
response_interval = float(sys.argv[2])

if __name__ == '__main__':
    main()
