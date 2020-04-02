import os
import cv2
import imageio

src_img_buff = []
gif_img_buff = []
k = 31


def fix_image(img_path):
    img_mat = cv2.imread(img_path, 1)
    img_mat = cv2.resize(img_mat, (360, 460))
    print(img_mat.shape[:2])
    return img_mat


def app_img_mat(img_start, img_end):
    gif_img_set = []
    for i in range(k):
        alpha = (i + 1) / k
        img = cv2.addWeighted(img_start, alpha, img_end, (1 - alpha), gamma=0)
        # cv2.imshow('img', img)
        # cv2.imwrite("img.jpg", img)
        # img = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2BGR)
        gif_img_set.append(img)
        cv2.waitKey(50)
    return gif_img_set


def src_img_mat(img_path):
    src_img_set = []
    for root, dirs, fs in os.walk(img_path):
        for f in fs:
            print(f)
            f_mat = fix_image(img_path + '/' + f)
            src_img_set.append(f_mat)
    return src_img_set


def gif_img_mat(img_path):
    gif_img_set = []
    src_img_set = src_img_mat(img_path)
    for idx in range(src_img_set.__len__() - 1):
        inter = app_img_mat(src_img_set[idx], src_img_set[idx + 1])
        gif_img_set.append(inter)
    return gif_img_set


def main(img_path, gif_file):
    src_img_path = img_path
    src_img_buff = src_img_mat(src_img_path)
    gif_img_buff = gif_img_mat(src_img_path)
    gif = imageio.mimsave(gif_file, src_img_buff, 'GIF', duration=0.5)
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main("./images/", "new.gif")
