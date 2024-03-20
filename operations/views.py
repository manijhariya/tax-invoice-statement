import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from etl.models import InvoiceData


def index(request):
    """
    The `index` function retrieves unique broker names from the `InvoiceData` model and renders them in
    a template for display.

    :param request: The `request` parameter in the `index` function is an object that contains
    information about the current HTTP request. It includes details such as the request method (GET,
    POST, etc.), request headers, request data, and more. In this code snippet, the function checks if
    the request method is
    :return: The `index` view function returns a list of unique broker names extracted from the
    `InvoiceData` model in the database when the HTTP method is "GET". This list is then passed to the
    "reporting.html" template as a context variable named "brokers". If the request method is not "GET",
    it returns an HTTP 400 Bad Request response with the message "Method Not Allowed".
    """
    if request.method == "GET":
        query_results = InvoiceData.objects.raw(
            "SELECT Xref, Broker FROM etl_invoicedata"
        )
        result_list = [""]
        for item in query_results:
            result_list.append(item.Broker)
        return render(request, "reporting.html", {"brokers": list(set(result_list))})
    else:
        return HttpResponseBadRequest("Method Not Allowed")


def report_total_load_amount(request):
    """
    This Python function retrieves and sums up total loan amounts from a database table based on
    settlement dates and returns the results in a JSON response.

    :param request: The function `report_total_load_amount` takes a request object as a parameter. It
    checks if the request method is "POST" and then executes a raw SQL query to retrieve data from the
    `InvoiceData` model. The query calculates the total loan amount grouped by the "Settlement Date"
    field
    :return: The function `report_total_load_amount` returns a JSON response containing the status
    "Pass" and a list of dictionaries with the keys "Settlement Date" and "Total Loan Amount". The data
    in the list is retrieved from the database query results where the total loan amount is summed up
    based on the Settlement Date. If the request method is not POST, it returns an HTTP 400 Bad Request
    response
    """
    if request.method == "POST":
        query_results = InvoiceData.objects.raw(
            "SELECT  `Settlement Date` AS Date, Xref, SUM(`Total Loan Amount`) AS `total_loan_amount` FROM etl_invoicedata GROUP BY `Settlement Date`;"
        )

        result_list = []
        for item in query_results:
            if item:
                result_list.append(
                    {
                        "Settlement Date": item.Date,
                        "Total Loan Amount": round(item.total_loan_amount, 4),
                    }
                )
        return JsonResponse({"status": "Pass", "details": result_list})
    else:
        return HttpResponseBadRequest("Method Not Allowed")


def report_number_of_loans(request):
    """
    This Python function retrieves the number of loans grouped by settlement date and tier from a
    database table and returns the results in a JSON response for a POST request.

    :param request: The `report_number_of_loans` function takes a request object as a parameter. It
    checks if the request method is "POST", and if so, it executes a raw SQL query to retrieve data from
    the `InvoiceData` model. The query calculates the number of loans grouped by `Settlement
    :return: A JSON response containing the status "Pass" and details of the settlement date, tier, and
    number of loans for each item in the query results is being returned.
    """
    if request.method == "POST":
        query_results = InvoiceData.objects.raw(
            "SELECT Xref, `Settlement Date` AS Date, Tier, COUNT(*) AS num_loans FROM etl_invoicedata GROUP BY `Settlement Date`, Tier;"
        )

        result_list = []
        for item in query_results:
            if item:
                result_list.append(
                    {
                        "Settlement Date": item.Date,
                        "Tier": item.Tier,
                        "Number of Loans": item.num_loans,
                    }
                )
        return JsonResponse({"status": "Pass", "details": result_list})

    else:
        return HttpResponseBadRequest("Method Not Allowed")


def highest_loan_amount(request):
    """
    This Python function retrieves the highest loan amount associated with a specific broker from a
    database table and returns the result in a JSON response.

    :param request: The `highest_loan_amount` function you provided is designed to retrieve the highest
    loan amount associated with a specific broker from the `InvoiceData` table. It takes a POST request
    containing the broker's name as a parameter
    :return: The function `highest_loan_amount` returns a JSON response containing the status "Pass" and
    details of the highest loan amount associated with a specific broker. The details include the
    broker's name and the highest loan amount found in the database for that broker. If the request
    method is not POST, it returns an HTTP response indicating that the method is not allowed.
    """
    if request.method == "POST":
        broker_name = json.loads(request.body).get("broker")
        if not broker_name:
            return HttpResponseBadRequest("Broker name is required")

        query_results = InvoiceData.objects.raw(
            f"SELECT Xref, MAX(`Total Loan Amount`) AS highest_loan_amount FROM etl_invoicedata WHERE Broker = '{broker_name}'"
        )

        result_list = []
        for item in query_results:
            if item:
                result_list.append(
                    {
                        "Broker": broker_name,
                        "Highest Loan Amount": item.highest_loan_amount,
                    }
                )
        return JsonResponse({"status": "Pass", "details": result_list})
    else:
        return HttpResponseBadRequest("Method Not Allowed")


def diff_dates_month(date1, date2):
    """
    The function `diff_dates_month` calculates the difference in months between two dates using the
    `relativedelta` function.

    :param date1: It looks like you are trying to calculate the difference in months between two dates
    using the `relativedelta` function. However, the code snippet you provided is incomplete. Could you
    please provide the missing part of the code or let me know how I can assist you further with this
    function?
    :param date2: It seems like you were about to provide some information about the `date2` parameter,
    but the message got cut off. Could you please provide more details or complete the sentence so that
    I can assist you better?
    :return: the difference in months between the two input dates, `date2` and `date1`, using the
    `relativedelta` function.
    """
    return relativedelta(date2 - date1).months


def broker_report(request):
    """
    This Python function generates a broker report based on the total loan amounts for a specific broker
    grouped by settlement date.

    :param request: The `broker_report` function you provided seems to be handling a POST request to
    generate a report based on broker data from an InvoiceData model. It retrieves the total loan amount
    grouped by settlement date for a specific broker
    :return: The `broker_report` function is returning a list of dictionaries containing information
    about the total loan amount for a specific broker on different settlement dates. The information
    includes the broker's name, the settlement date, the total loan amount, and the period (which is set
    to "Daily" for each entry). The results are sorted based on the settlement date before being
    returned.
    """
    if request.method == "POST":
        broker_name = json.loads(request.body).get("broker")
        if not broker_name:
            return HttpResponseBadRequest("Broker name is required")
        query_results = InvoiceData.objects.raw(
            f"SELECT Xref, SUM(`Total Loan Amount`) as total_loan_amount, `Settlement Date` AS Date FROM etl_invoicedata WHERE Broker = '{broker_name}' GROUP BY `Settlement Date`"
        )
        result_list = []
        for item in query_results:
            if item:
                result_list.append(
                    {
                        "Broker": broker_name,
                        "Date": item.Date,
                        "Total Loan Amount": item.total_loan_amount,
                        "Period": "Daily",
                    }
                )
        result_list = sorted(result_list, key=lambda x: x["Date"])

        if len(result_list) > 0:
            start_date_week = result_list[0]["Date"]
            start_date_month = result_list[0]["Date"]
            duration_week = {str(start_date_week): result_list[0]["Total Loan Amount"]}
            duration_month = {
                str(start_date_month): result_list[0]["Total Loan Amount"]
            }

            for result_ in result_list[1:]:
                period = abs((start_date_week - result_["Date"]).days)
                if period == 7:
                    duration_week[f"{str(start_date_week)}-{str(result_['Date'])}"] = (
                        duration_week[str(start_date_week)]
                    )
                elif period < 7:
                    duration_week[str(start_date_week)] += result_["Total Loan Amount"]
                else:
                    duration_week[result_["Date"]] = result_["Total Loan Amount"]
                    start_date_week = result_["Date"]

                period = diff_dates_month(start_date_month, result_["Date"])
                if period == 1:
                    duration_month[
                        f"{str(start_date_month)}-{str(result_['Date'])}"
                    ] = duration_month[str(start_date_month)]
                elif period < 1:
                    duration_month[str(start_date_month)] += result_[
                        "Total Loan Amount"
                    ]
                else:
                    duration_month[result_["Date"]] = result_["Total Loan Amount"]
                    start_date_month = result_["Date"]

        for dur_key, dur_value in duration_week.items():
            result_list.append(
                {
                    "Broker": broker_name,
                    "Date": dur_key,
                    "Total Loan Amount": dur_value,
                    "Period": "Weekly",
                }
            )
        for dur_key, dur_value in duration_month.items():
            result_list.append(
                {
                    "Broker": broker_name,
                    "Date": dur_key,
                    "Total Loan Amount": dur_value,
                    "Period": "Month",
                }
            )

        return JsonResponse({"status": "Pass", "details": result_list})
    else:
        return HttpResponseBadRequest("Method Not Allowed")


def total_loan_amount_by_time(request):
    """
    This Python function calculates the total loan amount within a specified time range based on invoice
    data.

    :param request: The function `total_loan_amount_by_time` is designed to calculate the total loan
    amount within a specified time range. It takes a POST request with JSON data containing a start date
    and an end date. The function then converts these dates to datetime objects, performs a SQL query to
    retrieve the total loan amount
    :return: The function `total_loan_amount_by_time` returns a JSON response containing the status
    "Pass" and a list of dictionaries with details including the start date, end date, and total loan
    amount for a given time period.
    """
    if request.method == "POST":
        start_date = json.loads(request.body).get("start_date")
        end_date = json.loads(request.body).get("end_date")

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        except Exception as e:
            return HttpResponseBadRequest("Enter a valid start and end date")

        query_results = InvoiceData.objects.raw(
            f"SELECT Xref, SUM(`Total Loan Amount`) AS total_loan_amount FROM etl_invoicedata WHERE `Settlement Date` BETWEEN '{start_date}' AND '{end_date}'"
        )

        result_list = []
        for item in query_results:
            if item:
                result_list.append(
                    {
                        "Start Date": start_date,
                        "End Date": end_date,
                        "Total Loan Amount": round(item.total_loan_amount, 4),
                    }
                )

        return JsonResponse({"status": "Pass", "details": result_list})
    else:
        return HttpResponseBadRequest("Method Not Allowed")
