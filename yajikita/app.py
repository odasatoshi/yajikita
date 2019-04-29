from urllib.parse import urlencode
import uuid
import os

from bottle import route, run, template, request, response

from yajikita.fitbit_query import register, client_id, redirect_uri
from yajikita.user_master import list_users


@route('/yajikita/')
def index():
    if request.get_cookie("session"):
        sessionid = request.get_cookie("session")
    else:
        sessionid = str(uuid.uuid4())
        response.set_cookie("session", sessionid)

    qp = urlencode((
        ('response_type', 'code'), ('client_id', client_id), ('redirect_uri', redirect_uri),
        ('scope', ' '.join(['activity', 'profile']))
    ))
    regurl = 'https://www.fitbit.com/oauth2/authorize?' + qp
    ret = '<a href="/yajikita/status"> status </status><br><a href="' + regurl + '"> regist </status>'
    return ret

@route('/yajikita/callback')
def callback():
    callback_code = request.query["code"]
    register(callback_code)
    return '<head><meta http-equiv="refresh"content="3; url=http://localhost:8080/yajikita/"></head><body>regist sucessful.</body>'


@route('/yajikita/test')
def test():
    from yajikita.fitbit_query import get_steps
    from datetime import date, timedelta
    u = list_users()[0]
    day1 = timedelta(days=1)
    get_steps(u['access_token'],
              date.today() - day1,
              date.today() + day1)
