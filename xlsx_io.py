'''
====== decode ======
example: {
    "Sheet1": {
        "names": {
            "group1": ["name1", "name2", "name3"], 
            "group2": ["name1", "name2", "name3"]
        }, 
        "count": {
            "group1": [1, ], 
            "group2": [1, 4, 10]
        },
    },
    "Sheet2": {
        "names": {
            "group1": ["name1", "name2", "name3"], 
            "group2": ["name1", "name2", "name3"]
        }, 
        "count": {
            "group1": [1, ], 
            "group2": [1, 4, 5]
        },
    }
}
'''

import openpyxl as xl

def decode(fn_meta, fn_names):
    file_meta = xl.load_workbook(fn_meta)
    file_names = xl.load_workbook(fn_names)
    sheets = file_meta.get_sheet_names()
    data = dict()
    for sheet in sheets:
        names = dict()
        count = dict()
        for row in file_meta[sheet].values:
            group_name = row[0]
            names[group_name] = list()
            count[group_name] = list()
            for value in row[1:]:
                count[group_name].append(int(value))
        for row in file_names[sheet].values:
            names[row[1]].append(row[0])
        data[sheet] = dict(names=names, count=count)
    return data
        
if __name__ == '__main__':
    print(decode("./config/meta.xlsx", "./config/names.xlsx"))