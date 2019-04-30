1. SQLiteDBを初期化

   * `python -m yajikita init`

2. テスト用サーバ起動(8080ポート)

   1. `export fb_ClientSecret=<Client Secret>`
   2. `export fb_ClientID=<Client ID>`
   3. `python -m yajikita`

3. ブラウザからダッシュボードを開く

   1. http://localhost:8080/yajikita/
   2. (初回のみ) fitbitのOAuthのページにリダイレクトされるので許可を与える
