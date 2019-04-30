import hmac
from urllib.parse import urlencode
import uuid
import os
import json

from bottle import route, run, template, request, response, static_file, HTTPResponse

from yajikita.fitbit_query import register, client_id, redirect_uri
from yajikita.user_master import get_dashboard_info

HMAC_KEY = b'yajikita_yajikita'


@route('/yajikita/')
def index():
    return static_file('index.html', root='./html/')


@route('/yajikita/callback')
def index():
    return static_file('callback.html', root='./html/')

@route('/yajikita/test')
def test():
    from yajikita.fitbit_query import get_steps
    from yajikita.user_master import list_users
    from datetime import date
    u = list_users()[0]
    get_steps(u['id'],
              u['access_token'],
              date.today(),
              "1d")

@route('/yajikita/<filename>')
def _static_file(filename):
    return static_file(filename, root='./html/')


def _response_json(obj):
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(obj, ensure_ascii=False)


def _validate_session(session):
    user_id, digest = session.split(':', maxsplit=1)
    if not user_id:
        return None
    expected = hmac.new(HMAC_KEY, msg=user_id.encode('utf8'),
                        digestmod='sha256').hexdigest()
    if digest == expected:
        return user_id
    return None


@route('/yajikita/api/oauth_info')
def get_oauth_info():
    qp = urlencode((
        ('response_type', 'code'), ('client_id', client_id), ('redirect_uri', redirect_uri),
        ('scope', ' '.join(['activity', 'profile']))
    ))
    url = 'https://www.fitbit.com/oauth2/authorize?' + qp
    return _response_json({'url': url})

@route('/yajikita/api/oauth_callback')
def oauth_callback():
    callback_code = request.query["code"]
    ret = register(callback_code)
    if ret:
        hmac_data = hmac.new(HMAC_KEY, msg=ret['user_id'].encode('utf8'),
                             digestmod='sha256').hexdigest()
        ret['session'] = ret['user_id'] + ':' + hmac_data
    return _response_json(ret)


@route('/yajikita/api/dashboard')
def get_dashboard():
    user_id = _validate_session(request.query['session'])
    ret = _response_json(get_dashboard_info(user_id) if user_id else None)
    if not ret:
        return HTTPResponse(status=401)
    return ret

# To refresh access token, GET this URI per 4hours.
@route('/yajikita/api/refresh')
def refresh_acesstoken():
    from yajikita.user_master import list_users
    from yajikita.fitbit_query import refresh_profile
    users = list_users()
    for s_user in users:
        refresh_profile(s_user["refresh_token"])

# To reload steps, GET this URI per an hour.
@route('/yajikita/api/reload_step')
def reload_step():
    from yajikita.user_master import list_users
    from yajikita.fitbit_query import get_steps
    users = list_users()
    for s_user in users:
        get_steps(s_user["user_id"], s_user["access_token"], "today", "7d")

