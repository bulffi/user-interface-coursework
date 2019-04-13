from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtMultimedia
from asrInterface import Ui_MainWindow
import json,requests
import sys
import os
import speech_recognition as sr
import webbrowser

class WeatherForecast(QWidget):
    def __init__(self):
        super(WeatherForecast,self).__init__()
        weather_url = "http://wthrcdn.etouch.cn/weather_mini?city=" + '上海'
        weather_response = requests.get(weather_url)
        weather_data = json.loads(weather_response.text)
        self.high = weather_data['data']['forecast'][0]['high']
        self.low = weather_data['data']['forecast'][0]['low']
        self.weather_type = weather_data['data']['forecast'][0]['type']
        self.wind_direction = weather_data['data']['forecast'][0]['fengxiang']
        self.tips = weather_data['data']['ganmao']
        self.resize(100,200)
        self.setStyleSheet('background:black')
        self.la_high = QLabel(self.high,self)
        self.la_low = QLabel(self.low, self)
        self.la_type = QLabel(self.weather_type, self)
        self.la_wind = QLabel(self.wind_direction, self)
        self.la_tips = QLabel(self.tips, self)
        self.la_high.setStyleSheet("color: rgb(0, 117, 210);")
        self.la_low.setStyleSheet("color: rgb(0, 117, 210);")
        self.la_type.setStyleSheet("color: rgb(0, 117, 210);")
        self.la_wind.setStyleSheet("color: rgb(0, 117, 210);")
        self.la_tips.setStyleSheet("color: rgb(0, 117, 210);")
        layout = QVBoxLayout()
        layout.addWidget(self.la_high)
        layout.addWidget(self.la_low)
        layout.addWidget(self.la_type)
        layout.addWidget(self.la_wind)
        layout.addWidget(self.la_tips)
        self.setLayout(layout)






class Recorder(QThread):
    finished = pyqtSignal()  # don't know why yet. If defined as self.xxx connet will be lost

    def __init__(self,results):
        super(Recorder, self).__init__()
        self.result = results

    def run(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            self.result["transcription"] = recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            self.result["success"] = False
            self.result["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            self.result["error"] = "Unable to recognize speech"
        self.finished.emit()


class MyWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.btn_start_speaking.clicked.connect(self.start_recording)
        self.response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        self.recorder = Recorder(self.response)
        self.recorder.finished.connect(self.do_something)
        self.sound_file = 'The Doors - People Are Strange.wav'
        self.sound = PyQt5.QtMultimedia.QSound(self.sound_file)

    def start_recording(self):
        self.btn_start_speaking.setText('Listen and Think')
        self.recorder.start()

    def do_something(self):
        print(self.response)
        # TODO do some tasks here!
        if self.response['transcription']:
            if 'music' in self.response['transcription']:
                self.sound.play()
            elif 'stop' in self.response['trancription']:
                self.sound.stop()
            elif 'notepad' in self.response['transcription']:
                os.system('notepad')
            elif 'weather' in self.response['transcription']:
                weather.show()
            elif 'search' in self.response['transcription']:
                webbrowser.open('https://www.baidu.com')
        self.btn_start_speaking.setText('OK! Again?')


app = QtWidgets.QApplication([])
application = MyWindow()
weather = WeatherForecast()
weather.show()
application.show()
sys.exit(app.exec())

