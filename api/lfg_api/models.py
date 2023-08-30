from django.db import models


class LoanFieldManager(models.Manager):
    def valid_fields(self):
        return self.filter(is_active=True).order_by('order_number')


class LoanField(models.Model):

    INPUT_TYPE_CHOICES =(
        ('text', 'Text'),
        ('number', 'Number'),
        ('month', 'Month'),
        ('time', 'Time'),
        ('email', 'E-mail')
    )
    name = models.CharField(max_length=50, unique=True)
    input_type = models.CharField(max_length=50, choices=INPUT_TYPE_CHOICES, default='text')
    required = models.BooleanField(default=False)
    order_number = models.IntegerField(unique=True, verbose_name="Order number \
                                      (Frontend input order) ")
    is_active = models.BooleanField(default=True)
    objects = LoanFieldManager()

    def __str__(self):
        return self.name


class LoanManager(models.Manager):
    def api_approved(self):
        return self.filter(is_api_approved=True)


class Loan(models.Model):
    name = models.CharField(max_length=150)
    document = models.JSONField()
    is_api_approved = models.BooleanField(default=False)
    is_admin_approved = models.BooleanField(default=False)
    objects = LoanManager()

    class Meta:
        verbose_name = "All Submitted Loan"

    def __str__(self):
        return self.name


class ApprovedLoan(Loan):
    class Meta:
        verbose_name = "API Approved Loan"
        proxy = True