import requests
import re
import json


class FetchInstagramUser():

    def __init__(self):
        self.base_url = 'https://www.instagram.com/'
        self.pattern = '<script type="text\/javascript">window._sharedData(.*?);<\/script>'

    def getFeatureArray(self, userid):
        page = requests.get(self.base_url + userid)

        x = re.findall(self.pattern, page.text)[0].lstrip(' = ')
        y = json.loads(x)

        user_data = y['entry_data']['ProfilePage'][0]['graphql']['user']

        return [
            user_data['edge_follow']['count'],  # userFollowerCount
            user_data['edge_followed_by']['count'],  # userFollowingCount
            len(user_data['biography']),  # userBiographyLength
            user_data['edge_owner_to_timeline_media']['count'],  # userMediaCount
            1 if user_data['profile_pic_url'].find('cdninstagram') != -1 else 0,  # userHasProfilePic
            1 if user_data['is_private'] else 0,  # userIsPrivate
            sum(c.isdigit() for c in user_data['username']),  # usernameDigitCount
            len(user_data['username']),  # usernameLength
        ]
