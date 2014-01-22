# -*- coding: utf-8 -*-

from parrot.core import OAuth2Client


class DoubanClient(OAuth2Client):
    AUTHORIZE_URI = 'https://www.douban.com/service/auth2/auth'
    ACCESS_TOKEN_URI = 'https://www.douban.com/service/auth2/token'
    API_URI_PREFIX = 'https://api.douban.com'

    def __init__(self, *args, **kwargs):

        return super(DoubanClient, self).__init__(*args, **kwargs)

    def get_avatar(self):

    	self.uid = self.douban_user_id
        res = self.call_api('/v2/user/~me')
    	self.name = res['name']
    	self.avatar = res['avatar']

        return {
        	'uid': self.uid,
        	'name': self.name,
        	'avatar': self.avatar
        }

