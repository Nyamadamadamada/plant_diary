import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import config.config as config


class Plant(object):
    def __init__(self, name = "", correction = [], hsv_range = [], grow_start_date = None):
        self.__name = name
        self.__correction = correction
        self.__hsv_range = hsv_range
        self.__grow_start_date = grow_start_date

    @property
    def name(self):
        return self.__name

    @property
    def correction(self):
        return self.__correction

    @property
    def hsv_range(self):
        return self.__hsv_range

    @property
    def grow_start_date(self):
        return self.__grow_start_date
    
    @name.setter
    def name(self, name):
        self.__name = name

    @correction.setter
    def correction(self, correction):
        self.__correction = correction

    @hsv_range.setter
    def hsv_range(self, hsv_range):
        self.__hsv_range = hsv_range

    @grow_start_date.setter
    def grow_start_date(self, grow_start_date):
        self.__grow_start_date = grow_start_date

class Diary(object):
    def __init__(self, plant_code = '', taken_date = None, weather = '', temp = 0, humidity = 0):
        self.__plant_code = plant_code
        self.__taken_date = taken_date
        self.__weather = weather
        self.__temp = temp
        self.__humidity = humidity

    @property
    def plant_code(self):
        return self.__plant_code
    
    @property
    def taken_date(self):
        return self.__taken_date
    
    @property
    def weather(self):
        return self.__weather
    
    @property
    def temp(self):
        return self.__temp

    @property
    def humidity(self):
        return self.__humidity
    
    @plant_code.setter
    def plant_code(self, plant_code):
        self.__plant_code = plant_code

    @taken_date.setter
    def taken_date(self, taken_date):
        self.__taken_date = taken_date

    @weather.setter
    def weather(self, weather):
        self.__weather = weather

    @temp.setter
    def temp(self, temp):
        self.__temp = temp

    @humidity.setter
    def humidity(self, humidity):
        self.__humidity = humidity
     
class Firebase:
    def __init__(self):    
        if not firebase_admin._apps:
            cred = credentials.Certificate(config.ROOT_PATH + 'src/config/serviceAccountKey.json') 
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()

    def get_plant(self):
        plant_data = self.db.collection(u'plant').document(config.GROWING_PLANT_CODE).get().to_dict()

        return Plant(plant_data["name"], plant_data["correction"], plant_data["hsv_range"], plant_data["grow_start_date"])
    
    '''
    未使用
    '''
    def get_latestdDiary(self):
        diary_ref = self.db.collection(u'diary')
        diary_ref.where(u'plant_code', u'==', config.GROWING_PLANT_CODE)
        query = diary_ref.order_by(u'taken_date', direction=firestore.Query.DESCENDING).limit(1)
        result = query.stream()

        # TODO オブジェクト１つしかないのにfor文使うの治したい、取得できなかった時の例外
        if result:
            for doc in result:
                return doc.to_dict()
        else:
            return Diary()
    

    def put_diary(self, diary):
        self.db.collection(u'diary').add({
                u'plant_code': diary.plant_code,
                u'taken_date': diary.taken_date,
                u'weather': diary.weather,
                u'temp': diary.temp,
                u'humidity': diary.humidity,
            })

    
    '''
    初期データ用
    '''
    def put_plant(self):
        now = datetime.datetime.now()
        plant = Plant('ｻﾆｰﾚﾀｽ', [{"color": "green", "name": "緑"}],[{"color": "green", "max": [90, 255, 255], "min": [30, 64, 0]}], now)
        self.db.collection(u'plant').document(config.GROWING_PLANT_CODE).set({
                u'name': plant.name,
                u'correction': plant.correction,
                u'hsv_range': plant.hsv_range,
                u'grow_start_date': plant.grow_start_date,
            })
        