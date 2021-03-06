# fun_readsmp函数用来读取微震事件的波形[单个通道]
# fun_readsmp依赖模块 struct，若未安装，则 pip install struct
# 
# 输入KJ551的smp文件，文件及格式正确时返回list序列，否则返回错误标志"Error"
# KJ551数据的目录规则 年/月/日/事件文件夹（每个通道一个smp文件）
# 如2020/2020-09/2020-09-10/2020-09-10_12-20-59文件夹，包含一个事件的所有通道数据
# import sys
# import os
import os
# import sys
from pathlib import Path


# 目录下需要有文件加格式 如 异常波形\2022-04-29_17-06-22\BMS_01_2022-04-29_17-06-22.smo
# time:格式 2022-04-29_17-06-22 eqp:检测设备数量 threshold：阈值（-1，1）之间
# Pearsons_r("2022-05-03_22-01-19", 16, 0.3)


pah1 = os.getcwd()


# pah1 = os.path.dir_name(pah)


def dfs_file(pah):  # 深度优先搜素找到文件夹 url
    # count = 0
    filelog = []
    day = {}
    for root, dirs, files in os.walk(pah):
        if not dirs:

            day1 = root[-19:]

            for i in files:

                if i[-4:] == ".smp" and i[-23:-4] == day1:
                    filelog.append(i)

            day[f'{day1}'] = filelog
            files.clear()

    print(day)


class DirectionTree(object):
    """
    生成目录树
    """

    def __init__(self, pathname='.', filename='result.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''
        self.cata = {}
        self.filepackage = []
        self.res = []
        self.day = ''
        self.maxeqp = 0
        self.daylist = set()

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self):

        # day: str = ""
        if self.pathname.is_file():
            # self.tree += '    |' * n + '-' * 4 + self.pathname.name + '\n'
            # self.file_name = self.pathname.name.split(".")
            #
            if self.pathname.suffix == ".smp":
                # self.res = self.pathname.name.split('/')
                self.filepackage.append([self.pathname.name, str(self.pathname)])
                # self.day = self.file_name[0][-19:]
                self.day = self.pathname.parent.name
                self.daylist.add(self.day)

                self.cata[f"{self.day}"] = self.filepackage

                if self.maxeqp < len(self.filepackage):
                    self.maxeqp = len(self.filepackage)

            # else:
            #     file_name.clear()
        elif self.pathname.is_dir():
            if self.filepackage:
                self.filepackage = []
                # self.tree += '    |' * n + '-' * 4 + \
                #     str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree()

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)

    def print_cata(self):
        # print(self.cata)
        # print(self.maxeqp)
        self.daylist = list(sorted(self.daylist))
        # print(self.daylist)
        return self.cata, self.maxeqp, self.daylist


class Pearsons_r:

    def __init__(self, cata, eqp, daylist, threshold):
        self.cata = cata
        self.eqp = eqp
        self.threshold = threshold
        self.data = []
        self.val = []
        self.res = {}
        # self.correlation_by_np()
        self.daylist = daylist
        self.data_eqp_num = []
        self.createlist()

    def createlist(self):  # time:格式 2022-04-29_17-06-22 eqp:检测设备数量

        from fun_readsmp import fun_readsmp
        # import os

        '''
           data->save 通道
        '''
        # try:

        for i in self.daylist:
            for j in range(self.eqp):
                self.data.append(fun_readsmp(self.cata[i][j][1]))
                import re
                smp = self.cata[i][j][0]
                s = re.search(r'_\d+_', smp).span()
                self.data_eqp_num.append(smp[s[0] + 1: s[1] - 1])
                # data = []
                # self.cata[]
                # if j + 1 < 10:
                #     self.data.append(fun_readsmp(rf".\异常波形\{self.time}\BMS_0{j + 1}_{self.time}.smp"))
                # else:
                #   self.data.append(fun_readsmp(rf".\异常波形\{self.time}\BMS_{j + 1}_{self.time}.smp"))

            self.correlation_by_np(day=i)
            self.data = []

        # except:
        #
        #     print("数据错误")

    def correlation_by_np(self, day):

        problem = set()
        import numpy as np
        for i in range(len(self.data)):
            for j in range(i + 1, len(self.data)):
                # a = np.array(Array[j])
                # b = np.array(Array[i])
                a = np.array(self.data[i])
                b = np.array(self.data[j])
                val = np.corrcoef(a, b)
                # print(val)
                # self.res[f'{i + 1}, {j + 1} ='] = val[0][1]
                if val[0][1] >= float(self.threshold):
                    problem.add(int(self.data_eqp_num[j]))
                    problem.add(int(self.data_eqp_num[i]))
                    # problem.add(i + 1)
                    # problem.add(j + 1)
        # sorted(problem)
        if not problem:
            print(f"在{day}，没有发现异常通道")
        else:
            print(f"在{day}，第{problem}通道发现异常")


def input_or_cwd():
    a = input("波形文件在当前目录下请输入1，在指定目录下请输入2，放弃请输入3\n")
    threshold = -100
    get_path = ''
    if a == '1':
        get_path = Path.cwd()
        threshold = input("请输入判断异常的阈值(-1,1)\n")

    elif a == '2':

        get_path = input("请您输入指定路径:\n")
        threshold = input("请输入判断阈值\n")

    elif a == '3':
        return ...

    elif a == '':
        print("输入有误,请重新输入\n")
        input_or_cwd()

    dirtree = DirectionTree()
    dirtree.set_path(get_path)
    dirtree.generate_tree()
    (cata, eqp, daylist) = dirtree.print_cata()
    # print(dirtree.cata)
    Pearsons_r(cata, eqp, daylist, threshold)
    # b = input("是否把结果保存到result.txt，是请输入1\n")
    # if b == "1":
    #     with open(result.txt, "w", encoding='utf-8' ) as f:
    #         f.write(res)
    #         # with open(self.filename, 'w', encoding='utf-8') as f:
    # else:
    #     ...


input_or_cwd()

# maxeqp缺失的话？ ->plan:
