import tweet
import config.config as config
import processing
import locale
import datetime
import os
import camera
import firebase
# import camera


PTHOTO_PATH = config.ROOT_PATH + 'workspace/taken/photo.jpg'
COMBINE_IMG = config.ROOT_PATH + 'workspace/combine.jpg'
PROCESS_IMG = config.ROOT_PATH + 'workspace/process.jpg'
STORE_PATH = config.ROOT_PATH + 'workspace/store/'

# 初期データ用
# firebase.Firebase().put_plant()

def file_operation():
    os.remove(COMBINE_IMG)
    os.remove(PROCESS_IMG)
    os.remove(PTHOTO_PATH)

if os.path.exists(PTHOTO_PATH):
    # 曜日を日本語表示させる
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    processing = processing.Process()
    processing.exec()

    # Twitter投稿
    tweet = tweet.Tweet()
    if tweet.exec_tweet():
        file_operation()
        # シャットダウン
        # os.system('sudo shutdown -h now')
else:
    camera.exec()
    command = "node " + config.ROOT_PATH + "js/storage.js"
    os.system(command)
