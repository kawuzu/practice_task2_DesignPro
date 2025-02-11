from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('delete/<int:request_id>/', views.delete_request, name='delete_request'),
    path('admin/categories/', views.admin_category_management, name='admin_category_management'),
    path('admin/requests/', views.admin_request_list, name='admin_request_list'),
    path('edit/<int:request_id>/', views.change_request_status, name='request_detail'),
]
