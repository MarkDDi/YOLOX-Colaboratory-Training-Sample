import cv2
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
import os
from PIL import Image, ImageTk
from datetime import datetime

cap = cv2.VideoCapture(0)  # 打开摄像头


# 摄像头画布内显示
def tkImage():
    ref, frame = cap.read()  # get a frame
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((600, 500), Image.ANTIALIAS)  # 图像大小重置成和画布一样的
    tkImage = ImageTk.PhotoImage(image=pilImage)
    return tkImage


# 拍照程序
def photo():
    ref, frame = cap.read()  # get a frame
    time_str = datetime.strftime(datetime.now(), '%Y-%m%d-%H-%M-%S')
    cv2.imwrite(path.get() + "\\" + entry_filename.get() + f"({time_str})" + ".png", frame)  # 拍照保存到指定位置


def photo_short():
    ref, frame = cap.read()  # get a frame
    time_str = datetime.strftime(datetime.now(), '%Y-%m%d-%H-%M-%S')
    cv2.imwrite(path.get() + "\\" + "XXXX-0000000" + entry_filename_short.get() + f"({time_str})" + ".png",
                frame)  # 拍照保存到指定位置


def selectPath():
    path_ = askdirectory()  # 使用askdirectory()方法返回文件夹的路径
    if path_ == "":
        path.get()  # 当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    else:
        path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
        path.set(path_)


def openPath():
    dir = os.path.dirname(path.get() + "\\")
    os.system('start ' + dir)
    # print(dir)


# 界面部分
top = tk.Tk()
top.title('视频窗口')
top.geometry('900x600')
path = StringVar()
path.set(os.path.abspath("."))

# 摄像头部分
canvas = Canvas(top, bg='white', width=600, height=500)
canvas.place(x=50, y=50)

# 输入部分（标准）
entry_filename_short = Entry(top, font=("微软雅黑", 10), fg="black", width=7)
Label(top, text="XXXX-0000000").place(x=660, y=150)
entry_filename_short.place(x=760, y=150)
Button(top, text="点此保存图片", command=photo_short, fg="black").place(x=660, y=180)

# 输入部分（自定义）
entry_filename = Entry(top, font=("微软雅黑", 10), fg="blue")
entry_filename.place(x=660, y=250)
Button(top, text="点此保存图片", command=photo, fg="blue").place(x=660, y=280)

# 浏览部分
Label(top, text="目标路径/工站位置:").grid(row=0, column=0)
Entry(top, textvariable=path, state="readonly").grid(row=0, column=1, ipadx=200)
# e.insert(0,os.path.abspath("."))
Button(top, text="路径选择", command=selectPath).grid(row=0, column=2)
Button(top, text="打开文件位置", command=openPath).grid(row=0, column=3)

while True:
    pic = tkImage()
    canvas.create_image(0, 0, anchor='nw', image=pic)
    top.update()
    top.after(1)
cap.release()