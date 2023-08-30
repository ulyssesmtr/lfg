from rest_framework import serializers
from lfg_api.models import Loan, LoanField


class LoanFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanField
        fields = ["name", "input_type", "required", "order_number","is_active"]


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ["name", "document"]

    def validate_document(self, document):
        if document:
            valid_fields = set(LoanField.objects.valid_fields().values_list('name', flat=True))
            document_fields = set(document.keys())
            if document_fields != valid_fields:
                missing_fields = valid_fields.difference(document_fields)
                raise serializers.ValidationError(f"The following fields are missing or were sent unnecessarily : {missing_fields}")
        return document
