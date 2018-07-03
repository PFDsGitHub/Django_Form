from django.shortcuts import render
from django import forms
from django.forms import fields
from django.forms import widgets


class TestForm(forms.Form):
    user = fields.CharField(
        required=True,
        max_length=12,
        min_length=3,
        error_messages={},
        # widget=widgets.Select(), # 定制HTML插件
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


def test(request):
    if request.method == 'GET':
        obj = TestForm()
        return render(request, 'test.html', {'obj':obj})
    else:
        print(123454)
        obj = TestForm(request.POST, request.FILES)
        obj.is_valid()
        print(obj.cleaned_data)
        return render(request, 'test.html', {'obj':obj})
