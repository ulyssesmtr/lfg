from django.test import TestCase
from lfg_api.models import LoanField, Loan
from django.shortcuts import resolve_url as r
from lfg_api.serializers import LoanFieldSerializer, LoanSerializer

class TestLoanFieldSerializer(TestCase):
    
    def setUp(self):
        self.data = {
            "name": "Purpose",
            "input_type": "text",
            "required": True,
            'order_number': 1,
            "is_active": True
        }


    def test_fields(self):
        expected_fields = ['name', 'input_type', 'required', 'order_number','is_active']
        self.assertSequenceEqual(expected_fields, LoanFieldSerializer.Meta.fields)

    def test_content(self):
        serializer = self.make_valid_serializer()
        self.assertEqual(serializer.data, self.data)

    def test_required_fields(self):
        required_fields = ['name', 'input_type', 'order_number', 'is_active', 'required']
        for field in required_fields:
            with self.subTest():
                serializer=self.make_valid_serializer(**{field:''})
                self.assertIn(field, serializer.errors)

    def test_loan_field_created(self):
        serializer = self.make_valid_serializer()
        serializer.save()
        self.assertEqual(LoanField.objects.count(), 1)

    def make_valid_serializer(self, **kwargs):
        data = dict(self.data, **kwargs)
        serializer = LoanFieldSerializer(data=data)
        serializer.is_valid()
        return serializer


class TestLoanSerializer(TestCase):

    fixtures = ['lfg_api/fixtures/loan_field_fixture.json']

    def setUp(self):
        self.data = {
        'name': 'Test Loan',
        'document': {
            'Email': 'email@email.com',
            'Lender': 'lender name',
            'Borrower Name': 'borrower name',
            'Purpose': 'purpose test',
            'Loan Value': 100
            }
        }

    def test_fields(self):
        expected_fields = ['name', 'document']
        self.assertSequenceEqual(expected_fields, LoanSerializer.Meta.fields)

    def test_content(self):
        serializer = self.make_valid_serializer()
        self.assertEqual(serializer.data, self.data)

    def test_required_fields(self):
        required_fields = ['name']
        for field in required_fields:
            with self.subTest():
                serializer=self.make_valid_serializer(**{field:''})
                self.assertIn(field, serializer.errors)

    def test_loan_created(self):
        serializer = self.make_valid_serializer()
        serializer.save()
        self.assertEqual(Loan.objects.count(), 1)
    
    def test_missing_field_error(self):
        data = {
        'name': 'Test Loan',
        'document': {
            'Email': 'email@email.com',
            'Lender': 'lender name',
            'Borrower Name': 'borrower name',
            'Purpose': 'purpose test',
            }
        }
        serializer = LoanSerializer(data=data)
        serializer.is_valid()
        self.assertIn('document', serializer.errors)
        
    def make_valid_serializer(self, **kwargs):
        data = dict(self.data, **kwargs)
        serializer = LoanSerializer(data=data)
        serializer.is_valid()
        return serializer