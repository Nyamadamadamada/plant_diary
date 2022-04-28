
# 植物観察日記

```
#　必要なモジュール（まとめられないのか？）
pip3 install opencv-python opencv-python-headless
pip3 install numpy
pip3 install numpy --upgrade
pip3 install pillow
pip3 install js2py
pip3 install requests requests_oauthlib
pip3 install --upgrade firebase-admin
npm install firebase
```

実行
```
# 実行
python /Users/yamadanatsumi/app/python/plant_diary/index.py
```

```
# ラズパイ初期設定
sudo apt update
sudo apt upgrade
sudo apt-get install python3-picamera
sudo apt-get install python3-pip
sudo apt-get install libatlas-base-dev
# localに日本語がない
sudo localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
mkdir Public/src
mkdir 
```
## 初期設定
nodeインストール
https://nodered.jp/docs/getting-started/raspberrypi

カメラ設定
```
sudo raspi-config
```

エラーの時
```
E: The package lists or status file could not be parsed or opened.
Reading package lists... Error!
E: Encountered a section with no Package: header
E: Problem with MergeList /var/lib/apt/lists/raspbian.raspberrypi.org_raspbian_dists_bullseye_contrib_binary-armhf_Packages
E: The package lists or status file could not be parsed or opened.
```
↓
```
#設定ファイルをリネーム
sudo mv /var/lib/apt/lists /var/lib/apt/lists_old
sudo apt update
sudo apt upgrade
```
http://kwithubuntu.blog133.fc2.com/blog-entry-39.html

## 植物を変更するときにやること
- config内の`GROWING_PLANT_CODE`を変更する
- FireSotreDBの`plant`テーブルにドキュメントを追加

## 残課題
- index.py実行時にAuthにログインする
- storageへZIPにして送る
- 2色のHSV値から成長を算出する

## 流れ
1. 電源を入れる
2. 8時30分と３5分にプログラムが実行される
3. 画像がTwitterに投稿される
4. 水やり

### plant_diary
- 画像を加工する
- twitterに投稿する
- 画像をFBに送信する
- 観察状況をFBに送信する
- 処理終了後にシャットダウンする

### raspberry
- 写真を撮影する
- cronを定期実行する

### 人間がやること
- ラズパイの電源を確保すること
- 撮影前に電源を入れること
- 朝の水やり（撮影後）


## 参考
ログイン
https://firebase.google.com/docs/reference/rest/auth/#section-sign-in-email-password

画像の合成
https://www.mathpython.com/ja/opencv-image-add/

Twitter API 
画像付きツイート
https://computer.masas-record-storage-container.com/2020/05/04/postmediaupload/

画像の色抽出
https://craft-gogo.com/python-opencv-color-detection/
https://algorithm.joho.info/programming/python/opencv-color-detection/

HSVとは？
https://www.peko-step.com/html/hsv.html

白黒の割合
https://techtech-sorae.com/pythonopencv%E3%81%A7%E4%BA%8C%E5%80%A4%E7%94%BB%E5%83%8F%E3%81%8B%E3%82%89%E7%99%BD%E3%81%A8%E9%BB%92%E3%81%AE%E9%9D%A2%E7%A9%8D%E6%AF%94%E3%82%92%E7%AE%97%E5%87%BA/

１日の時間細分図（府県天気予報の場合）
https://www.jma.go.jp/jma/kishou/know/yougo_hp/saibun.html