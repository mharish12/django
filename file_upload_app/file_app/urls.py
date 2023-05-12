from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_panel/", views.admin_panel, name="admin_panel"),
    path("upload/", views.upload, name="upload"),
    # path("download/", views.download, name="download"),
    path("download_file/<str:file>/", views.download_file, name="download_file"),
    # path("open/", views.open, name="open"),
    path("open_file/<str:file>/", views.open_file, name="open_file"),
]
