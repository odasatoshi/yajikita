import base64
import requests
import os
import json

from yajikita.user_master import update_user

client_secret = os.environ['fb_ClientSecret']
client_id = os.environ['fb_ClientID']
redirect_uri = 'http://localhost:8080/yajikita/callback'

def check_precondition():
    if not (client_id and client_secret):
        print('fb_ClientSecret or fb_ClientID is empty')
        exit()

def register(acode):
    authcode = 'Basic ' + base64.b64encode((client_id + ":" + client_secret).encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': authcode,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'clientId': client_id,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': acode
    }

    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)

    if response.status_code == 200:
        ret = json.loads(response.text)
        user_id = ret["user_id"]
        access_token = ret["access_token"]
        refresh_token = ret["refresh_token"]
        update_user(user_id, access_token, refresh_token)
    else:
        print("ERROR")


def get_steps(access_token, start_date, end_date):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = 'https://api.fitbit.com/1/user/-/activities/steps/date/{}/{}.json'.format(
        str(start_date), str(end_date))
    resp = requests.get(url, headers=headers)
    print(resp.text)
