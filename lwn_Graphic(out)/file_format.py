filename1 = "ATM自然语言描述和形式化表示.txt"
filename2 = "ATM自然语言描述和形式化表示(标准化).txt"
with open('E:/Code/project301/file/' + filename1,'r',encoding = 'utf-8') as fr,open('E:/Code/project301/file/' + filename2,'w',encoding = 'utf-8') as fd:
        for text in fr.readlines():
                if text.split():
                        fd.write(text)
        print('输出成功....')            
