from celery import shared_task
import requests
import json
from lfg_api.models import Loan

LOAN_PROCESSOR_API_URL = 'https://loan-processor.digitalsys.com.br/api/v1/loan/'


@shared_task
def task_loan_external_evaluation(loan_pk):
    try:
        loan = Loan.objects.get(pk=loan_pk)
    except Loan.DoesNotExist:
        return "Invalid Loan primary key"

    try:
        data = {
            "name": loan.name,
            "document": json.dumps(loan.document)
        }
        response = requests.post(url=LOAN_PROCESSOR_API_URL, data=data)
        result = response.json().get("approved")
        loan.is_api_approved = result
        loan.save()
        return f"Loan id {loan.pk} got the following result: {result}"
    except Exception as e:
        print(f"An error ocurred during the task_loan_external_evaluation execution. Error: {str(e)}")
