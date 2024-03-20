from cpkmodel import CPkModel
from django.db import models


class InvoiceData(models.Model):
    """
    Invoice Data Module.
    """

    app_id = models.IntegerField(name="App ID")
    xref = models.IntegerField(
        null=False, name="Xref", editable=False, primary_key=True
    )
    settlement_date = models.DateField(null=False, name="Settlement Date")
    broker = models.CharField(null=False, name="Broker", max_length=100)
    sub_broker = models.CharField(name="Sub Broker", max_length=100)
    borrower_name = models.CharField(name="Borrower Name", max_length=100)
    description = models.CharField(name="Description", max_length=500)
    total_loan_amount = models.FloatField(
        null=False,
        name="Total Loan Amount",
        editable=False,
        # primary_key=True
    )
    comission_rate = models.FloatField(null=False, name="Comission Rate")
    upfront = models.FloatField(name="Upfront")
    upfront_incl_gst = models.FloatField(name="Upfront Incl GST")
    tier = models.CharField(name="Tier", null=False, max_length=10)
