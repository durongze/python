import cv2
import numpy as np
import math

import UseOpenCV as WmOpenCv

def detect_all_lines(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBinary = WmOpenCv.ToBinaryImage(imgGray)
    isExit = WmOpenCv.ShowImage('bin', imgBinary)
    if isExit:
        print(f'exit detect.')
    edges = cv2.Canny(imgBinary, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    return lines

def class_vline_and_hline(lines):
    horizontal_lines = []
    vertical_lines = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
        
        if abs(angle) < 45 or abs(angle) > 135:
            horizontal_lines.append(line[0])
        else:
            vertical_lines.append(line[0])
    
    horizontal_lines.sort(key=lambda x: -((x[2]-x[0])**2 + (x[3]-x[1])**2))
    vertical_lines.sort(key=lambda x: -((x[2]-x[0])**2 + (x[3]-x[1])**2))
    return horizontal_lines, vertical_lines

# (Ax + By + C = 0)
def line_equation(x1, y1, x2, y2):
    A = y2 - y1
    B = x1 - x2
    C = x2*y1 - x1*y2
    return A, B, C

def intersection(A1, B1, C1, A2, B2, C2):
    determinant = A1*B2 - A2*B1
    if determinant == 0:
        return None
    x = (B2*C1 - B1*C2) / determinant
    y = (A1*C2 - A2*C1) / determinant
    return (abs(x), abs(y))

def show_border_lines(image, top_line, bottom_line, left_line, right_line):
    cv2.line(image, (top_line[0], top_line[1]), (top_line[2], top_line[3]), (0, 0, 255), 2)
    cv2.line(image, (bottom_line[0], bottom_line[1]), (bottom_line[2], bottom_line[3]), (0, 0, 255), 2)
    cv2.line(image, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (0, 255, 0), 2)
    cv2.line(image, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (0, 255, 0), 2)

def show_corners(image, top_left, top_right, bottom_left, bottom_right):
    if top_left:
        cv2.circle(image, (int(top_left[0]), int(top_left[1])), 5, (255, 0, 0), -1)
    if top_right:
        cv2.circle(image, (int(top_right[0]), int(top_right[1])), 5, (255, 0, 0), -1)
    if bottom_left:
        cv2.circle(image, (int(bottom_left[0]), int(bottom_left[1])), 5, (255, 0, 0), -1)
    if bottom_right:
        cv2.circle(image, (int(bottom_right[0]), int(bottom_right[1])), 5, (255, 0, 0), -1)

def detect_border_lines(image, isShow = True):
    if image is None:
        return None

    lines = detect_all_lines(image)
    if lines is None:
        print("未检测到直线")
        return None
    
    horizontal_lines, vertical_lines = class_vline_and_hline(lines)
    if len(horizontal_lines) < 2 or len(vertical_lines) < 2:
        print("无法检测到足够的边框线")
        return None
    
    top_line = horizontal_lines[0]
    bottom_line = horizontal_lines[1]
    left_line = vertical_lines[0]
    right_line = vertical_lines[1]
    
    top_A, top_B, top_C = line_equation(*top_line)
    bottom_A, bottom_B, bottom_C = line_equation(*bottom_line)
    left_A, left_B, left_C = line_equation(*left_line)
    right_A, right_B, right_C = line_equation(*right_line)
    

    top_left = intersection(top_A, top_B, top_C, left_A, left_B, left_C)
    top_right = intersection(top_A, top_B, top_C, right_A, right_B, right_C)
    bottom_left = intersection(bottom_A, bottom_B, bottom_C, left_A, left_B, left_C)
    bottom_right = intersection(bottom_A, bottom_B, bottom_C, right_A, right_B, right_C)
    
    if isShow:
        show_border_lines(image, top_line, bottom_line, left_line, right_line)
        show_corners(image, top_left, top_right, bottom_left, bottom_right)
    
    return {
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

def proc_cur_img(image):
    isExit = False
    result = detect_border_lines(image)
    if result:
        print("检测到的边框线:")
        print(f"顶边: {result['top_line']}")
        print(f"底边: {result['bottom_line']}")
        print(f"左边: {result['left_line']}")
        print(f"右边: {result['right_line']}")
        print("\n延长线交点坐标:")
        print(f"左上角: {result['corners']['top_left']}")
        print(f"右上角: {result['corners']['top_right']}")
        print(f"左下角: {result['corners']['bottom_left']}")
        print(f"右下角: {result['corners']['bottom_right']}")

        cv2.imshow("Detection Result", image)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q') or key == 27:  # 27是ESC
            isExit = True
        cv2.destroyAllWindows()
        return isExit

def Main():
    image_path = 'images'
    image_files = WmOpenCv.ProcImageFromDir(image_path)
    for img_path in image_files:
        image = cv2.imread(img_path)
        isExit = proc_cur_img(image)
        if (isExit):
            print(f'exit ...')
            break

if __name__ == "__main__":
    Main()
