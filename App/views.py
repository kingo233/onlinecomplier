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
        f = open('code.cpp', 'w')
        f.write(code)
        f.close()
        complie_res = runcmd(["D:\\Dev-Cpp\\MinGW64\\bin\\g++.exe", "code.cpp"])
        if complie_res[0] == 0:
            run_res = runcmd(["a.exe"], inputdata)
            if run_res[0] == 0:
                return JsonResponse({"msg": run_res[1]})
            else:
                return JsonResponse({"msg": "Run time error!"})
        else:
            return JsonResponse({"msg": complie_res[2]})
