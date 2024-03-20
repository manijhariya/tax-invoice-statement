from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from .logic import extract_data_from_pdf
from .models import InvoiceData


def index(request):
    """
    The `index` function checks the request method and returns a rendered template for a GET request, or
    a "Method Not Allowed" response for other request methods.

    :param request: The `request` parameter in the code snippet represents an HTTP request object that
    is sent to the server. It contains information such as the request method (GET, POST, etc.),
    headers, user data, and any data sent in the request body. In this code snippet, the function
    `index`
    :return: In the provided code snippet, if the request method is "GET", the function returns a call
    to the `render` function with parameters `template_name="index.html"` and `request=request`.
    However, if the request method is not "GET", the function does not return anything explicitly. It
    should be corrected to return an `HttpResponseBadRequest` object in the else block.
    """
    if request.method == "GET":
        return render(template_name="index.html", request=request)
    else:
        HttpResponseBadRequest("Method Not Allowed")


def upload_file(request):
    """
    The `upload_file` function handles file uploads, saves the file to a specified location, extracts
    data from a PDF file, and bulk creates records in the `InvoiceData` model.

    :param request: The `request` parameter in the `upload_file` function is typically an HttpRequest
    object that represents the HTTP request made by the client. It contains information about the
    request, such as the method used (GET, POST, etc.), any data sent in the request (such as form data
    or files),
    :return: A JsonResponse with the status "Pass" and details "File Upload Successfully!" is being
    returned if the request method is "POST" and the file is successfully uploaded and processed. If the
    request method is not "POST", an HttpResponseBadRequest with the message "Method Not Allowed" is
    being returned.
    """
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            HttpResponseBadRequest("Please Upload a valid file first")

        fss = FileSystemStorage(location=settings.UPLOAD_FILES)
        filename = fss.save(file.name, file)

        data = extract_data_from_pdf(filename)
        InvoiceData.objects.bulk_create(
            InvoiceData(**vals) for vals in data.to_dict(orient="records")
        )

        return JsonResponse({"status": "Pass", "details": "File Upload Successfully!"})
    else:
        HttpResponseBadRequest("Method Not Allowed")
