from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate,login

# Create your views here.
from django.views.generic.base import View
from users.models import UserProfile
from utils.email_send import send_register_eamil
# 引入登录表单验证
from .forms import LoginForm,RegisterForm

# 邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
# 登录
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        # 实例化登录表单验证
        login_form = LoginForm(request.POST)
        # 实例化验证合法
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象，失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        # 表单验证不合法
        else:
            return render(request,'login.html',{'login_form':login_form})
# 注册
class RegisterView(View):
    # 用户注册
    def get(self,request):
        register_form = RegisterForm();
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        '''表单验证通过'''
        if register_form.is_valid():
            user_name = request.POST.get('email',None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email = user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已存在'})
            pass_word = request.POST.get('password',None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库中的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})