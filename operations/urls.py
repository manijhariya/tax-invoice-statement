# Operations URLs module
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "report_total_load_amount/",
        views.report_total_load_amount,
        name="report_total_load_amount",
    ),
    path(
        "report_number_of_loans/",
        views.report_number_of_loans,
        name="report_number_of_loans",
    ),
    path(
        "highest_loan_amount/",
        views.highest_loan_amount,
        name="highest_loan_amount",
    ),
    path(
        "broker_report/",
        views.broker_report,
        name="broker_report",
    ),
    path(
        "total_loan_amount_by_time/",
        views.total_loan_amount_by_time,
        name="total_loan_amount_by_time",
    ),
]
