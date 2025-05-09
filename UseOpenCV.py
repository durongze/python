import cv2
import os

# F:\Program\Python\Python312\python.exe  "f:\program\python\python312\scripts\pip3.12.exe" install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple

def LoadImageFromeFile(imgPath):
    # 读取图像并转为灰度
    imgRgb = cv2.imread(imgPath, cv2.IMREAD_COLOR_RGB) # IMREAD_GRAYSCALE
    return imgRgb

def ToGrayImage(imgRgb):
    imgGray = cv2.cvtColor(imgRgb, cv2.COLOR_RGB2GRAY)
    return imgGray

def ToBinaryImage(imgGray):
    # 全局阈值二值化（假设黑色 < 127，白色 >= 127）
    _, imgBinary = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    return imgBinary

def CropImage(img, x1, y1, x2, y2):
    cropped = img[y1:y2, x1:x2]
    return cropped

def ShowImage(title, img):
    # 显示结果
    isExit = False
    cv2.imshow(title, img)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q') or key == 27:  # 27是ESC
        print(f'exit image')
        isExit = True
    cv2.destroyAllWindows()
    return isExit

def ProcImage(imgPath):
    imgRgb = LoadImageFromeFile(imgPath)
    isExit = ShowImage(imgPath, imgRgb)
    if (isExit):
        return isExit
    
    imgGray = ToGrayImage(imgRgb)
    isExit = ShowImage(imgPath, imgGray)
    if (isExit):
        return isExit
    
    imgBinary = ToBinaryImage(imgGray)
    isExit = ShowImage(imgPath, imgBinary)
    if (isExit):
        return isExit
    
    return False

def ProcImageFromDir(directory, extensions=['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                image_files.append(os.path.join(root, file))
    return image_files

def Main():
    image_path = 'images'
    image_files = ProcImageFromDir(image_path)
    for img_path in image_files:
        isExit = ProcImage(img_path)
        if (isExit):
            print(f'exit ...')
            break

if __name__ == "__main__":
    Main()

