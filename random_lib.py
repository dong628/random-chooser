import random as r
from copy import deepcopy

class Names:
    # 初始化：创建选中列表picked，待选列表cur_names，原始列表names
    def __init__(self, names) -> None:
        self.names = deepcopy(names)
        self.refresh()
    # 向选中列表中添加n个group组内的名字
    def add(self, group, n):
        while n > 0 and len(self.cur_names[group]) > 0:
            self.picked.append(self.cur_names[group].pop())
            self.cur_cnt[group] += 1
            self.totcnt += 1
            n -= 1
    # 生成待选列表cur_names，清空选中列表picked
    def refresh(self):
        self.cur_names = deepcopy(self.names)
        self.cur_cnt = {k:0 for k in self.cur_names.keys()}
        self.totcnt = 0
        self.picked = list()
        for key in self.cur_names.keys():
            r.shuffle(self.cur_names[key])
        print(self.cur_names)
        print(self.names)
        print(self.picked)
    # 返回选中列表picked
    def output(self):
        return ' '.join(self.picked)
    def count(self):
        return self.totcnt

# 用于计算button在grid中位置的类
class GridMap:
    # 初始化：创建row与col
    def __init__(self, maxcol):
        self.maxcol = maxcol
        self.currow = 0
        self.curcol = 0
    def next(self):
        if self.curcol == self.maxcol:
            self.curcol = 0
            self.currow += 1
        self.curcol += 1
    def nextline(self):
        self.curcol = 0
        self.currow += 1
    def row(self):
        return self.currow
    def col(self):
        return self.curcol

def test_Names():
    data = {str(k):[str(i) for i in range(k*10, (k+1)*10)] for k in range(10)}
    print("data: ", data)
    test = Names(data)
    print("Test 1: ", test.output())
    test.add('1', 3)
    print("Test 2: ", test.output())
    test.add('2', 4)
    test.add('1', 5)
    print("Test 3: ", test.output())
    test.refresh()
    print("Test 4: ", test.output())
    test.add('5', 8)
    print("Test 5: ", test.output())
    test.add('5', 5)
    print("Test 6: ", test.output())

def test_GridMap():
    grid = GridMap(4)
    grid.next()
    grid.next()
    grid.next()
    grid.next()
    print("Test 1: %d - %d" % (grid.row(), grid.col()))
    grid.next()
    grid.next()
    print("Test 2: %d - %d" % (grid.row(), grid.col()))
    grid.nextline()
    print("Test 3: %d - %d" % (grid.row(), grid.col()))

if __name__ == "__main__":
    test_Names()
    test_GridMap()