import ctypes
import sys
import time

import numpy as np
import pydirectinput as mi
import keyboard
import pyautogui
import tensorflow as tf
import tensorflow_hub as hub
import win32gui
from PyQt5.QtWidgets import QApplication

model_name = "movenet_lightning"
#
# module = hub.load("movenet_singlepose_lightning_4")
# input_size = 192
module = hub.load("movenet_singlepose_thunder_4")
input_size = 256
##########################

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()

model = module.signatures['serving_default']

hwnd = win32gui.FindWindow(None, '守望先锋')

channels_count = 4
width = 600
height = 400

x = (1920 - width) // 2
y = (1080 - height) // 2

############################


SendInput = ctypes.windll.user32.SendInput


def MyMoveClick(x=None, y=None):
    currentX, currentY = pyautogui.position()

    extra = ctypes.c_ulong(0)
    ii_ = mi.Input_I()
    ii_.mi = mi.MouseInput(int((x - currentX) * 0.63), int((y - currentY) + abs((y - currentY) * 0.1)), 0,
                           mi.MOUSEEVENTF_MOVE | mi.MOUSEEVENTF_RIGHTCLICK, 0,
                           ctypes.pointer(extra))
    command = mi.Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def movenet():
    start = time.time()
    img = screen.grabWindow(hwnd, x, y, width, height).toImage()
    # img.save("大小测试.png")
    b = img.bits()

    b.setsize(height * width * channels_count)
    arr = np.frombuffer(b, np.uint8).reshape((height, width, channels_count))

    image = np.delete(arr, 3, 2)
    shot = time.time()
    print("抓拍延迟:", shot - start)

    input_image = tf.expand_dims(image, axis=0)
    input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

    # SavedModel format expects tensor type of int32.
    input_image = tf.cast(input_image, dtype=tf.int32)
    # Run model inference.
    outputs = model(input_image)
    # mot = time.time()
    # print("模型延迟:", mot - shot)
    # Output is a [1, 1, 17, 3] tensor.
    keypoints_with_scores = outputs['output_0'].numpy()

    return keypoints_with_scores


# st = False
# R_st = True
# F_st = False
# while True:
#     try:
#         if keyboard.is_pressed('B'):
#             st = False
#         if keyboard.is_pressed('K'):
#             st = True
#         if keyboard.is_pressed('R'):
#             R_st = False
#         else:
#             R_st = True
#         if keyboard.is_pressed('F'):
#             F_st = True
#         else:
#             F_st = False
#         if (st and R_st) or F_st:
#             start = time.time()
#             keypoints_with_scores = movenet()
#
#             # mot = time.time()
#             # print("外模型延迟:", mot - start)
#
#             if keypoints_with_scores[0][0][0][2] < 0.25:
#                 end = time.time()
#                 print("未找到目标")
#                 print("此次延迟", end - start)
#                 continue
#
#             pair = [int(keypoints_with_scores[0][0][0][1] * width), int(keypoints_with_scores[0][0][0][0] * height)]
#
#             MyMoveClick(pair[0] + x, pair[1] + y)
#             end = time.time()
#             # print("移动鼠标延迟：", end - mot)
#             deltime = end - start
#             print("总延迟", deltime)
#             time.sleep(0.08 - deltime)
#     except Exception as e:
#         print(e)


def main_fuc():
    try:
        start = time.time()
        keypoints_with_scores = movenet()

        # mot = time.time()
        # print("外模型延迟:", mot - start)
        if keypoints_with_scores[0][0][0][2] < 0.25:
            end = time.time()
            print("未找到目标")
            print("此次延迟", end - start)
            return
        pair = [int(keypoints_with_scores[0][0][0][1] * width), int(keypoints_with_scores[0][0][0][0] * height)]

        MyMoveClick(pair[0] + x, pair[1] + y)
        end = time.time()
        # print("移动鼠标延迟：", end - mot)
        deltime = end - start
        print("总延迟", deltime)
    except Exception as e:
        print(e)


keyboard.add_hotkey('F', main_fuc)
keyboard.add_hotkey('A+F', main_fuc)
keyboard.add_hotkey('W+F', main_fuc)
keyboard.add_hotkey('S+F', main_fuc)
keyboard.add_hotkey('A+W+F', main_fuc)
keyboard.add_hotkey('A+S+F', main_fuc)
keyboard.wait()
