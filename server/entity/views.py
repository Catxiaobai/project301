import json
import time
import os
import subprocess

from django.http import HttpResponse, JsonResponse

from entity.models import Trace, Invalid
from server import error_code
from django.shortcuts import render


# Create your views here.


# 建模
def modeling(request):
    os.system('python3 E:/Code/project301/lwn_Graphic/ConstructModel.py')
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 图形化展示模型
def show_model(request):
    os.system('python3 E:/Code/project301/lwn_Graphic/2020-08.py')
    pp = subprocess.Popen('python3 E:/Code/project301/lwn_Graphic/draw_graph.py')
    time.sleep(10)
    pp.kill()
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 完整性验证
def judge_model(request):
    os.system('python3 E:/Code/project301/lzy_Complete/Model3/judgeModelComplete.py')
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        lines = f.readline().split("\n")
    res = lines[0]
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        test = f.read()
    test = test[62:]
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": res, "msg": test})


# 模型补全
def add_model(request):
    request_json = json.loads(request.body)
    if (None == request_json):
        return JsonResponse({**error_code.CLACK_NULL_ERROR})
    with open('E:/Code/project301/file/addTrace.txt', 'w') as f:  # 设置文件对象
        for i in range(len(request_json)):
            f.write('Trace:\n')
            f.write(request_json[i]['value'].replace('  ', '\n'))  # 将字符串写入文件中
            f.write('\n')
    os.system('python3 E:/Code/project301/lzy_Complete/Model3/completeModel.py')
    os.system('python3 E:/Code/project301/lwn_Graphic/2020-08.py')

    return JsonResponse({**error_code.CLACK_SUCCESS})


# 安全性验证
def safe_verify(request):
    request_json = json.loads(request.body)
    res = request_json['msg']
    with open('E:/Code/project301/file/target.txt', 'w') as f:  # 设置文件对象
        f.write('Transition:\n')
        f.write(res.replace('  ', '\n'))  # 将字符串写入文件中
    os.system('python2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 增加场景
def add_trace(request):
    request_json = json.loads(request.body)
    try:
        trace = Trace(trace_name=request_json['name'],
                      trace_content=request_json['content'],
                      trace_describe=request_json['describe'],
                      trace_details=request_json['details'])
        trace.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 修改场景
def edit_trace(request):
    request_json = json.loads(request.body)
    aim_id = request_json['id']
    new_name = request_json['name']
    new_content = request_json['content']
    new_describe = request_json['describe']
    new_details = request_json['details']

    if not Trace.objects.filter(id=aim_id).exists():
        return JsonResponse({**error_code.CLACK_NOT_EXISTS})
    try:
        Trace.objects.filter(id=aim_id).update(trace_name=new_name)
        Trace.objects.filter(id=aim_id).update(trace_content=new_content)
        Trace.objects.filter(id=aim_id).update(trace_describe=new_describe)
        Trace.objects.filter(id=aim_id).update(trace_details=new_details)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": str(e)})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除场景
def delete_trace(request):
    request_json = json.loads(request.body)
    aim_id = request_json['trace_id']
    try:
        Trace.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 查询全部场景
def trace_list(request):
    traces = Trace.objects.all()
    result = [trace.to_dict() for trace in traces]
    return JsonResponse({**error_code.CLACK_SUCCESS, "trace_list": result})


# 从txt文件中导入场景
def import_trace(request):
    request_json = json.loads(request.body)
    filename = request_json['name']
    try:
        with open('E:/Code/project301/file/' + filename, 'r', encoding='utf-8') as f:
            original_file = f.read()
            lines = original_file.splitlines()
        index = 0
        if Trace.objects.filter().exists():
            latest_trace = Trace.objects.latest('id')
            latest_id = latest_trace.id
        else:
            latest_id = 1
        while index < len(lines):
            if '0' <= lines[index][0] <= '9':
                index += 1
                new_name = "场景" + str(latest_id)
                latest_id += 1
                new_content = ""
                new_details = ""
                new_describe = ""
                # 判断是否为中文
                if '\u4e00' <= lines[index][0] <= '\u9fff':
                    new_details += lines[index] + '\n'
                    index += 1

                # 判断是否是trace
                if lines[index] == "Trace:":
                    index += 1
                    # 截取第一句放入介绍中
                    new_describe = lines[index]
                while index < len(lines) and (lines[index][0] <= '0' or lines[index][0] >= '9'):
                    new_content = new_content + lines[index] + '\n'
                    index += 1

                trace = Trace(trace_name=new_name,
                              trace_content=new_content,
                              trace_details=new_details,
                              trace_describe=new_describe)
                trace.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "content": original_file})


# 增加失效场景
def add_invalid(request):
    request_json = json.loads(request.body)
    try:
        invalid = Invalid(invalid_name=request_json['name'],
                          invalid_content=request_json['content'],
                          invalid_describe=request_json['describe'],
                          invalid_details=request_json['details'])
        invalid.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 修改失效场景
def edit_invalid(request):
    request_json = json.loads(request.body)
    aim_id = request_json['id']
    new_name = request_json['name']
    new_content = request_json['content']
    new_describe = request_json['describe']
    new_details = request_json['details']

    if not Invalid.objects.filter(id=aim_id).exists():
        return JsonResponse({**error_code.CLACK_NOT_EXISTS})
    try:
        Invalid.objects.filter(id=aim_id).update(invalid_name=new_name)
        Invalid.objects.filter(id=aim_id).update(invalid_content=new_content)
        Invalid.objects.filter(id=aim_id).update(invalid_describe=new_describe)
        Invalid.objects.filter(id=aim_id).update(invalid_details=new_details)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": str(e)})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除场景
def delete_invalid(request):
    request_json = json.loads(request.body)
    aim_id = request_json['invalid_id']
    try:
        Invalid.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 查询全部场景
def invalid_list(request):
    invalids = Invalid.objects.all()
    result = [invalid.to_dict() for invalid in invalids]
    return JsonResponse({**error_code.CLACK_SUCCESS, "invalid_list": result})


# 从txt文件中导入场景
def import_invalid(request):
    request_json = json.loads(request.body)
    filename = request_json['name']
    try:
        with open('E:/Code/project301/file/' + filename, 'r', encoding='utf-8') as f:
            original_file = f.read()
            lines = original_file.splitlines()
        if Invalid.objects.filter().exists():
            latest_invalid = Invalid.objects.latest('id')
            latest_id = latest_invalid.id
        else:
            latest_id = 1
        index = 0
        while index < len(lines):
            # 判断是否是Transition
            if lines[index] == "Transition:":
                index += 1
                new_name = "失效场景" + str(latest_id)
                latest_id += 1
                new_content = ""
                new_details = "暂无文字表述"
                # 截取第一句放入介绍中
                new_describe = lines[index]
                while index < len(lines) and lines[index] != "Transition:":
                    new_content = new_content + lines[index] + '\n'
                    index += 1
                invalid = Invalid(invalid_name=new_name,
                                  invalid_content=new_content,
                                  invalid_details=new_details,
                                  invalid_describe=new_describe)
                invalid.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "content": original_file})