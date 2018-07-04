from django.shortcuts import render, redirect, HttpResponse
from django import forms
from django.forms import fields
from django.forms import widgets
from app01 import models
import json


class TestForm(forms.Form):
    user = fields.CharField(
        required=True,
        max_length=12,
        min_length=3,
        error_messages={},
        widget=widgets.TextInput(attrs={'class':'c1'}), # 定制HTML插件
        label='用户名',
        initial='请输入用户名',
        help_text='帮助信息',
        show_hidden_initial=True, # 插件后面加一个隐藏且具有默认值的插件（可用于检验两次输入是否一致）
        validators=[], # 自定义验证规则
        localize=True, # 是否支持本地化
        disabled=True, # 是否不能编辑
        label_suffix=':',
    )
    age = fields.IntegerField()

    email = fields.EmailField()

    img = fields.FileField()

    city = fields.ChoiceField(
        choices=[(1,'北京'),(2,'上海'),(3,'沙河'),],
        initial=2,
    )
    city = fields.TypedChoiceField(
        coerce=lambda x: int(x), # 类型转换 结果返回整型
        choices=[(1,'北京'),(2,'上海'),(3,'沙河'),],
        initial=2,
    )

    hobby = fields.MultipleChoiceField(
        choices=[(1,'a'),(2,'b'),(3,'c'),],
        initial=[1,2,],
    )

class Foo:

    def __str__(self):
        return "<input type='text'>"

def test(request):
    if request.method == 'GET':
        obj = TestForm()
        return render(request, 'test.html', {'obj':obj})
    else:
        obj = TestForm(request.POST, request.FILES)
        obj.is_valid()
        print(obj.cleaned_data)
        return render(request, 'test.html', {'obj':obj})


class LoveForm(forms.Form):
    price = fields.IntegerField()
    user_id = fields.IntegerField(
        # widget=widgets.Select(choices=[(0,'alex'),(1,'yuan'),(2,'egon'),])
        widget=widgets.Select()
    )

    # 自定制init 实现数据实时更新
    def __init__(self,*args,**kwargs):
        super(LoveForm, self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.choices = models.UserInfo.objects.values_list('id','username')

def love(request):
    obj = LoveForm()

    return render(request, 'love.html', {'obj':obj})


# 基于源码扩展
from django.core.exceptions import ValidationError
class AjaxForm(forms.Form):
    username = fields.CharField()
    user_id = fields.IntegerField(
        widget=widgets.Select(choices=[(0,'alex'),(1,'yuan'),(2,'egon'),])
    )
    # 自定义方法  clean_字段名
    # 必须返回值  self.cleaned_data['username']
    # 如果出错  raise ValidationError('用户名已存在')
    # 单独字段验证
    def clean_username(self):
        v = self.cleaned_data['username']
        if models.UserInfo.objects.filter(username=v).count():
            # 整体错了
            # 自己详细错误信息
            raise ValidationError('用户名已存在')
        return v

    # 单独字段验证
    def clean_user_id(self):
        return self.cleaned_data['user_id']

    # 整体验证
    def clean(self):
        value_dict = self.cleaned_data
        v1 = value_dict.get('username')
        v2 = value_dict.get('user_id')
        if v1 == 'root' and v2 == 1:
            raise ValidationError('整体错误信息')
        return self.cleaned_data


def ajax(request):
    if request.method == 'GET':
        obj = AjaxForm()
        return render(request, 'ajax.html', {'obj':obj})
    else:
        ret = {'status':None, 'message':None}
        obj = AjaxForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            # 跳转到百度
            ret['status'] = '钱'
            return HttpResponse(json.dumps(ret))
        else:
            print(obj.errors)
            # 错误信息显示到前端页面上
            ret['message'] = obj.errors
            return HttpResponse(json.dumps(ret))

