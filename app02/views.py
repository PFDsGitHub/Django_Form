from django.shortcuts import render
from django import forms
from django.forms import fields
from django.forms import widgets
from app01 import models


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
