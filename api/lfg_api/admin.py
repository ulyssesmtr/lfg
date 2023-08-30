from django.contrib import admin
from lfg_api.models import LoanField, Loan, ApprovedLoan


class LoanFieldAdmin(admin.ModelAdmin):
    list_display = ["name", "input_type", "required", "order_number", "is_active"]

class LoanAdmin(admin.ModelAdmin):
    list_display = ["name", "document", "is_api_approved", "is_admin_approved"]
    readonly_fields = ('is_api_approved', )

class ApprovedLoanAdmin(LoanAdmin):
    def get_queryset(self, request):
        return self.model.objects.api_approved()


admin.site.register(LoanField, LoanFieldAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(ApprovedLoan, ApprovedLoanAdmin)