from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('download_file/<str:filename>/', views.download_file, name='download_file'),
    path('open/<str:file_name>/', views.open_file, name='open_file'),
]