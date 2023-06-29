import tkinter as tk
import random_lib as rlib

# 点名按钮类：描述一组父组件为 frame，数据为 data[sheet]，
# 最大堆叠宽度为 maxcol，点名函数为 call(cnt, group, sheet)，显示字体为 font 的点名按钮
class Buttons:
    def __init__(self, frame, data, sheet, maxcol, call, font):
        self.buttons = dict()
        self.grid_map = iter(rlib.GridMap(int(maxcol)))
        for group in data[sheet]["names"].keys():
            self.buttons[group] = list()
            for count in data[sheet]["count"][group]:
                self.buttons[group].append(tk.Button(frame, text="%s * %d"%(group, count), command=(lambda cnt=count,\
                                                    group=group, sheet=sheet:call(cnt, group, sheet)), font=font))
                next(self.grid_map)
                self.buttons[group][-1].grid(row=self.grid_map.row(), column=self.grid_map.col(), padx=5, pady=5)
                self.buttons[group][-1].grid_remove()
            if len(data[sheet]["count"][group]) != 1:
                self.grid_map.nextline()

# 切换按钮类：描述一组父组件为 frame，数据为 data，
# 绑定点名按钮为 buttons，显示字体为 font 的切换按钮
class Switch:
    def __init__(self, frame, data, buttons, font):
        self.buttons = buttons
        self.active = None
        self.keymap = list(data.keys())
        self.chosen = tk.IntVar()
        for sheet_id in range(len(self.keymap)):
            temp = tk.Radiobutton(frame, text="%s"%self.keymap[sheet_id], font=font,\
                                variable=self.chosen, value=sheet_id, command=lambda sheet_id=sheet_id:self.call_switch(self.keymap[sheet_id]), indicatoron=False)
            temp.grid(row=0, column=sheet_id, padx=10, pady=10, ipadx=5, ipady=5)
    # 切换分组方式方法
    def call_switch(self, sheet):
        if self.active != None:
            for group in self.buttons[self.active].keys():
                for button in self.buttons[self.active][group]:
                    button.grid_remove()
        # print(buttons)
        for group in self.buttons[sheet].keys():
            print(group)
            for button in self.buttons[sheet][group]:
                button.grid()
        self.active = sheet