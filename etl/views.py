from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

from django.conf import settings

def index(request):
    return render(template_name="index.html", request=request)


def upload_file(request):
    file = request.FILES.get("file")

    fss = FileSystemStorage(location=settings.UPLOAD_FILES)
    filename = fss.save(file.name, file)

    print(filename)
    return JsonResponse({"status" : "Pass", "details" : "File Upload Successfully!"})
