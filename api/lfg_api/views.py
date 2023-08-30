from rest_framework import generics
from lfg_api.serializers import LoanFieldSerializer, LoanSerializer
from lfg_api.models import LoanField
from lfg_api.tasks import task_loan_external_evaluation



class LoanFieldListView(generics.ListAPIView):
    queryset = LoanField.objects.valid_fields()
    serializer_class = LoanFieldSerializer

    
class LoanCreateView(generics.CreateAPIView):
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        loan_obj = serializer.save()
        task_loan_external_evaluation.delay(loan_obj.pk)
