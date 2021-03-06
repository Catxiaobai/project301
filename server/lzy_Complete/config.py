#encoding:utf-8
import sys
import lzy_Complete.EFSM

loopLimit = 5  # 纠正次数上限
numOfPSG = 1    # 序列生成的生成条数
sort = 1  # 排序开关 1是全排序(连接迁移排序按引入变量多少)； 0是DFS（除了候选对立分支）； 2是相关迁移排序； 3是连接迁移排序
# 数据相关迁移的排序
yrzswgbl = 1  # 引入最少无关变量
achcdpx = 1  # 按重合程度排序
mbfzpax = 1 # 目标分支排序
achxhpx = 0  # 按重合先后排序(控制距离)
hhpx = 0  # 混合排序
useNodefition = 1 # 使用未定义优先
usedefition = 1 # 使用已定义优先
#新迁移优先
newtransort = 0
# 权重
defPercent = [10, 1]  # 权重：event action
usePercent = [10, 1]  # 权重：cond action
# 回溯
back = 1  # 1是单步回溯，0是回溯至上一数据相关迁移(全排序和仅连接迁移随机时可用)

# 两个映射函数（混合排序：根据映射函数的不同可以退化成按数量排序或是按先后顺序排序）
def distMap(dist):
        return 1 / dist

def numMap(num):
        return num

# 获取用于序列生成的目标分支
def getTargetBranch(targetBranch):

    return targetBranch

# 获取用于序列生成的模型
def getGenerateModule():
    # print('config')
    # modelfiledir = ''
    # # modelfile = "efsm_atm1.txt"
    # modelfile = "resultModel2.txt"
    # # modelfile = "lift_EFSM.txt"
    # inputfile = modelfiledir + modelfile
    filepath = './file/'
    inputfile=filepath+"resultModel2.txt"
    return inputfile
if __name__ == '__main__':
    getGenerateModule()