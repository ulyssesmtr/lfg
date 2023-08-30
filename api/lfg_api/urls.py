from django.urls import path, include
from lfg_api import views


app_name='lfg_api'

urlpatterns = [
    path('loanfield/', views.LoanFieldListView.as_view(), name='list_loanfields'),
    path('loan/', views.LoanCreateView.as_view(), name='add_loans')

]

