from django.db import models
from django.utils import timezone
from datetime import datetime
class Branch(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subjects_available = models.ManyToManyField('Subject', related_name='branches')
    password = models.CharField(max_length=255)


    class Meta:
        verbose_name = 'Branch'  # Singular form
        verbose_name_plural = 'Branches'  # Plural form

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Fee: {self.fee}"

class Student(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255)
    phone_number1 = models.CharField(max_length=15)
    phone_number2 = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    subjects = models.ManyToManyField(Subject)
    advance_payment_months = models.IntegerField(default=0) 
    last_payment_date = models.DateField(null=True, blank=True)
    calculate_paid_status = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        # If reg_id is not set (new record), generate it
        if not self.reg_id:
            branch_name = self.branch.name.lower()
            student_count = Student.objects.filter(branch=self.branch).count() + 1
            self.reg_id = f"{branch_name}_{student_count}"
        super().save(*args, **kwargs)

    def calculate_paid_status(self):
        if self.last_payment_date:
            months_since_payment = (datetime.now().year - self.last_payment_date.year) * 12 + (datetime.now().month - self.last_payment_date.month)
            if months_since_payment <= self.advance_payment_months:
                remaining_months = self.advance_payment_months - months_since_payment + 1
                return f"Paid"
            else:
                return "Unpaid"
        return "Unpaid"

    def total_fees(self):
        return sum(subject.fee for subject in self.subjects.all())

    def __str__(self):
        return self.name


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    ]) 

    def __str__(self):
        return f"{self.student.name} - {self.payment_date} - {self.amount}"

from django.db import models
from django.contrib.auth.models import User

# class Invoice(models.Model):
#     branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
#     student = models.ForeignKey('Student', on_delete=models.CASCADE)
#     invoice_number = models.CharField(max_length=100, unique=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.invoice_number
from django.db import models
from .models import Branch, Subject  # Ensure you import necessary models

# class Invoice(models.Model):
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)  # New field added
#     parent_name = models.CharField(max_length=255)
#     phone_number1 = models.CharField(max_length=15)
#     address = models.TextField()
#     subjects = models.ManyToManyField(Subject)
#     advance_payment_months = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name
from django.db import models
from django.utils import timezone

# class Invoice(models.Model):
#     # Relating Invoice to a Branch
#     branch = models.ForeignKey('Branch', on_delete=models.CASCADE)

#     # Relating Invoice to a Student (as you are fetching students in the view)
#     # student = models.ForeignKey('Student', on_delete=models.CASCADE)

#     # Other relevant fields
#     invoice_number = models.CharField(max_length=100, unique=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date_created = models.DateTimeField(auto_now_add=True)

#     # Invoice-specific fields
#     name = models.CharField(max_length=255)  # Name of the student
#     parent_name = models.CharField(max_length=255)  # Parent name
#     phone_number1 = models.CharField(max_length=15)  # Primary contact number
#     address = models.TextField()  # Student address

#     # Linking the subjects for which the invoice is issued
#     subjects = models.ManyToManyField('Subject')

#     advance_payment_months = models.IntegerField(default=0)  # Months of advance payment

#     def __str__(self):
#         return f"Invoice {self.invoice_number} - {self.name}"

#     # Custom method to calculate the total amount based on subjects
#     def calculate_total_amount(self):
#         return sum(subject.fee for subject in self.subjects.all())
from django.db import models
from django.utils import timezone
from uuid import uuid4

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True, default=uuid4().hex[:8].upper())
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_payment_made = models.DecimalField(max_digits=10, decimal_places=2)
    months = models.IntegerField()

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.student.name}"

from django.db import models

class DeletedStudent(models.Model):
    name = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255)
    phone_number1 = models.CharField(max_length=15)
    address = models.TextField()
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    advance_payment_months = models.IntegerField(default=0)
    subjects = models.TextField()  # Store subjects as a comma-separated string
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name