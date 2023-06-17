import random as r

class Names:
    # 初始化：创建选中列表picked，待选列表cur_names，原始列表names
    def __init__(self, names) -> None:
        self.names = names
        self.refresh()
    # 向选中列表中添加n个group组内的名字
    def add(self, group, n):
        while n > 0 and len(self.cur_names[group]) > 0:
            self.picked.append(self.cur_names[group].pop())
            self.cur_cnt[group] += 1
            n -= 1
    # 生成待选列表cur_names，清空选中列表picked
    def refresh(self):
        self.cur_names = self.names.copy()
        self.cur_cnt = {k:0 for k in self.names.keys()}
        self.picked = list()
        for key in self.cur_names.keys():
            r.shuffle(self.cur_names[key])
    # 返回选中列表picked
    def output(self):
        return ' '.join(self.picked)

def main():
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

if __name__ == "__main__":
    main()