import math
import tkinter as tk

import pyautogui
from pynput import keyboard,mouse
from pynput.keyboard import Key
from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int

key_press = False
temp_coord = Coord(0,0)
coord = [Coord(0,0),Coord(0,0)]
coord_id = 0
pre_id = -1
text_id = -1
config_constant = 0
show_judge = True


# 获取屏幕尺寸
screen_width, screen_height = pyautogui.size()


# 创建主窗口
root = tk.Tk()
root.attributes("-topmost", True)  # 窗口置顶
root.attributes("-alpha",0.5)  # 设置窗口透明
root.attributes("-fullscreen", True)  # 全屏显示
root.overrideredirect(True)  # 隐藏窗口边框
root.wm_attributes("-disabled", False)  # 允许窗口拦截事件

# 创建画布
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# 在屏幕上画点
def draw_point(x, y):
    global pre_id
    pre_id =  canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="")
# 写字
def draw_text(x,y,text):
    global text_id
    text_id = canvas.create_text(x,y,text=text,fill="red",font=("Arial",20))

# 监听键盘
def on_press(key):
    global key_press, temp_coord, coord,pre_id,coord_id,config_constant
    if key == Key.alt_l:
        key_press = True
    if hasattr(key, 'char') and key.char == '+':
        if temp_coord.x ==0 and temp_coord.y ==0:
            canvas.itemconfig(text_id, text="你确定你点出红点了？")
        else:
            if coord_id == 0:  #这部分完成第一个点的输入，同时为了时刻显示图像，将pre_id设为初始值
                pre_id = -1
                coord[0] = temp_coord
                temp_coord = Coord(0, 0)
                coord_id = 1
                if config_constant == 0:
                    canvas.itemconfig(text_id,text = "配置点1输入完成，输入配置点2")
                else:
                    canvas.itemconfig(text_id, text="迫击炮位置输入完成，输入目标位置")
            else:  #这部分是第二个点的工作,有两种,第二种搬到鼠标点击里实现了，这样可以实时
                if config_constant == 0:
                    coord[1] = temp_coord
                    temp_coord = Coord(0, 0)
                    config_constant =round(math.sqrt((coord[0].x-coord[1].x)**2+(coord[0].y-coord[1].y)**2))
                    canvas.delete("all")
                    if config_constant == 0:
                        draw_text(screen_width-300,30,"配置失败，点距离太小了")
                    else:
                        draw_text(screen_width - 300, 30, "配置成功，输入迫击炮位置")
                    coord_id = 0
    if hasattr(key, 'char') and key.char == '-':
        if config_constant == 0:
            if key_press:
                exit_all()
            else:
                canvas.itemconfig(text_id, text="退出程序按alt和-")

        else:
            if coord_id == 0:
                config_constant = 0
                canvas.delete("all")
                draw_text(screen_width-300,30,"输入配置点1")
            else:
                coord_id = 0
                canvas.delete("all")
                draw_text(screen_width - 300, 30, "配置成功，输入迫击炮位置")
    if hasattr(key, 'char') and key.char == '*':
        global show_judge
        if show_judge:
            root.withdraw()
            show_judge = False
        else:
            root.deiconify()
            show_judge = True

def on_release(key):
    if key == Key.alt_l:
        global  key_press
        key_press = False

def on_mouse_click(x, y, button, pressed):
    global key_press
    if key_press and pressed:
        canvas.delete(pre_id)
        draw_point(x,y)
        global temp_coord
        temp_coord = Coord(x,y)
        if coord_id == 1 and config_constant != 0:
            coord[1] = temp_coord
            temp_length = round(
                math.sqrt((coord[0].x - coord[1].x) ** 2 + (coord[0].y - coord[1].y) ** 2)) * 1000 / config_constant
            canvas.itemconfig(text_id, text=f"距离为{temp_length}")

def exit_all():
    global keyboard_listener,mouse_listener,root
    keyboard_listener.stop()
    mouse_listener.stop()
    root.destroy()
    exit()
# 启动监听
keyboard_listener = keyboard.Listener(on_press = on_press,on_release=on_release)
keyboard_listener.start()


mouse_listener = mouse.Listener(on_click=on_mouse_click)
mouse_listener.start()


# 程序启动，要求输入配置点1
draw_text(screen_width-300,30,"输入配置点1")


# 运行主循环
root.mainloop()