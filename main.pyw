# -*- coding: UTF-8 -*-
import tkinter as tk
import xlsx_io as io
import random_lib as rlib
import pickle as p

# 读取配置文件
try:
    import yaml
except ImportError:
    print("未找到 yaml 模块，从 json 文件中读取配置文件")
    import json
    with open("config.json", 'r', encoding="utf-8") as f:
        config = json.loads(f.read())
else:
    with open("config.yml", 'r', encoding="utf-8") as f:
        config = yaml.load(f.read(), Loader=yaml.CLoader)

# 读取元数据与名单
if("meta" not in config or "names" not in config):
    data = io.name_load_pkl(config["pkldir"])
else:
    data = io.decode(config["meta"], config["names"])
if(data == -1):
    print("元数据未找到，从二进制文件中读取")
    data = io.name_load_pkl(config["pkldir"])
elif(data == -2):
    print("名单未找到，从二进制文件中读取")
    data = io.name_load_pkl(config["pkldir"])
elif(data == -3):
    print("元数据与名单不匹配，请检查工作表名是否一致")
    exit()
elif(data == 0):
    print("未找到openpyxl模块，从二进制文件中读取")
    data = io.name_load(config["pkldir"])
else:
    io.name_dump_pkl(data, config["pkldir"])
    
# 创建主窗口
root = tk.Tk()
root.title(config["title"])
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# 创建文字显示区域
text_frame = tk.Frame(root)
# text_frame.grid(row=0, column=0, sticky="nsew")
text_frame.pack(side="left", fill="both", expand=True)

# 帮助文字显示区域
helptext = tk.Label(text_frame, font=config["help_font"], anchor=tk.CENTER, text=config["help"])
helptext.grid(row=0, column=0, sticky="n")
# helptext.config(highlightbackground="red", highlightthickness=1)
# 主显示区域
print(root.winfo_screenwidth()//2)
display = tk.Label(text_frame, font=config["display_font"], width=root.winfo_screenwidth()//(2*20), wraplength=root.winfo_screenwidth()//2, anchor=tk.CENTER, justify='center')
display.grid(row=1, column=0, sticky="n")
# display.config(highlightbackground="black", highlightthickness=1)
# 计数显示区域
helpcnt = tk.Label(text_frame, font=config["count_font"], anchor=tk.CENTER)
helpcnt.grid(row=2, column=0, sticky="s")
# helpcnt.config(highlightbackground="red", highlightthickness=1)

text_frame.rowconfigure(0, weight=1)
text_frame.rowconfigure(1, weight=1)
text_frame.rowconfigure(2, weight=1)

# 创建按钮显示区域
button_frame = tk.Frame(root)
# button_frame.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
button_frame.pack(side="right", fill="both", expand=True)
# 切换点名方式按钮显示区域
switch_frame = tk.LabelFrame(button_frame, text="点击按钮切换点名方式", font=config["switch_help_font"])
switch_frame.grid(row=0, column=0, sticky="nsew")
# 点名按钮显示区域
choices_frame = tk.LabelFrame(button_frame)
choices_frame.grid(row=1, column=0, sticky=tk.W+tk.E, pady=20)
# 设置选项显示区域
options_frame = tk.LabelFrame(button_frame)
options_frame.grid(row=2, column=0, sticky=tk.S)

button_frame.rowconfigure(0, weight=1)
button_frame.rowconfigure(1, weight=1)
button_frame.rowconfigure(2, weight=1)

# 创建各组random类
random_sheets = dict()
for sheet in data.keys():
    random_sheets[sheet] = rlib.Names(data[sheet]["names"])

# 定义点名按钮的回调函数
cur_sheet = None
def call_pick(n, group, sheet):
    global cur_sheet
    if hold.get() == 1 or sheet != cur_sheet:
        cur_sheet = sheet
        random_sheets[sheet].refresh()
    random_sheets[sheet].add(group, n)
    display.config(text=random_sheets[sheet].output())
    helpcnt.config(text="当前数量：" + str(random_sheets[sheet].count()))

# 定义清空按钮的回调函数
def clear():
    global cur_sheet
    random_sheets[cur_sheet].refresh()
    display.config(text=random_sheets[cur_sheet].output())
    helpcnt.config(text="当前数量：" + str(random_sheets[cur_sheet].count()))

# 快捷生成函数
def callback(event):
    global config
    print(repr(event.char))
    try:
        num = int(event.char)
    except ValueError:
        return
    call_pick(num, config["shortcut_group"], config["shortcut_sheet"])

# 创建点名按钮
grid_map = dict()
buttons = dict()
for sheet in data.keys():
    buttons[sheet] = dict()
    grid_map[sheet] = iter(rlib.GridMap(int(config["maxcol"])))
    for group in data[sheet]["names"].keys():
        buttons[sheet][group] = list()
        for count in data[sheet]["count"][group]:
            buttons[sheet][group].append(tk.Button(choices_frame, text="%s * %d"%(group, count), command=lambda cnt=count,\
                                                   group=group, sheet=sheet:call_pick(cnt, group, sheet), font=config["button_font"]))
            next(grid_map[sheet])
            buttons[sheet][group][-1].grid(row=grid_map[sheet].row(), column=grid_map[sheet].col(), padx=5, pady=5)
            buttons[sheet][group][-1].grid_remove()
        if len(data[sheet]["count"][group]) != 1:
            grid_map[sheet].nextline()

active = None
# 切换点名方式回调函数
def call_switch(sheet):
    global active
    if active != None:
        for group in buttons[active].keys():
            for button in buttons[active][group]:
                button.grid_remove()
    print(buttons)
    for group in buttons[sheet].keys():
        print(group)
        for button in buttons[sheet][group]:
            button.grid()
    active = sheet

# 绑定快捷键
button_frame.bind("<Key>", callback)
button_frame.focus_set()

# 添加切换按钮
keymap = list(data.keys())
chosen = tk.IntVar()
for sheet_id in range(len(keymap)):
    temp = tk.Radiobutton(switch_frame, text="%s"%keymap[sheet_id], font=config["switch_font"], variable=chosen, value=sheet_id, command=lambda sheet_id=sheet_id:call_switch(keymap[sheet_id]), indicatoron=False)
    temp.grid(row=0, column=sheet_id, padx=10, pady=10)
call_switch(keymap[0])

# “滞留”选项
hold = tk.IntVar()
hold.set(1)
hold_check = tk.Checkbutton(options_frame, text='生成时清除原内容', variable = hold, font=config["hold_font"], indicatoron=False)
hold_check.grid(row=0, column=0)

# 清空按钮
clear_button = tk.Button(options_frame, text='清空当前内容', font=config["hold_font"], command=clear)
clear_button.grid(row=0, column=1, padx=10, pady=15)

# mainloop
root.mainloop()