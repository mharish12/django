import os
import pandas as pd
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        return redirect('admin_panel')
    return render(request, 'home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            return redirect('admin_panel')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid Credentials'})
    return render(request, 'admin_login.html')

def admin_panel(request):
    files = []
    for file_name in os.listdir(settings.MEDIA_ROOT):
        if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            files.append((file_name, os.path.getsize(file_path)))
    return render(request, 'admin.html', {'files': files})

def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def open_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return HttpResponse('Invalid File Type')
        return render(request, 'open_file.html', {'file_name': file_name, 'table_html': df.to_html(index=False)})
    raise Http404
