import os
import pandas as pd
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


@login_required(login_url="/admin/")
def home(request):
    try:
        if request.method == "POST" and request.FILES["file"]:
            myfile = request.FILES["file"]
            fs = FileSystemStorage()
            fs.save(myfile.name, myfile)
            return redirect("admin_panel")
    except Exception as e:
        exception = {"exception": e, "messages": "Upload failed with exception."}
        print("Execption printing: ", e)
        return render(request, "error.html", exception)

    return render(request, "home.html")


@login_required(login_url="/admin/")
def admin_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if username == "admin" and password == "admin":
                return redirect("admin_panel")
            else:
                return render(
                    request, "admin_login.html", {"error": "Invalid Credentials"}
                )
    except Exception as e:
        exception = {"exception": e, "messages": "Upload failed with exception."}
        print("Execption printing: ", e)
        return render(request, "error.html", exception)

    return render(request, "admin_login.html")


@login_required(login_url="/admin/")
def admin_panel(request):
    files = []
    try:
        # file_name = request.file
        temp = os.listdir(settings.MEDIA_ROOT)
        print("list dir exec")
        for file_name in temp:
            if (
                file_name.endswith(".csv") or file_name.endswith(".xlsx")
            ) and file_name != "":
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                files.append(
                    {"file_name": file_name, "size": os.path.getsize(file_path)}
                )
    except Exception as e:
        exception = {"exception": e, "messages": "Upload failed with exception."}
        print("Execption printing: ", e)
        return render(request, "error.html", exception)

    return render(request, "admin.html", {"files": files})


# @login_required(login_url="/admin/")
# def download(request):
#     return download_file(request, "test.csv")


@login_required(login_url="/admin/")
def download_file(request, file):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, file)
        if os.path.exists(file_path):
            with open(file_path, "rb") as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-excel"
                )
                response[
                    "Content-Disposition"
                ] = "inline; filename=" + os.path.basename(file_path)
                return response
    except Exception as e:
        exception = {"exception": e, "messages": "Upload failed with exception."}
        print("Execption printing: ", e)
        return render(request, "error.html", exception)
    raise Http404


# @login_required(login_url="/admin/")
# def open(request):
#     return open_file(request, "test.csv")


@login_required(login_url="/admin/")
def open_file(request, file, *args):
    try:
        print("file object: ", file)
        file_path = os.path.join(settings.MEDIA_ROOT, file)
        if os.path.exists(file_path):
            if file.endswith(".csv"):
                # print("file path: ", file_path)
                df = pd.read_csv(file_path)
            elif file.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                return HttpResponse("Invalid File Type")
            return render(
                request,
                "open_file.html",
                {"file": file, "table_html": df.to_html(index=True)},
            )
    except Exception as e:
        exception = {"exception": e, "messages": ["Upload failed with exception."]}
        print("Execption printing: ", e)
        return render(request, "error.html", exception)
    raise Http404


@login_required(login_url="/admin/")
def upload(request):
    try:
        if request.method == "POST" and request.FILES["file"]:
            myfile = request.FILES["file"]
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(
                request, "upload.html", {"uploaded_file_url": uploaded_file_url}
            )
    except Exception as e:
        exception = {"exception": e, "messages": "Upload failed with exception."}
        print("Execption printing: ", e)
        return render(request, "error.html", exception)
    return render(request, "upload.html")
