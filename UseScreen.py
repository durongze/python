import cv2
import numpy as np
import pyautogui
import mss

import UseOpenCV as WmOpenCv

# F:\Program\Python\Python312\python.exe  "f:\program\python\python312\scripts\pip3.12.exe" install pyautogui -i https://pypi.tuna.tsinghua.edu.cn/simple
# F:\Program\Python\Python312\python.exe  "f:\program\python\python312\scripts\pip3.12.exe" install mss       -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置截图区域 (x, y, width, height)
region = (10, 10, 500, 800)  # 根据你的需求调整坐标和大小

def ProcImage(imgRgb):
    imgGray = WmOpenCv.ToGrayImage(imgRgb)
    imgBinary = WmOpenCv.ToBinaryImage(imgGray)
    return imgBinary

def CapScreenByAutoGui():
    title = "Screen Capture (Press 'q' to quit)"
    while True:
        screenshot = pyautogui.screenshot(region=region)
        frame = np.array(screenshot)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        imgResult = ProcImage(frame)

        cv2.imshow(title, imgResult)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def CapScreenByMss():
    title = "Screen Capture (Press 'q' to quit)"
    while True:
        with mss.mss() as sct:
            monitor = {"top": region[0], "left": region[1], "width": region[2], "height": region[3]}
            frame = np.array(sct.grab(monitor))

            imgResult = ProcImage(frame)

            cv2.imshow(title, imgResult)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

def Main():
    CapScreenByMss()

if __name__ == "__main__":
    Main()