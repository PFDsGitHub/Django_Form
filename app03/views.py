from django.shortcuts import render
from django.shortcuts import HttpResponse
from app01 import models
import json


def serialize(request):

    return render(request, 'serialize.html')


"""
def get_data(request):
    user_list = models.UserInfo.objects.all()

    return render(request, 'get_data.html', {'user_list':user_list})
"""


def get_data(request):
    from django.core import serializers

    ret = {'status':True, 'data':None}
    try:
        # user_list = models.UserInfo.objects.all()
        # QuerySet[obj,obj,obj]
        # 前端还要反序列化
        # var v = JSON.parse(arg.data)
        # ret['data'] = serializers.serialize('json', user_list)

         user_list = models.UserInfo.objects.all().values('id','username')
         # QuerySet[dict,dict,dict]
         # console.log(arg.data)
         ret['data'] = list(user_list)
    except Exception as e:
        ret['status'] = False
    result = json.dumps(ret)

    return HttpResponse(result)
