'''
====== decode ======
以下是 decode() 函数解码样例
{
    "Sheet1": {
        "names": {
            "group1": ["name1", "name2", "name3"], 
            "group2": ["name1", "name2", "name3"]
        }, 
        "count": {
            "group1": [1, ], 
            "group2": [1, 4, 10]
        }
    },
    "Sheet2": {
        "names": {
            "group1": ["name1", "name2", "name3"], 
            "group2": ["name1", "name2", "name3"]
        }, 
        "count": {
            "group1": [1, ], 
            "group2": [1, 4, 5]
        }
    }
}
'''

import pickle

# 解码 xlsx 数据
def decode(fn_meta, fn_names):
    try:
        import openpyxl as xl
    except ImportError:
        return 0
    # 元数据未找到返回-1，名单未找到返回-2
    try:
        file_meta = xl.load_workbook(fn_meta)
    except FileNotFoundError:
        return -1
    try:
        file_names = xl.load_workbook(fn_names)
    except FileNotFoundError:
        return -2

    sheets = file_meta.get_sheet_names()
    if(set(file_names.get_sheet_names()) != set(sheets)):
        return -3
    data = dict()
    for sheet in sheets:
        names = dict()
        count = dict()
        # 遍历元数据所有行，找出所有分组
        for row in file_meta[sheet].values:
            group_name = row[0]
            names[group_name] = list()
            count[group_name] = list()
            # 遍历每一行的每一列，添加次数
            for value in row[1:]:
                if value == None:
                    break
                count[group_name].append(int(value))
        # 根据分组添加姓名
        for row in file_names[sheet].values:
            names[row[1]].append(row[0])
        data[sheet] = dict(names=names, count=count)
    return data

# 转储数据到 pickle 文件中
def name_dump_pkl(data, pkl_file):
    with open(pkl_file, 'wb') as f:
        pickle.dump(data, f)

# 从 pickle 文件中读取数据
def name_load_pkl(pkl_file):
    try:
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
        return data
    except FileNotFoundError:
        return -1

def get_config(yml_name="config.yml", json_name="config.json"):
    try:
        import yaml
    except ImportError:
        print("未找到 yaml 模块，从 json 文件中读取配置文件")
        import json
        with open(json_name, 'r', encoding="utf-8") as f:
            config = json.loads(f.read())
    else:
        with open(yml_name, 'r', encoding="utf-8") as f:
            config = yaml.load(f.read(), Loader=yaml.CLoader)
    return config

def get_data(config):
    if("meta" not in config or "names" not in config):
        data = name_load_pkl(config["pkldir"])
    else:
        data = decode(config["meta"], config["names"])
    if(data == -1):
        print("元数据未找到，从二进制文件中读取")
        data = name_load_pkl(config["pkldir"])
    elif(data == -2):
        print("名单未找到，从二进制文件中读取")
        data = name_load_pkl(config["pkldir"])
    elif(data == -3):
        print("元数据与名单不匹配，请检查工作表名是否一致")
        exit()
    elif(data == 0):
        print("未找到openpyxl模块，从二进制文件中读取")
        data = name_load_pkl(config["pkldir"])
    else:
        name_dump_pkl(data, config["pkldir"])
    return data

if __name__ == '__main__':
    print(decode("./config/meta.xlsx", "./config/names.xlsx"))