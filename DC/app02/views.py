
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import loginForm  # 导入你的登录表单
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import loginForm  # 导入你的表单类
from . import models
import json
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
def user_add(request):
    if request.method == "GET":
        form = loginForm()
        return render(request, 'user_add.html', {'form': form, 'num': 0})  # 初始时 num 设置为 0
    else:
        form = loginForm(data=request.POST)
        if form.is_valid():
            username_ = form.cleaned_data['username']
            if models.UserInfo.objects.filter(username=username_).exists():
                messages.error(request, '用户名已存在')
                return render(request, 'user_add.html', {'form': form, 'num': 1})  # 注册失败，显示错误信息
            else:
                form.save()
                messages.success(request, '用户注册成功')  # 保存成功后添加成功消息
                return redirect('/login/')  # 注册成功后直接重定向到登录页面
        else:
            messages.error(request, '表单数据无效')
            return render(request, 'user_add.html', {'form': form, 'num': 0})  # 表单数据无效，重新显示表单页面
def user_login(request):
    if request.method == "GET":
        form = loginForm()

        # 从 Cookie 中获取用户名和密码，并自动填充到登录表单中
        username = request.COOKIES.get('username', '')
        password = request.COOKIES.get('password', '')
        remember = request.COOKIES.get('remember', False)
        form.fields['username'].initial = username
        form.fields['password'].initial = password

        return render(request, 'login.html', {'form': form, 'remember': remember})
    else:
        form = loginForm(data=request.POST)
        if form.is_valid():
            username_ = form.cleaned_data['username']
            password_ = form.cleaned_data['password']
            if models.UserInfo.objects.filter(username=username_, password=password_).exists():
                uid = username_
                checkbox_data = request.POST.get('remember')
                if checkbox_data == 'on':
                    # 记住密码，将用户名和密码存储在 Cookie 中，有效期14天
                    response = redirect(uid + '/home/')
                    response.set_cookie('username', username_, expires=timezone.now() + timedelta(days=14))
                    response.set_cookie('password', password_, expires=timezone.now() + timedelta(days=14))
                    response.set_cookie('remember', True, expires=timezone.now() + timedelta(days=14))
                    # 检查用户是否已经有在线记录，如果有，则更新时间戳；如果没有，则创建记录
                    return response
                else:
                    return redirect(uid + '/home/')
            else:
                num = 1
                form = loginForm()
                return render(request, 'login.html', {'form': form, 'num': num})
        else:
            return render(request, 'login.html', {'form': form})

def logout(request):
    # 获取当前登录用户的用户名
    username = request.user.username
    # 删除在线用户记录
    models.OnlineUser.objects.filter(username__username=username).delete()
    # 重定向到登录页面
    return redirect('/login/')


def home(request, username_):
    new_username = request.session.get('new_username')
    online_user = models.UserInfo.objects.filter(username=username_).first()

    if online_user:
        id_ = online_user.id
        name = models.NameToUser.objects.filter(user_info_id=id_).values_list('name', flat=True).first()
        default_name = name if name else "默认名字"
    else:
        default_name = "默认名字"

    if request.method == "GET":
        return render(request, 'home.html', {'uid': username_, 'name': default_name})
    elif request.method == "POST":
        data = json.loads(request.body)
        newname = data.get("new_username", "").strip()
        username_ = data.get("account")

        if online_user:
            rename(newname, online_user.id)
            return JsonResponse({"message": "用户名修改成功"}, status=200)
        else:
            return JsonResponse({"error": "找不到对应的用户名记录"}, status=404)
    else:
        num = 123
        form = loginForm()
        return render(request, 'home.html', {'form': form, 'num': num, 'uid': online_user.id if online_user else None, 'name': default_name})
def rename(newname, username_):
    try:
        if not newname:
            return JsonResponse({"error": "新用户名不能为空"}, status=400)

        # 查找用户信息
        user_info = models.UserInfo.objects.filter(id=username_).first()
        if not user_info:
            return JsonResponse({"error": "无法找到与给定用户名相关联的用户信息"}, status=404)

        # 尝试获取与用户信息相关联的用户名记录
        user_entry = models.NameToUser.objects.filter(user_info_id=user_info.id).first()

        if user_entry:
            # 如果找到用户名记录，则更新用户名
            user_entry.name = newname
            user_entry.save()
        else:
            # 如果找不到用户名记录，则创建新的用户名记录
            models.NameToUser.objects.create(user_info_id=user_info.id, name=newname)

        # 如果修改用户名成功，返回成功消息
        return JsonResponse({"message": "用户名修改成功"}, status=200)
    except Exception as e:
        # 如果修改用户名时出现异常，返回错误消息
        return JsonResponse({"error": str(e)}, status=500)
