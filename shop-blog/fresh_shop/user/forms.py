import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):
    # required=True必填
    user_name = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '用户名必填',
                                                'max_length': '用户名最长20',
                                                'min_length': '用户名最短为5'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={'required': '密码必填',
                                          'max_length': '密码最长20',
                                          'min_length': '密码最短为8'})
    cpwd = forms.CharField(max_length=20, min_length=8, required=True,
                           error_messages={'required': '密码必填',
                                           'max_length': '密码最长20',
                                           'min_length': '密码最短为8'})
    email = forms.CharField(required=True, error_messages={'required': '邮箱必填'})
    allow = forms.BooleanField(required=True, error_messages={'required': '必须同意用户协议'})

    def clean_user_name(self):
        # 校验注册的账号是否已存在
        username = self.cleaned_data['user_name']
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该账号已存在，请更换账号再注册')
        return self.cleaned_data['user_name']

    def clean(self):
        # 校验密码是否一致
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data

    def clean_email(self):
        # 校验邮箱格式
        email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data['email']
        if not re.match(email_reg, email):
            raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '用户名未填',
                                                'max_length': '用户名最长20',
                                                'min_length': '用户名最短为5'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={'required': '密码未填',
                                          'max_length': '密码最长20',
                                          'min_length': '密码最短为8'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('pwd')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册，请先注册'})

        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=5, required=True,
                               error_messages={
                                   'required': '收件人必填',
                                   'max_length': '收件人姓名不超过5字符'
                               })
    address = forms.CharField(required=True,
                              error_messages={
                                   'required': '地址必填'
                               })
    postcode = forms.CharField(required=True, error_messages={
        'required': '邮编必填'
    })
    mobile = forms.CharField(required=True, error_messages={
        'required': '手机号码必填'
    })