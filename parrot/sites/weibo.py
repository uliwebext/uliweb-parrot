# -*- coding: utf-8 -*-

from parrot.core import OAuth2Client


class WeiboClient(OAuth2Client):
    AUTHORIZE_URI = 'https://api.weibo.com/oauth2/authorize'
    ACCESS_TOKEN_URI = 'https://api.weibo.com/oauth2/access_token'
    API_URI_PREFIX = 'https://api.weibo.com/2'

    DEFAULT_REQUEST_TYPE = "parameter"

    def __init__(self, *args, **kwargs):
        return super(WeiboClient, self).__init__(*args, **kwargs)

    def get_avatar(self):

        res = self.call_api('/users/show.json', data={'uid': self.uid})
        self.name = res['name']
        self.avatar = res['profile_image_url']

        return {
        	'uid': self.uid,
        	'name': self.name,
        	'avatar': self.avatar
        }

