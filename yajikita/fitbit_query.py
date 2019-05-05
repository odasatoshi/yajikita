import base64
import requests
import os
import json
from yajikita.user_master import (
    update_user, update_steps, list_users, get_access_token, get_refresh_token)


client_secret = os.environ['fb_ClientSecret']
client_id = os.environ['fb_ClientID']
host_path = os.environ['yajikita_host']
if host_path == "":
    host_path = "http://localhost:8080"
redirect_uri = host_path + '/yajikita/callback'
ACCESS_TOKEN_EXPIRES_IN = 86400 * 30  # 30 days

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
        'code': acode,
        'expires_in': ACCESS_TOKEN_EXPIRES_IN
    }

    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)

    if response.status_code == 200:
        ret = json.loads(response.text)
        user_id = ret["user_id"]
        access_token = ret["access_token"]
        refresh_token = ret["refresh_token"]
        get_steps(user_id, access_token, "today", "7d")
        ret = update_user(user_id, access_token=access_token, refresh_token=refresh_token)
        if not ret['name']:
            return get_user_profile(user_id, access_token)
        return ret
    else:
        return None

def refresh_profile(rtoken):
    authcode = 'Basic ' + base64.b64encode((client_id + ":" + client_secret).encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': authcode,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': rtoken,
        'expires_in': ACCESS_TOKEN_EXPIRES_IN
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)
    if response.status_code == 200:
        ret = json.loads(response.text)
        user_id = ret["user_id"]
        access_token = ret["access_token"]
        refresh_token = ret["refresh_token"]
        return update_user(user_id, access_token=access_token, refresh_token=refresh_token)
    else:
        return None


def get_user_profile(user_id, access_token):
    auth = 'Bearer ' + access_token
    headers = {
        'Authorization': auth,
    }
    response = requests.get('https://api.fitbit.com/1/user/-/profile.json', headers=headers)
    if response.status_code == 200:
        ret = json.loads(response.text)["user"]
        avatar = ret["avatar150"].replace('profile_150_square', 'profile_64_square')
        displayName = ret["displayName"]
        return update_user(user_id, displayName=displayName, avatar=avatar)
    else:
        return None

def get_steps(user_id, access_token, end_date, period):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    url = 'https://api.fitbit.com/1/user/-/activities/steps/date/{}/{}.json'.format(
        str(end_date), str(period))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        ret = json.loads(response.text)["activities-steps"]
        update_steps(user_id, ret)
    else:
        print("ERROR")

def renew_per_hour():
    users = list_users()
    for s_user in users:
        get_user_profile(s_user[0],s_user[1])

def get_friends(user_id, access_token, *, retry=False):
    auth = 'Bearer ' + access_token
    headers = {
        'Authorization': auth,
    }
    response = requests.get('https://api.fitbit.com/1.1/user/-/friends.json', headers=headers)
    if response.status_code == 401 and not retry:
        if 'Access token expired' in response.text:
            rtoken = get_refresh_token(user_id)
            refresh_profile(rtoken)
            access_token = get_access_token(user_id)
            return get_friends(user_id, access_token, retry=True)
    if response.status_code != 200:
        return None
    return response.json()["data"]
