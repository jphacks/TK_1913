# Overview
- お辞儀のデータを管理する

# Init
## 1. MySQLのインストール
```
$ sudo apt install mysql
```
- 他にも必要かもしれない
- ユーザなども適宜作成しておく

## 2. データベースの作成
```
mysql -uroot -p
mysql> CREATE DATABASE jph2019
```

## 3. python packageのインストール
- 以下は `run.py` と同じディレクトリで実行する
```
$ pip3 install -r requirements.txt
```

## 4. DBの初期化
```
$ FLASK_APP=run.py flask db init
```

## 5. DBのマイグレーション
```
$ FLASK_APP=run.py flask db migrate
```

# Usage
```
FLASK_APP=run.py flask run
```

# model
`./models/models.py` で定義
## Bow
- お辞儀のデータを格納するモデル

|カラム|型|説明|
|-|-|-|
|id|Integer|primary key|
|timestamp|string|お辞儀が始まった時刻のタイムスタンプ|
|macaddress|string|データを送信するデバイスのmac address|
|path|string|お辞儀データを格納するファイルのパス|
|user_id|Integer|Userへのリファレンス, どのユーザのお辞儀か|
|created_at|datetime|エントリの作成日時|
|updated_at|datetime|エントリの更新日時|

# Routes
`./run.py` で定義
## POST: /start
- (未実装)
- お辞儀データが送られてくる前にお辞儀テーブルににエントリを作成
### Input
- 以下のフォーマットのjson形式のデータが `POST` で `Content-Type: application/json` で送られてくることを期待
```
{
  "timestamp": 1572022431,
  "mac_address": "ff:ff:ff:ff:ff:ff",
}
```
### Process
- DBのBowテーブルにエントリを作成
### Output
- なし

## POST: /bow
- jsonを受け取り，それをそのままtimestampとmac_addressで一意に特定されるファイルに追記していく
### Input
- 以下のフォーマットのjson形式のデータが `POST` で `Content-Type: application/json` で送られてくることを期待
```
{
  "timestamp": 1572022431,
  "time": 1572022431,
  "pressure1": 1000,
  "pressure2": 995,
  "mac_address": "ff:ff:ff:ff:ff:ff",
}
```
### Process
- 送られて来たデータを以下の規則で命名されるファイルに書き込む
```
"{}{}.csv".format(mac_address, timestamp)
# 1572022431ff:ff:ff:ff:ff:ff.csv
```
- `mac_address` と `timestamp`が同じならば同じファイルに書き込まれる

### Output
- 何も返さない
  - 現状ではデバッグのためタイムスタンプを返すようになっている
