import os, sys, io
import M5
from M5 import *
from module import LlmModule
import time

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
label10 = None
label11 = None
label12 = None
label13 = None
llm_0 = None

k = None
dict2 = None
i = None
class2 = None
confidence = None
x1 = None
y1 = None
x2 = None
y2 = None

def handle_ModuleLLM_response_msg():
  global k, dict2, i, class2, confidence, x1, y1, x2, y2, label0, label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12, label13, llm_0
  for k in (llm_0.get_response_msg_list()):
    if (k['work_id']) == (llm_0.get_latest_yolo_work_id()):
      if k['data']['finish']:
        continue
      dict2 = k['data']['delta']
      if dict2 and isinstance(dict2, dict):
        confidence = float(dict2.get('confidence', 0))
        if confidence < 0.65:
          continue
        class2 = dict2.get('class', '')
        bbox = dict2.get('bbox', [0, 0, 0, 0])
        x1 = float(bbox[0])
        y1 = float(bbox[1])
        x2 = float(bbox[2])
        y2 = float(bbox[3])
        label8.setText(str(class2))
        label9.setText(str(round(confidence, 2)))
        label10.setText(str(round(x1, 1)))
        label11.setText(str(round(y1, 1)))
        label12.setText(str(round(x2, 1)))
        label13.setText(str(round(y2, 1)))
        print(f"{class2} {confidence:.2f} bbox:[{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}]")

def setup():
  global label0, label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12, label13, llm_0, dict2, k, class2, confidence, x1, i, y1, x2, y2
  M5.begin()
  Widgets.setRotation(1)
  Widgets.fillScreen(0x222222)
  label0 = Widgets.Label("State", 10, 20, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label1 = Widgets.Label("~", 10, 50, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label2 = Widgets.Label("class", 10, 80, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label3 = Widgets.Label("confidence", 160, 80, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label4 = Widgets.Label("x1", 10, 108, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label5 = Widgets.Label("y1", 10, 140, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label6 = Widgets.Label("x2", 10, 170, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label7 = Widgets.Label("y2", 10, 200, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label8 = Widgets.Label("~", 60, 80, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label9 = Widgets.Label("~", 270, 80, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label10 = Widgets.Label("~", 50, 108, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label11 = Widgets.Label("~", 50, 140, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label12 = Widgets.Label("~", 50, 170, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  label13 = Widgets.Label("~", 50, 200, 1.0, 0xffffff, 0x222222, Widgets.FONTS.Montserrat18)
  print("Iniciando puerto serie UART2 tx=17 rx=18...")
  llm_0 = LlmModule(2, tx=17, rx=18)
  label1.setText(str('Wait ModuleLLM connection..'))
  print("Esperando conexion con ModuleLLM...")
  while not (llm_0.check_connection()):
    time.sleep(1)
  print("Conexion OK. Reseteando ModuleLLM...")
  label1.setText(str('Reset ModuleLLM..'))
  llm_0.sys_reset(True)
  print("Esperando que el sistema arranque tras reset...")
  label1.setText(str('Esperando arranque..'))
  time.sleep(5)
  print("Setup camara...")
  label1.setText(str('Setup Camera module..'))
  llm_0.camera_setup(input='/dev/video0', frame_width=320, frame_height=320, request_id='camera_setup', enoutput=False)
  print("Setup YOLO...")
  label1.setText(str('Setup YOLO module..'))
  llm_0.yolo_setup(model='yolo11n', enoutput=True, input=llm_0.get_latest_camera_work_id(), request_id='yolo_setup')
  print("Setup completo.")
  label1.setText(str('OK'))

def loop():
  global label0, label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12, label13, llm_0, dict2, k, class2, confidence, x1, i, y1, x2, y2
  M5.update()
  llm_0.update()
  handle_ModuleLLM_response_msg()
  llm_0.clear_response_msg_list()

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")