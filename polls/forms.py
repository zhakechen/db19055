"""zhake chen"""
import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

# 正则匹配用户名长度
from polls.models import User

USERNAME_PATTERN = re.compile(r'\w{5,20}')
# 正则匹配电话号码
TEL_PATTERN = re.compile(r'1[3-9]\d{9}')


class LoginForm(forms.Form):
    """对用户名的验证"""
    username = forms.CharField(required=True,
                               error_messages={
                                   'required': '请输入用户名',
                               })
    """对密码的验证"""
    password = forms.CharField(required=True,
                               strip=False,
                               min_length=8,
                               error_messages={
                                   'required': '请输入用户口令',
                                   'min_length': '用户口令至少8个字符'
                               })
    captcha = forms.CharField(required=True,
                              min_length=4,
                              max_length=4,
                              error_messages={
                                  'required': '请提供有效的验证码',
                                  'min_length': '验证码是四位哦',
                                  'max_length': '验证码是四位哦'
                              })

    def clean_username(self):
        """正则验证用户名"""
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('用户名有数字，字母下划线划线构成且长度为5-20')
        return username


class RegisterForm(forms.Form):
    username = forms.CharField(required=True,
                               min_length=8,
                               error_messages={'required': '输名字'})
    password = forms.CharField(required=True,
                               min_length=5,
                               max_length=20,
                               error_messages={'required': '输密码', 'min_length': '请输入最少5个字符'})
    repassword = forms.CharField(required=True,
                                 strip=False,
                                 error_messages={'required': '再输密码'})
    email = forms.EmailField(required=True,
                             help_text='请输入正确的邮箱地址',
                             error_messages={'required': '输邮箱'})
    tel = forms.CharField(required=True,
                          error_messages={'required':'请输入手机号'})
    mobliecode = forms.CharField(required=True,
                                 error_messages={'required':'请输入手机验证码'})
    agreement = forms.CharField(required=True,
                                error_messages={'required':'需勾选本网站服务条款'})


    def clean_username(self):
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('用户名由字母，数字，下划线构成且长度为5-20')
        user = User.objects.filter(username=username).first()
        if user:
            raise ValidationError('用户名已经被注册，请更换你的用户名')
        return username

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if not TEL_PATTERN.fullmatch(tel):
            raise ValidationError('请输入有效的手机号码')
        return tel

    def clean_repassword(self):
        password = self.cleaned_data['password']
        repassword = self.cleaned_data['repassword']
        if password != repassword:
            raise ValidationError('用户口令和确认口令不一致')
        return make_password(password)

