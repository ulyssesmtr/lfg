from django.test import TestCase
from lfg_api.models import Loan
from rest_framework.test import APIClient
from django.shortcuts import resolve_url as r
from rest_framework import status
from lfg_api.serializers import LoanFieldSerializer
from unittest.mock import patch


class TestLoanFieldListView(TestCase):
    fixtures = ['lfg_api/fixtures/loan_field_fixture.json']

    def setUp(self):        
        self.client = APIClient()
        self.list_resp = self.client.get(r('lfg_api:list_loanfields'))

    def test_get(self):
        """Should return a 200 OK"""
        self.assertEqual(self.list_resp.status_code, status.HTTP_200_OK)
    
    def test_post_not_allowed(self):
        """POST should not be allowed"""
        resp = self.client.post(r('lfg_api:list_loanfields'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_allowed(self):
        """PUT should not be allowed"""
        resp = self.client.put(r('lfg_api:list_loanfields'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_not_allowed(self):
        """PATCH should not be allowed"""
        resp = self.client.patch(r('lfg_api:list_loanfields'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        """DELETE should not be allowed"""
        resp = self.client.delete(r('lfg_api:list_loanfields'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_list(self):
        """Response json should be an array"""
        self.assertEqual(type(self.list_resp.json()), list)
    
    def test_valid_fields(self):
        """Response should only contain active fields"""
        for field in self.list_resp.json():
            with self.subTest():
                self.assertEqual(field['is_active'], True)

    def test_get_list_fields(self):
        """Response should contain exactly the serializers fields"""
        self.assertEqual(list(self.list_resp.json()[0].keys()), LoanFieldSerializer.Meta.fields)


class TestLoanView(TestCase):

    fixtures = ['lfg_api/fixtures/loan_field_fixture.json']

    def setUp(self):        
        self.client = APIClient()
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
        self.resp = self.client.post(r('lfg_api:add_loans'), data=self.data, format='json')
    
    def test_post(self):
        """Should return a 201 CREATED"""
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)

    def test_get_not_allowed(self):
        """GET should not be allowed"""
        resp = self.client.get(r('lfg_api:add_loans'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_allowed(self):
        """PUT should not be allowed"""
        resp = self.client.put(r('lfg_api:add_loans'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_not_allowed(self):
        """PATCH should not be allowed"""
        resp = self.client.patch(r('lfg_api:add_loans'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        """DELETE should not be allowed"""
        resp = self.client.delete(r('lfg_api:add_loans'))
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_loan_created(self):
        self.assertEqual(Loan.objects.count(), 1)

    @patch('lfg_api.views.task_loan_external_evaluation.delay')
    def test_celery_task_called(self, mock_function):
        """Celery task should be correctly called"""
        self.resp = self.client.post(r('lfg_api:add_loans'), data=self.data, format='json')
        self.assertTrue(mock_function.called)
    
    def test_missing_field(self):
        """Should return a 400 when a field is missing from the payload"""
        data = {
            'name': 'Test Loan',
            'document': {
                'Email': 'email@email.com',
                'Lender': 'lender name',
                'Borrower Name': 'borrower name',
                'Purpose': 'purpose test',
                }
        }
        self.resp = self.client.post(r('lfg_api:add_loans'), data=data, format='json')
        self.assertEqual(self.resp.status_code, status.HTTP_400_BAD_REQUEST)