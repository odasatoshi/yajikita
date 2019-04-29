import base64
import requests
import os
import json
import yajikita.user_master


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
        yajikita.user_master.update_user(user_id, access_token=access_token, refresh_token=refresh_token)
        get_steps(access_token, "today", "7d")
    else:
        print("ERROR")

def refresh_profile(rtoken):
    authcode = 'Basic ' + base64.b64encode((client_id + ":" + client_secret).encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': authcode,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
      'grant_type': 'refresh_token',
      'refresh_token': rtoken
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)
    if response.status_code == 200:
        ret = json.loads(response.text)
        user_id = ret["user_id"]
        access_token = ret["access_token"]
        refresh_token = ret["refresh_token"]
        yajikita.user_master.update_user(user_id, access_token=access_token, refresh_token=refresh_token)
    else:
        print("ERROR")
}

def get_user_profile(uname, access_token):
    auth = 'Bearer ' + access_token
    headers = {
        'Authorization': auth,
    }
    response = requests.get('https://api.fitbit.com/1/user/'+ uname + '/profile.json', headers=headers)
    if response.status_code == 200:
        ret = json.loads(response.text)["user"]
        avatar = ret["avatar150"]
        displayName = ret["displayName"]
        yajikita.user_master.update_user(uname, displayName=displayName, avatar=avatar)
    else:
        print("ERROR")

def get_steps(access_token, end_date, period):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = 'https://api.fitbit.com/1/user/-/activities/steps/date/{}/{}.json'.format(
        str(end_date), str(period))
    resp = requests.get(url, headers=headers)
    print(resp.text)


def renew_per_hour():
    users = yajikita.user_master.list_users()
    for s_user in users:
        get_user_profile(s_user[0],s_user[1])
