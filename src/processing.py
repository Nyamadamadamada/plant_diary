import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests
import config.config as config
import firebase
import datetime


class Process:
    PTHOTO_PATH = config.ROOT_PATH + 'workspace/taken/photo.jpg'
    MASK_IMG = config.ROOT_PATH + 'workspace/mask.jpg'
    FORMAT_IMG = config.ROOT_PATH + 'assets/format.jpg'
    COMBINE_IMG = config.ROOT_PATH + 'workspace/combine.jpg'
    PROCESS_IMG = config.ROOT_PATH + 'workspace/process.jpg'
    FONT_PATH = config.ROOT_PATH + 'assets/font/mushin.otf'
     

    def __init__(self):
        self.weather = ""
        self.temp = 0
        self.humidity = 0
        self.plant = firebase.Firebase().get_plant()
        self.befoerDiary = firebase.Firebase().get_befoerDiary()

    '''
    main
    '''
    def exec(self):
        self.photo_comparison()
        self.set_weather_info()
        self.set_dateText()
        self.pthoto_composition(Process.FORMAT_IMG, Process.PTHOTO_PATH, Process.COMBINE_IMG, 24, 40)
        self.photo_add_text(Process.COMBINE_IMG, Process.PROCESS_IMG)

        # Firebaseに登録
        diary = firebase.Diary(
                plant_code = config.GROWING_PLANT_CODE,
                taken_date = datetime.datetime.now(),
                weather = self.weather_en,
                temp = self.temp,
                humidity = self.humidity
            )
        firebase.Firebase().put_diary(diary)

    '''
    現在の天気を取得し、set
    '''
    def set_weather_info(self):
        params = {
            "APPID" : config.API_KEY,
            "units" : "metric",
            "zip" : "131-0031,jp"
        }
        res = requests.get(config.OPENWEATHER_URL, params=params)
        data = res.json()
        self.temp = round(data["main"]["temp"],1)
        self.humidity = data["main"]["humidity"]
        lstdict = [
            { "en": "Thunderstorm", "ja": "雷" },
            { "en": "Drizzle", "ja": "霧雨☂️" },
            { "en": "Rain", "ja": "雨☂️" },
            { "en": "Snow", "ja": "雪☃️" },
            { "en": "Mist", "ja": "もや" },
            { "en": "Smoke", "ja": "煙" },
            { "en": "Haze", "ja": "かすみ" },
            { "en": "Dust", "ja": "埃" },
            { "en": "Fog", "ja": "霧" },
            { "en": "Sand", "ja": "砂" },
            { "en": "Ash", "ja": "灰" },
            { "en": "Squall", "ja": "スコール" },
            { "en": "Tornado", "ja": "竜巻" },
            { "en": "Clear", "ja": "晴れ☀️" },
            { "en": "Clouds", "ja": "くもり☁️" },
            ]
        self.weather_en = data["weather"][0]["main"]
        self.weather = [x for x in lstdict if x["en"] == self.weather_en][0]["ja"]


    def calc_whiteArea(self, bw_image):
        image_size = bw_image.size
        whitePixels = cv2.countNonZero(bw_image)

        whiteAreaRatio = (whitePixels/image_size)*100#[%]
        self.whiteAreaRatio = round(whiteAreaRatio, config.COLORERIA_DECIMAL_POINT) if round(whiteAreaRatio, config.COLORERIA_DECIMAL_POINT) > 0.01 else 0

    '''
    緑色を検知して白黒にする
    '''
    def photo_comparison(self):
        img = cv2.imread(Process.PTHOTO_PATH)
        # HCV値化する。
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # TODO 複数色の場合
        for hsv_range in self.plant.hsv_range:
            hsv_min = np.array([hsv_range["min"][0], hsv_range["min"][1], hsv_range["min"][2]])
            hsv_max = np.array([hsv_range["max"][0], hsv_range["max"][1], hsv_range["max"][2]])

            # 指定した色に基づいたマスク画像の生成
            mask = cv2.inRange(hsv, hsv_min, hsv_max)
            # マスク画像確認用
            cv2.imwrite(Process.MASK_IMG, mask)
            self.calc_whiteArea(mask)

    '''
    画像を合体させる
    '''
    def pthoto_composition(self, img_path1, img_path2, out, left, top):
        back_img = Image.open(img_path1).resize((1200,1600))
        front_img = Image.open(img_path2).resize((1152, 648))
        back_img_copy = back_img.copy()
        back_img_copy.paste(front_img, (left, top))
        back_img_copy.save(out)


    '''
    画像に文字を追加
    '''
    def photo_add_text(self, img_path, out):
        #元画像を読み込んでくる
        image = Image.open(img_path)
        #文字を書きこむ為のオブジェクトが用意されているので取得する
        draw = ImageDraw.Draw(image)

        plant_name_font = ImageFont.truetype(Process.FONT_PATH, size=180)
        date_font = ImageFont.truetype(Process.FONT_PATH, size=90)
        weather_font = ImageFont.truetype(Process.FONT_PATH, size=85)
        text_font = ImageFont.truetype(Process.FONT_PATH, size=100)
        desc_upper = str(self.what_day) + "日目" + "。" + self.hour_text + "に撮影。"
        desc_lower = self.plant.correction[0]["name"] + "の割合が"+ str(round(self.whiteAreaRatio,2)) + "％"

        #文字描画
        draw.text((40, 730), self.plant.name, fill=(51,51,51), font=plant_name_font)
        draw.text((40, 970), str(self.month), fill=(51,51,51), font=date_font)
        draw.text((190, 970), str(self.day), fill=(51,51,51), font=date_font)
        draw.text((410, 970), self.day_of_week, fill=(51,51,51), font=date_font)
        draw.text((700, 920), self.weather, fill=(51,51,51), font=weather_font)
        draw.text((700, 1010), str(self.temp), fill=(51,51,51), font=weather_font)
        draw.text((80, 1200), desc_upper, fill=(51,51,51), font=text_font)
        draw.text((80, 1320), str(desc_lower), fill=(51,51,51), font=text_font)
        #画像を保存する
        image.save(out)
    
    def set_dateText(self):
        dt_now = datetime.datetime.now()
        hour_to_text = [
            {"min": 0, "max": 3, "name": "未明"},
            {"min": 3, "max": 6, "name": "明け方"},
            {"min": 6, "max": 9, "name": "朝"},
            {"min": 9, "max": 12, "name": "昼前"},
            {"min": 12, "max": 15, "name": "昼過ぎ"},
            {"min": 15, "max": 18, "name": "夕方"},
            {"min": 18, "max": 21, "name": "夜のはじめ頃"},
            {"min": 21, "max": 24, "name": "夜遅く"},
        ]
        hour_date = [x for x in hour_to_text if x["min"] <= dt_now.hour < x["max"]][0]
        self.hour_text = hour_date["name"]
        self.month = dt_now.month
        self.day = dt_now.day
        self.day_of_week = dt_now.strftime('%a')
        self.what_day = (datetime.date.today() - self.plant.grow_start_date.date()).days + 1

