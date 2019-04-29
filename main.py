from bottle import route, run, template, request, response
import uuid
import os
import fitbit_query
redirect_uri="http://localhost:8080/"

client_secret = os.environ["fb_ClientSecret"]
client_id = os.environ["fb_ClientID"]

if client_id == "" or client_secret == "":
    exit()


@route('/yajikita/')
def index():
    if request.get_cookie("session"):
        sessionid = request.get_cookie("session")
    else:
        sessionid = str(uuid.uuid4())
        response.set_cookie("session", sessionid)
 
    regurl = 'https://www.fitbit.com/oauth2/authorize?response_type=code&client_id='\
    + client_id + '&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fyajikita%2Fcallback&scope=activity%20profile&expires_in=604800'

    ret = '<a href="/yajikita/status"> status </status><br><a href="' + regurl + '"> regist </status>'
    return ret

@route('/yajikita/callback')
def callback():
    callback_code = request.query["code"]
    fitbit_query.regist(callback_code)
    return '<head><meta http-equiv="refresh"content="3; url=http://localhost:8080/yajikita/"></head><body>regist sucessful.</body>'


if __name__ == '__main__':
    run(host='localhost', port=8080)
else:
    application = default_app()

