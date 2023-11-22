from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def user_logout(requset):
    logout(requset)

    return redirect('login')


@login_required
def user_profile(requset, id):
    user = None
    try:
        user = User.objects.get(pk=id)
    except Exception as e:
        print(e)

    return render(requset, 'user/profile.html', {'user': user})


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
                message = '帳號跟密碼不能為空'
            else:
                # 登入動作
                user = authenticate(
                    request, username=username, password=password)
                print(user)
                if not user:
                    # 篩選帳號
                    if User.objects.filter(username=username):
                        message = '密碼錯誤!'
                    else:
                        message = '帳號錯誤!'
                else:
                    login(request, user)
                    message = '登入成功!'
                    return redirect('todolist')

    return render(request, 'user/login.html', {'message': message})

# Create your views here.


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
                    return redirect('todolist')
                # 　帳號重複檢查
        except Exception as e:
            print(e)
            message = '註冊失敗'

    return render(request, 'user/register.html', {'form': form, 'message': message})
