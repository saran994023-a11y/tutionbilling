from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Q
from .models import Branch, Subject, Student, Invoice, Payment, DeletedStudent

# Unregister the Group model
from django.contrib.auth.models import Group
admin.site.unregister(Group)
from django.contrib import admin

# Customize the site header, title, and index title
admin.site.site_header = "Administration"
admin.site.site_title = "Administration"
admin.site.index_title = "Welcome to the Administration Panel"



# Admin for Branch model
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')


# Admin for Subject model
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'fee')


# Custom Filters
class PaidStatusFilter(admin.SimpleListFilter):
    title = _('Paid Status')
    parameter_name = 'is_paid'

    def lookups(self, request, model_admin):
        return [
            ('paid', _('Paid')),
            ('unpaid', _('Unpaid')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'paid':
            return queryset.filter(remaining_balance=0)
        if self.value() == 'unpaid':
            return queryset.filter(remaining_balance__gt=0)


class StudentPaidStatusFilter(admin.SimpleListFilter):
    title = _('Paid Status')
    parameter_name = 'paid_status'

    def lookups(self, request, model_admin):
        return [
            ('paid', _('Paid')),
            ('unpaid', _('Unpaid')),
        ]

    def queryset(self, request, queryset):
        paid_students = []
        unpaid_students = []

        for student in queryset:
            total_fees = sum(subject.fee for subject in student.subjects.all())
            total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0

            if total_paid >= total_fees:
                paid_students.append(student.id)
            else:
                unpaid_students.append(student.id)

        if self.value() == 'paid':
            return queryset.filter(id__in=paid_students)
        elif self.value() == 'unpaid':
            return queryset.filter(id__in=unpaid_students)
        return queryset


class AdvancePaymentFilter(admin.SimpleListFilter):
    title = _('Advance Payment Months')
    parameter_name = 'advance_payment_months'

    def lookups(self, request, model_admin):
        return [
            (1, _('1 month')),
            (3, _('3 months')),
            (6, _('6 months')),
            (12, _('12 months')),
        ]

    def queryset(self, request, queryset):
        try:
            if self.value():
                months_paid = int(self.value())
                matching_students = []
                for student in queryset:
                    total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
                    monthly_fee = sum(subject.fee for subject in student.subjects.all()) / len(student.subjects.all()) if student.subjects.all() else 0
                    advance_months = total_paid // monthly_fee if monthly_fee > 0 else 0
                    if advance_months >= months_paid:
                        matching_students.append(student.id)
                return queryset.filter(id__in=matching_students)
        except ValueError:
            return queryset

        return queryset


class TotalFeesFilter(admin.SimpleListFilter):
    title = _('Total Fees')
    parameter_name = 'total_fees'

    def lookups(self, request, model_admin):
        return [
            ('low', _('Less than 500')),
            ('medium', _('1000 - 5000')),
            ('high', _('More than 5000')),
        ]

    def queryset(self, request, queryset):
        # Filter queryset based on total fees ranges
        low_ids = []
        medium_ids = []
        high_ids = []

        for student in queryset:
            total_fees = sum(subject.fee for subject in student.subjects.all())
            if total_fees < 500:
                low_ids.append(student.id)
            elif 1000 <= total_fees <= 5000:
                medium_ids.append(student.id)
            else:
                high_ids.append(student.id)

        if self.value() == 'low':
            return queryset.filter(id__in=low_ids)
        elif self.value() == 'medium':
            return queryset.filter(id__in=medium_ids)
        elif self.value() == 'high':
            return queryset.filter(id__in=high_ids)

        return queryset


# Admin for Invoice model
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'total_fees', 'remaining_balance', 'date_created')
    search_fields = ('invoice_number', 'student__name', 'student__parent_name', 'student__phone_number1', 'student__branch__name')
    list_filter = ('date_created', 'student__branch', 'total_fees')  # Added branch filter

    def is_paid(self, obj):
        return obj.remaining_balance <= 0
    is_paid.boolean = True
    is_paid.short_description = 'Paid Status'

# Admin for Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'get_reg_id',  # Display reg_id as the first column
        'name',
        'branch',
        'parent_name',
        'phone_number1',
        'get_subjects',
        'total_fees',
        'advance_payment_months',
    )
    list_filter = ('branch', StudentPaidStatusFilter, AdvancePaymentFilter, TotalFeesFilter)  # Filters
    search_fields = ('reg_id', 'name', 'parent_name', 'phone_number1', 'branch__name')  # Added reg_id as the first searchable field

    def get_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
    get_subjects.short_description = 'Subjects'

    def total_fees(self, obj):
        return sum(subject.fee for subject in obj.subjects.all())
    total_fees.admin_order_field = 'total_fees'  # Enables sorting
    total_fees.short_description = 'Total Fees'

    def advance_payment_months(self, obj):
        total_paid = obj.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
        monthly_fee = sum(subject.fee for subject in obj.subjects.all()) / len(obj.subjects.all()) if obj.subjects.all() else 0
        return total_paid // monthly_fee if monthly_fee > 0 else 0
    advance_payment_months.short_description = 'Months Paid'

    def get_reg_id(self, obj):
        return obj.reg_id  # Fetch the reg_id from the Student model
    get_reg_id.short_description = 'Registration ID'

class DeletedStudentAdmin(admin.ModelAdmin):
    list_display =('name','parent_name','phone_number1','address','total_fees','advance_payment_months','subjects','deleted_at')   
# Register models in the admin
admin.site.register(Branch, BranchAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(DeletedStudent,DeletedStudentAdmin)
