import cv2
import os

import UseOpenCV as WmOpenCv

# F:\Program\Python\Python312\python.exe  "f:\program\python\python312\scripts\pip3.12.exe" install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple

def ProcImage(imgRgb):
    imgGray = WmOpenCv.ToGrayImage(imgRgb)
    imgBinary = WmOpenCv.ToBinaryImage(imgGray)
    return imgBinary

def ShowImage(title, img):
    isExit = False
    cv2.imshow(title, img)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q') or key == 27:  # 27是ESC
        isExit = True
    cv2.destroyAllWindows()
    return isExit

def ShowCameraProps(cap):
    for prop in dir(cv2):
        if prop.startswith("CAP_PROP"):
            prop_id = getattr(cv2, prop)
            value = cap.get(prop_id)
            print(f"{prop}: {value}")

def ShowCameraImage(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("can not get frame.")
            break
        
        image = ProcImage(frame)

        cv2.imshow("Camera", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def OpenCamera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("can not open camera.")
        exit
    return cap

def CloseCamera(cap):
    cap.release()
    cv2.destroyAllWindows()

def SetCamera(cap):
    desired_fps = 5
    success = cap.set(cv2.CAP_PROP_FPS, desired_fps)
    if not success:
        print("Failed to set fps.")
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"set fps: {desired_fps}, cur fps: {actual_fps}")
    width = 1280
    height = 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"screen: {width}x{height}")

def Main():
    cap = OpenCamera()
    ShowCameraProps(cap)
    SetCamera(cap)
    ShowCameraImage(cap)
    CloseCamera(cap)

if __name__ == "__main__":
    Main()