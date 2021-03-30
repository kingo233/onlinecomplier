from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from App.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import os
import subprocess


def runcmd(command, input=None, timeout=1):
    res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True)
    sout, serr = res.communicate(input)
    return res.returncode, sout, serr


def runcpp(code, inputdata):
    f = open('code.cpp', 'w')
    f.write(code)
    f.close()
    complie_res = runcmd(["g++ code.cpp"])
    if complie_res[0] == 0:
        run_res = runcmd(["./a.out"], inputdata)
        if run_res[0] == 0:
            return run_res[1]
        else:
            return "Run time error!"
    else:
        return complie_res[2]


def runc(code, inputdata):
    f = open('cpde.c', 'w')
    f.write(code)
    f.close()
    complie_res = runcmd(["gcc code.c"])
    if complie_res[0] == 0:
        run_res = runcmd(["./a.out"], inputdata)
        if run_res[0] == 0:
            return run_res[1]
        else:
            return "Run time error!"
    else:
        return complie_res[2]


def runpython(code, inputdata):
    f = open('code.py', 'w')
    f.write(code)
    f.close()
    run_res = runcmd(["python3 code.py"], inputdata)
    if run_res[0] == 0:
        return run_res[1]
    else:
        return run_res[2]


# Create your views here.
def home(request):
    # return HttpResponse("首页")
    users = User.objects.all()
    return render(request, "index.html", context={"title": "Django", "name": "nannan", "users": users})


@csrf_exempt
def editor(request):
    if request.method == 'GET':
        return render(request, "editor.html")
    else:
        code = request.POST['code']
        inputdata = request.POST['inputdata']
        lang = request.POST['lang']
        lang_handle_dict = {'C++': runcpp, 'C': runc, 'Python': runpython}
        if lang == 'JAVA':
            return JsonResponse({"msg": "该语言暂不支持！"})

        return JsonResponse({"msg": lang_handle_dict[lang](code,inputdata)})
