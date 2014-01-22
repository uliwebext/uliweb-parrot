import string
from json import loads
from datetime import datetime, timedelta
from time import mktime
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError
from urlparse import urlparse, urlunparse
from urlparse import urlsplit, urlunsplit, parse_qsl

HTTP_TIMEOUT = 60

class OAuth2Utils(object):

    @staticmethod
    def get_server_list():
        from uliweb import settings
        servers = settings.get_var("Parrot/ServerList")
        return servers

    @staticmethod
    def create_client(sns_name):
        from uliweb import settings
        from uliweb.utils.common import import_attr
        servers = settings.get_var("Parrot/ServerList")
        server = servers[sns_name]
        return import_attr(server['info'][1])(
            server['client_id'], 
            server['client_secret'],
            server['redirect_uri'])
    
    @staticmethod
    def build_url(base, additional_params=None):
        url = urlparse(base)
        query_params = {}
        query_params.update(parse_qsl(url.query, True))
        if additional_params is not None:
            query_params.update(additional_params)
            for k, v in additional_params.iteritems():
                if v is None:
                    query_params.pop(k)
        
        return urlunparse((url.scheme,
                                    url.netloc,
                                    url.path,
                                    url.params,
                                    urlencode(query_params),
                                    url.fragment))
                                    
    @staticmethod
    def http_request_header(url, access_token, data=None, parse=True, method="GET"):
        from urllib2 import Request, urlopen

        req = Request(url, data=data)
        req.headers.update({
            'Authorization': 'Bearer {0}'.format(access_token)
        })
        
        res = urlopen(req, timeout=HTTP_TIMEOUT).read()
        if parse:
            return loads(res)
        return res
    
    @staticmethod
    def http_request_query(url, access_token, data=None, parse=True, method="GET"):
        from urllib2 import Request, urlopen
        from urlparse import urlparse, urlunparse
        from urlparse import urlsplit, urlunsplit, parse_qsl

        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query))
        query.update({
            'access_token': access_token
        })

        if method == "GET":
            query.update(data)
            url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
            req = Request(url)
        else:
            url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
            req = Request(url, data=urlencode(data))
        
        res = urlopen(req, timeout=HTTP_TIMEOUT).read()

        if parse:
            return loads(res)
        return res


class OAuth2Client(object):
    AUTHORIZE_URI = None
    ACCESS_TOKEN_URI = None
    API_URI_PREFIX = None

    DEFAULT_REQUEST_TYPE = "bearer"
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
        self.access_token = None
        self.refresh_token = None
        self.token_expires = -1

    @property
    def token_uri(self):
        return self.ACCESS_TOKEN_URI
    
    @property   
    def authorization_uri(self):
        return self.AUTHORIZE_URI
    
    @property
    def default_response_type(self):
        return 'code'

    @property
    def default_grant_type(self):
        return 'authorization_code'
    
    def get_authorization_code_uri(self, scope=None, scope_delim=None, state=None, **params):
        
        params.update({
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        })
        
        if 'response_type' not in params:
            params['response_type'] = self.default_response_type
            
        if state is not None:
            params['state'] = state

        scope_delim = scope_delim and scope_delim or ' '
        if scope is not None:
            params['scope'] = scope_delim.join(scope)
        
        return OAuth2Utils.build_url(self.authorization_uri, params)
    
    def get_access_token(self, code=None, **params):
        if code:
            params['code'] = code

        if 'grant_type' not in params:
            params['grant_type'] = self.default_grant_type

        params.update({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
        })
        
        try:
            response = urlopen(self.token_uri, urlencode(params).encode('utf-8'))
            data = loads(response.read().decode('utf-8'))

            for key in data:
                setattr(self, key, data[key])
                
            if hasattr(self, 'expires_in'):
                self.token_expires = mktime((datetime.utcnow() + timedelta(
                    seconds=self.expires_in)).timetuple())

            self.get_avatar()
            return True, data

        except HTTPError, e:
            data = loads(e.read())
            return False, data
        
    def get_refresh_token(self, refresh_token, **params):
        return self.get_token(grant_type='refresh_token', refresh_token=refresh_token)
    
    def call_api(self, api="user/me", data=None, request_type=None, parse=True, method="GET"):
        url = self.API_URI_PREFIX + api

        if not request_type: 
            request_type = self.DEFAULT_REQUEST_TYPE

        if request_type == "bearer":
            return OAuth2Utils.http_request_header(url, self.access_token, data=data, parse=parse, method=method)
        else:
            return OAuth2Utils.http_request_query(url, self.access_token, data=data, parse=parse, method=method)   


    def get_avatar(self):
        return None