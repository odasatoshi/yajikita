import base64
import requests
import os
import json
import user_master

def regist(acode):
    client_secret = os.environ["fb_ClientSecret"]
    client_id = os.environ["fb_ClientID"]

    authcode = 'Basic ' + base64.b64encode((client_id + ":" + client_secret).encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': authcode,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'clientId': client_id,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8080/yajikita/callback',
        'code': acode
    }

    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)

    if response.status_code == 200:
        ret = json.loads(response.text)
        user_id = ret["user_id"]
        access_token = ret["access_token"]
        refresh_token = ret["refresh_token"]
        user_master.update_user(user_id, access_token=access_token, refresh_token=refresh_token)
    else:
        print("ERROR")

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
        user_master.update_user(uname, displayName=displayName, avatar=avatar)
    else:
        print("ERROR")

# updated / 1h 
def renew_per_hour():
    users = user_master.list_user()
    for s_user in users:
        get_user_profile(s_user[0],s_user[1])
