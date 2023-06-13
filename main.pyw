# -*- coding: UTF-8 -*-
import tkinter as tk
import random
import json
import pickle as p

default_font = ('微软雅黑', 26)
default_help = "使用数字键快速生成指定数量的名字~"

# 读取文件中的信息
try:
    with open('config.pkl', 'rb') as f:
        print("Load from config.pkl\n")
        data = p.load(f)
        print(data)
except FileNotFoundError:
    with open('config.json', 'r', encoding='utf-8') as f:
        print("Warning: Load from config.json\n")
        pkl = open("config.pkl", 'wb')
        data = json.loads(f.read())
        p.dump(data, pkl)
        pkl.close()
        print(data)
    
# 创建主窗口
root = tk.Tk()
root.title('天选时刻')
#root.geometry('500x500')

# 创建显示区域
tf = tk.Frame(root)
tf.grid(row=0, column=0, sticky=tk.W)

display = tk.Label(tf, width=40, height=8, font=default_font, wraplength=800, anchor=tk.CENTER)
display.grid(row=1, column=0, sticky=tk.W)

helptext = tk.Label(tf, font=('微软雅黑', 20), anchor=tk.CENTER, text=default_help)
helptext.grid(row=0, column=0)

tff = tk.Frame(tf)
tff.grid(row=2, column=0)
helpcnt = tk.Label(tff, font=('微软雅黑', 20), anchor=tk.CENTER)
helpcnt.grid(row=0, column=0)

curind = 0
cnt = 0
namesl = data[0][1].split().copy()
random.shuffle(namesl)
names = str()

# 定义点名按钮的回调函数
def calln(n, ind):
    print('ind: ', ind)
    global names, namesl, cnt, curind
    if(hold.get() or ind != curind):
        curind = ind
        namesl = data[ind][1].split().copy()
        random.shuffle(namesl)
        names = str()
        cnt = 0
    for i in range(n):
        try:
            names += ' ' + namesl.pop()
            cnt += 1
        except KeyError:
            pass
    display.config(text=names)
    helpcnt.config(text="当前数量：" + str(cnt))

# 定义退出按钮的回调函数
def quitx():
    root.destroy()

# 快捷生成函数
def callback(event):
    print(repr(event.char))
    try:
        num = int(event.char)
    except ValueError:
        return
    calln(num, 0)

bf = tk.Frame(root)
bf.grid(row=0, column=1, sticky=tk.E)

# 创建点名按钮
cbs = list()
for button in data:
    for ex in button[2]:
        print("append", button[0], ex, "calln(", ex, ',', data.index(button), ")")
        cbs.append(tk.Button(bf, text="%s * %d"%(button[0], ex), command=lambda ex=ex, ix=data.index(button):calln(ex, ix), font=default_font))
        cbs[-1].grid(row=button[3][button[2].index(ex)][0], column=button[3][button[2].index(ex)][1], sticky=tk.W+tk.E)


# 绑定快捷键
bf.bind("<Key>", callback)
bf.focus_set()

# “滞留”选项
hold = tk.IntVar()
hold.set(1)
hold_check = tk.Checkbutton(tff, text='生成时清除原内容', variable = hold, font=('微软雅黑', 22), indicatoron=False)
hold_check.grid(row=0, column=3, padx=50)

calln(1, 0)
root.mainloop()