import autogui
import pyautogui
import time
import os

ui_width, ui_height = pyautogui.size()

print(ui_width, ui_height)
#pyautogui.click(x=22,y=33,clicks=1, button='right')
pyautogui.click(ui_width/2, ui_height/2, button='left')
pyautogui.moveTo(250, ui_height - 2)
pyautogui.click()
pyautogui.typewrite('camera', interval=0.25)
pyautogui.press('enter')
time.sleep(3)
btnCapture = pyautogui.locateOnScreen('still.png')  # 按钮图标，可以找到的
print(btnCapture)
if btnCapture == None:
    pyautogui.alert("error:not found picture")
else:
    btnCaptureX, btnCaptureY = pyautogui.center(btnCapture)
    pyautogui.click(btnCaptureX, btnCaptureY)
