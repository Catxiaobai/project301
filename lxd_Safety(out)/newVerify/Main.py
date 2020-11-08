# -*- coding: UTF-8 -*-

#主文件
import os
import forwardSearch as sequeueGenerate
import fileinput
import obtain_efsm_info as obtain_efsm_info
import EFSM
import config
def main():
    time1=0
    count=0
    time2=0
    number=0
    length=0
    select=0
    flag=0
    iteration=0
    targetPath = list()
    uselist = []
    while obtain_efsm_info.targetbranchlist and flag <= len(obtain_efsm_info.targetbranchlist):
        # 序列生成
        pathT = sequeueGenerate.search(uselist)
        time1 += sequeueGenerate.generationtime
        count += sequeueGenerate.successnumber
        number += sequeueGenerate.sequencenumber
        time2 += sequeueGenerate.generationsorttime
        length += sequeueGenerate.sequencelength
        select += sequeueGenerate.selecenumber
        iteration+=1
        print "----------------------"
        print pathT
        print "----------------------"

        if sequeueGenerate.sequencenumber == 0:
            flag += 1
            obtain_efsm_info.sort()
        else:
            flag = 0
            obtain_efsm_info.change()
            path = pathT[0]
            path.extend(targetPath)
            targetPath = path
            uselist = pathT[1]

        # print "生成序列条数为%s" % number
        if number != 0:
            # filename = 'path.txt'
            # with open(filename, 'w') as file_object:
            #     path_num = []
            #     for path in pathT:
            #         path_num.append(int(path[1:]))
            #     file_object.write(str(path_num))
            SM = obtain_efsm_info.returnSM()
            # flag = SM.testGen(pathT)
            # if flag == 1:
            #     print ('生成迁移路径')
            # path = SM.allPathNum()
            # print path
    if flag != 0:
        return -1
    return targetPath

if __name__ == '__main__':
    path = main()
    print path
    if path != -1:
        filepath = 'E:/Code/project301/file/'
        filename = 'path.txt'
        with open(filepath+filename, 'w') as file_object:
            path_num = []
            for pathT in path:
                path_num.append(int(pathT[1:]))
            file_object.write(str(path_num))
        SM = obtain_efsm_info.returnSM()
        flag = SM.testGen(path)
        # if flag == 1:
        #     print ('生成迁移路径')
        # path = SM.allPathNum()
        # print path








