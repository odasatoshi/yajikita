1. SQLiteDBを初期化

   * `python -m yajikita init`

2. テスト用サーバ起動(8080ポート)

   1. `export fb_ClientSecret=<Client Secret>`
   2. `export fb_ClientID=<Client ID>`
   3. `app.py`の`get_dashboard`関数内にあるTODOと書かれた箇所を自分のユーザIDで書き換える
   4. `python -m yajikita`

3. ブラウザからダッシュボードを開く

   * http://localhost:8080/yajikita/index.html
