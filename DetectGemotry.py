import cv2
import numpy as np
import math

import UseOpenCV as WmOpenCv

def line_equation(x1, y1, x2, y2):
    A = y2 - y1
    B = x1 - x2
    C = x2*y1 - x1*y2
    return A, B, C

def intersection(A1, B1, C1, A2, B2, C2):
    """计算两条直线的交点"""
    determinant = A1*B2 - A2*B1
    if determinant == 0:
        return None  # 平行线
    x = (B2*C1 - B1*C2) / determinant
    y = (A1*C2 - A2*C1) / determinant
    return (abs(x), abs(y))

def find_phone_border(image, isShow=True):
    if image is None:
        print("无法加载图像")
        return None
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bin = WmOpenCv.ToBinaryImage(gray)
    blurred = cv2.GaussianBlur(bin, (5, 5), 0)
    
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("未找到轮廓")
        return None
    
    largest_contour = max(contours, key=cv2.contourArea)
    
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)
    
    segments = []
    for i in range(len(approx)):
        pt1 = tuple(approx[i][0])
        pt2 = tuple(approx[(i+1)%len(approx)][0])
        segments.append((pt1[0], pt1[1], pt2[0], pt2[1]))
    
    horizontal = []
    vertical = []
    
    for seg in segments:
        x1, y1, x2, y2 = seg
        angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
        
        angle = angle % 180
        if angle > 90:
            angle -= 180
    
        if abs(angle) < 45: 
            horizontal.append(seg)
        else: 
            vertical.append(seg)
    
  
    if len(horizontal) < 2 or len(vertical) < 2:
        print("无法检测到足够的边框线段")
        return None
    
    def line_length(line):
        x1, y1, x2, y2 = line
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    horizontal.sort(key=line_length, reverse=True)
    vertical.sort(key=line_length, reverse=True)
    
    top_line = horizontal[0]
    bottom_line = horizontal[1]
    left_line = vertical[0]
    right_line = vertical[1]
    
    top_A, top_B, top_C = line_equation(*top_line)
    bottom_A, bottom_B, bottom_C = line_equation(*bottom_line)
    left_A, left_B, left_C = line_equation(*left_line)
    right_A, right_B, right_C = line_equation(*right_line)
    
    top_left = intersection(top_A, top_B, top_C, left_A, left_B, left_C)
    top_right = intersection(top_A, top_B, top_C, right_A, right_B, right_C)
    bottom_left = intersection(bottom_A, bottom_B, bottom_C, left_A, left_B, left_C)
    bottom_right = intersection(bottom_A, bottom_B, bottom_C, right_A, right_B, right_C)
    

    if isShow:
        # 绘制轮廓和近似多边形
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 255), 2)
        cv2.drawContours(image, [approx], -1, (255, 0, 255), 2)
        
        # 绘制检测到的边线
        cv2.line(image, (top_line[0], top_line[1]), (top_line[2], top_line[3]), (0, 0, 255), 2)
        cv2.line(image, (bottom_line[0], bottom_line[1]), (bottom_line[2], bottom_line[3]), (0, 0, 255), 2)
        cv2.line(image, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (0, 255, 0), 2)
        cv2.line(image, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (0, 255, 0), 2)
        
        # 绘制延长线交点
        if top_left:
            cv2.circle(image, (int(top_left[0]), int(top_left[1])), 5, (255, 0, 0), -1)
        if top_right:
            cv2.circle(image, (int(top_right[0]), int(top_right[1])), 5, (255, 0, 0), -1)
        if bottom_left:
            cv2.circle(image, (int(bottom_left[0]), int(bottom_left[1])), 5, (255, 0, 0), -1)
        if bottom_right:
            cv2.circle(image, (int(bottom_right[0]), int(bottom_right[1])), 5, (255, 0, 0), -1)
    
    return {
        "contour": largest_contour,
        "approx_contour": approx,
        "top_line": top_line,
        "bottom_line": bottom_line,
        "left_line": left_line,
        "right_line": right_line,
        "corners": {
            "top_left": top_left,
            "top_right": top_right,
            "bottom_left": bottom_left,
            "bottom_right": bottom_right
        }
    }

def proc_cur_img(img):
    result = find_phone_border(img)
    if result:
        print("检测结果:")
        print(f"轮廓点数: {len(result['contour'])}")
        print(f"近似轮廓点数: {len(result['approx_contour'])}")
        print("\n检测到的边框线:")
        print(f"顶边: {result['top_line']}")
        print(f"底边: {result['bottom_line']}")
        print(f"左边: {result['left_line']}")
        print(f"右边: {result['right_line']}")
        print("\n延长线交点坐标:")
        print(f"左上角: {result['corners']['top_left']}")
        print(f"右上角: {result['corners']['top_right']}")
        print(f"左下角: {result['corners']['bottom_left']}")
        print(f"右下角: {result['corners']['bottom_right']}")

def Main():
    isExit = False
    image_path = 'images'
    image_files = WmOpenCv.ProcImageFromDir(image_path)
    for img_path in image_files:
        image = cv2.imread(img_path)
        proc_cur_img(image)

        cv2.imshow("Detection Result", image)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q') or key == 27:  # 27是ESC
            isExit = True
        cv2.destroyAllWindows()
        if (isExit):
            print(f'exit ...')
            break

if __name__ == "__main__":
    Main()