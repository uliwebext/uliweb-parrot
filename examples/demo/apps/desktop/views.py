#coding=utf-8
from uliweb import expose, functions

@expose('/')
def index():
	from uliweb import request
	from uliweb.orm import get_model
	from parrot.core import OAuth2Utils
	user_id = request.session.get('user_id')
	if user_id:
		LoginUser = get_model('loginuser')
		user = LoginUser.get(LoginUser.c.id == user_id)
		if user:
			return {'logined':True, 'user': user}

	servers = OAuth2Utils.get_server_list()

	return {'logined': False, 'servers': servers}

@expose('/login/by/<sns>')
def login(sns):
	from parrot.core import OAuth2Utils
	client = OAuth2Utils.create_client(sns)
	url = client.get_authorization_code_uri()
	return redirect(url)

@expose('/account/oauth/<sns>')	
def oauth_callback(sns):
	from parrot.core import OAuth2Utils
	from uliweb.orm import get_model

    #如果是错误回调
	error_code = request.GET.get("error", None)
	if error_code :
		if error_code == "access_denied":
			return error(u"ERROR: 用户拒绝了统一授权登录。")
		else:
			return error(u"ERROR: 未知错误 %s" % error_code)
        
	obj = OAuth2Utils.create_client(sns)
	code=request.GET.get('code', None)
	success, token = obj.get_access_token(code=code)
	if success:
		access_token = token['access_token']
		LoginUser = get_model('loginuser')

		obj = LoginUser(site=sns, name=obj.name, uid=obj.uid, avatar=obj.avatar)
		obj.save()
		request.session.set('user_id', obj.id)
		return redirect("/")

	return "ERROR"
