from bottle import route, run, template, request, response
import uuid
import os
from fitbit.api import Fitbit

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
    fitbit = Fitbit(
        client_id,
        client_secret,
        redirect_uri=redirect_uri,
        timeout=10,
        )
    callback_code = request.query["code"]
    if callback_code:
        try:
            fitbit.client.fetch_access_token(callback_code)
        except:
            pass
    else:
        pass
    for key, value in fitbit.client.session.token.items():
        print('{} = {}'.format(key, value))
        yield template('Requests code is <b>{{code}}</b>, key={{key}}, {{value}}', code=callback_code, key=key, value=value)

    return "exit"



if __name__ == '__main__':
    run(host='localhost', port=8080)
else:
    application = default_app()

