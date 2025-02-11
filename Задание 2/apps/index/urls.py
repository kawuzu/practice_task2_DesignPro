from django.urls import path

from .views import index_page, register, login_view, logout_user, dashboard, admin_dashboard

urlpatterns = [
    path('', index_page, name='index_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
path('admin/', admin_dashboard, name='admin_dashboard'),
]
