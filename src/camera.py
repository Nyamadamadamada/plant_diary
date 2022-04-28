from picamera import PiCamera
from time import sleep
import config.config as config

PTHOTO_PATH = config.ROOT_PATH + 'workspace/taken/photo.jpg'

def exec():
    print ("撮影開始")
    camera = PiCamera()
    camera.resolution = (1280, 720)
    sleep(5)
    camera.capture(PTHOTO_PATH)

if __name__ == '__main__':
    exec()
