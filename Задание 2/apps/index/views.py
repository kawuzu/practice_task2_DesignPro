import re

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from apps.design.models import Request


def index_page(request):
    completed_requests = Request.objects.filter(status='Выполнено').order_by('-created_at')[:4]
    in_progress_count = Request.objects.filter(status='Принято в работу').count()
    return render(request, 'index.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count
    })

@login_required
def dashboard(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_requests': user_requests})


def logout_user(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        consent = request.POST.get('consent')

        errors = {}

        if not re.match(r'^[А-Яа-яЁё\s-]+$', full_name):
            errors['full_name'] = 'ФИО должно содержать только кириллические буквы, пробелы и дефисы.'

        if not re.match(r'^[a-zA-Z-]+$', username):
            errors['username'] = 'Логин должен содержать только латиницу и дефисы.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Логин уже занят.'

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors['email'] = 'Введите корректный email адрес.'

        if not password:
            errors['password'] = 'Пароль обязателен.'
        elif password != password_repeat:
            errors['password_repeat'] = 'Пароли не совпадают.'

        if not consent:
            errors['consent'] = 'Необходимо согласие на обработку персональных данных.'

        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, 'registration.html', {'errors': errors})

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('login')

    return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index_page')
        else:
            messages.error(request, 'Неверный логин или пароль. Пожалуйста, попробуйте еще раз.')

    return render(request, 'login.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'manage_requests':
            return redirect('admin_request_list')
        elif action == 'manage_categories':
            return redirect('admin_category_management')
        else:
            messages.error(request, 'Invalid action selected.')

    return render(request, 'admin_dashboard.html')