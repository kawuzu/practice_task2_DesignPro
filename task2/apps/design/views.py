from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Request, Category


@login_required
def create_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        photo = request.FILES.get('photo')

        if not title or not description or not category_id:
            messages.error(request, 'Все поля являются обязательными.')
            return render(request, 'create_request.html', {'categories': Category.objects.all()})

        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2 Мб
                messages.error(request, 'Размер фото не должен превышать 2 Мб.')
                return render(request, 'create_request.html', {'categories': Category.objects.all()})
            if not photo.name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                messages.error(request, 'Фото должно быть в формате JPG, JPEG, PNG или BMP.')
                return render(request, 'create_request.html', {'categories': Category.objects.all()})

        category = Category.objects.get(id=category_id)
        request_obj = Request.objects.create(
            title=title,
            description=description,
            category=category,
            photo=photo,
            user=request.user,
            status='Новая'
        )
        messages.success(request, 'Заявка успешно создана.')
        return redirect('dashboard')

    return render(request, 'create_request.html', {'categories': Category.objects.all()})


@login_required
def delete_request(request, request_id):
    request_user = Request.objects.get(id=request_id)
    if request.method == 'POST':
        request_user.delete()
        return redirect('dashboard')
    return render(request, 'delete_request.html', {'request_user': request_user})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_category_management(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_category':
            name = request.POST.get('category_name')
            if name:
                Category.objects.create(name=name)
        elif action == 'delete_category':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            category.delete()

    return render(request, 'admin_category_management.html', {'categories': categories})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_request_list(request):
    requests = Request.objects.all()

    return render(request, 'admin_request_list.html', {'requests': requests})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def change_request_status(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        comment = request.POST.get('comment')
        image = request.FILES.get('image')

        if request_obj.status == 'Новая' or request_obj.status == 'Принято в работу':
            if new_status == 'Выполнено':
                if not image:
                    messages.error(request, 'Для смены статуса на "Выполнено" необходимо прикрепить изображение дизайна.')
                    return redirect('request_detail', request_id=request_obj.id)
                request_obj.status = new_status
                request_obj.image = image
                request_obj.comment = comment
                request_obj.save()
                messages.success(request, 'Статус заявки успешно изменен на "Выполнено".')
            elif new_status == 'Принято в работу':
                if not comment:
                    messages.error(request, 'Для смены статуса на "Принято в работу" необходимо указать комментарий.')
                    return redirect('request_detail', request_id=request_obj.id)
                request_obj.status = new_status
                request_obj.comment = comment
                request_obj.save()
                messages.success(request, 'Статус заявки успешно изменен на "Принято в работу".')
            else:
                messages.error(request, 'Недопустимый статус.')
        else:
            messages.error(request, 'Вы не можете изменить статус заявки, которая не находится в статусе "Новая".')

    return render(request, 'change_request_status.html', {'request_obj': request_obj})
