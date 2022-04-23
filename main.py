import mss
import mss.tools
import tkinter
import time
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt


def screenshot(monitor_number=0, output='input/sct.png'):
    with mss.mss() as sct:
        output = sct.shot(mon=monitor_number, output=output)

    return output

def detection():
    # 全画面スクショ
    _ = screenshot()
    im = cv2.imread('input/o1176064415046373356.png')

    # 二値化
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    retval, im_bw = cv2.threshold(im_gray, 215, 255, cv2.THRESH_BINARY)
    cv2.imwrite('output/bw.png', im_bw)

    # 輪郭抽出
    contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 小さい輪郭を削除
    contours = list(filter(lambda x: cv2.contourArea(x) > 80, contours))

    # 四角形の輪郭を出力
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0),2,cv2.LINE_AA)

    cv2.imwrite('output/rect.png', im)

def end():
    root.destroy()

def main():
    # 画面作成
    root = tkinter.Tk()
    root.geometry('300x200')
    root.title('mahjong-recognizer')

    # ボタン作成
    button = tk.Button(text='クリア', font=("Meiryo", "12", "normal"), command = detection)
    button.place(x=100, y =250, width=100, height=50 )
    button = tk.Button(text='終了', font=("Meiryo", "12", "normal"), command = end)
    button.place(x=100, y =370, width=100, height=50 )
    root.mainloop()


if __name__ == '__main__':
    main()
