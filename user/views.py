from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def user_logout(requset):
    logout(requset)

    return redirect('login')


def user_profile(request):
    return render(request, 'user/profile.html')


def user_login(request):
    message = ''
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('register'):
            return redirect('register')

        if request.POST.get('login'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            if password == '' or username == '':
                message = '帳密不能爲空'
            else:
                # 登入動作
                user = authenticate(
                    request, username=username, password=password)
                if not user:
                    # 篩選姓名
                    if User.objects.filter(username=username):
                        message = '密碼錯誤'
                    else:
                        message = '帳號有誤'
                else:
                    login(request, user)
                    message = '登入成功'
                    return redirect('profile')

    return render(request, 'user/login.html', {'message': message})


def user_register(request):
    message = ''
    form = UserCreationForm()
    if request.method == 'GET':
        print('GET')

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(username, password1, password2)

            if len(password1) < 8:
                message = '密碼過短'
            elif password1 != password2:
                message = '兩次密碼不同'
            else:
                if User.objects.filter(username=username).exists():
                    message = '帳號重複'
                else:
                    user = User.objects.create_user(
                        username=username, password=password1)
                    user.save()
                    login(request, user)
                    message = '註冊成功!'
                    return redirect('profile')
                # 　帳號重複檢查
        except Exception as e:
            print(e)
            message = '註冊失敗'
    return render(request, 'user/register.html', {'form': form, 'message': message})
