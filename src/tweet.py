from requests_oauthlib import OAuth1Session
import json
import config.config as config

# TODO:エラー発生時に通知
class Tweet:
    POST_IMG = config.ROOT_PATH + 'workspace/process.jpg'

    def __init__(self):
        self.__outh = OAuth1Session(
            config.CONSUMER_KEY,
            config.CONSUMER_SECRET,
            config.ACCESS_TOKEN,
            config.ACCESS_TOKEN_SECRET,
        )
    
    def exec_tweet(self):
        result = self.upload_media()
        return self.post_tweet(result)


    def upload_media(self):
        files = {
            "media": open(Tweet.POST_IMG, 'rb'),
        }

        response = self.__outh.post(
            config.POST_MEDIA_URL,
            files=files,
        )

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(
                "メディアアップロード失敗: {} {}".format(response.status_code, response.text)
            )


    def post_tweet(self, media_result):
        params = {
            'status' : "[システム投稿]" ,
            'media_ids' : media_result['media_id_string']
        }
        response = self.__outh.post(
            config.POST_TWEET_URL,
            params=params,
        )
        if response.status_code == 200:
            print('Tweet成功')
            return True
        else:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        
