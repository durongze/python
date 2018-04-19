# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = '郭 璞'
#    __date__ = '2016/8/4'
#    __Desc__ = 一个可以将图片转换成终端字符形式的小工具

from time import *
from PIL import Image

class ImageTool():

    def __init__(self):
        print 'Initialization Completed! @',ctime()

    def getChars(self,image_pixels,image_width,image_height):
        replace_chars = 'ABCDEFGHIJKLMNO '
        terminal_chars = ''
        for h in xrange(image_height):
            for w in xrange(image_width):
                point_pixel = image_pixels[w,h]
                terminal_chars +=replace_chars[int(sum(point_pixel)/3.0/256.0*16)]
            terminal_chars+='\n'
        return terminal_chars

    def formatImage(self,imagename,image_width,image_height):
        img = Image.open(imagename)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        w,h = img.size
        rw = image_width*1.0/w
        rh = image_height*1.0/h
        r = rw if rw<rh else rh
        rw = int(r*w)
        rh = int(r*h)
        img = img.resize((rw,rh),Image.ANTIALIAS)
        return img

    def entrance(self,image_path,out_width,out_height):
        image = self.formatImage(imagename=image_path,image_width=out_width,image_height=out_height)
        image_pixels = image.load()
        out_width ,out_height = image.size
        terminal_chars = self.getChars(image_pixels=image_pixels,image_width=out_width,image_height=out_height)
        print terminal_chars

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print sys.argv[0],'path','w','h'
        sys.exit()
    tool = ImageTool()
    imagename = sys.argv[1]
    w = int(sys.argv[2])
    h = int(sys.argv[3])
    tool.entrance(imagename,w,h);
