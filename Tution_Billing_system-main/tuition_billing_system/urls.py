from django.contrib import admin
from django.urls import path, include
from main.views import landing_page, branch_login, branch_home, manage_students, add_student, delete_student, generate_student_bill, student_payment_status, manage_invoice
from main import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('branch_login/', branch_login, name='branch_login'),
    path('branch_home/', branch_home, name='branch_home'),
    path('manage_students/', manage_students, name='manage_students'),
    path('add_student/', add_student, name='add_student'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('student_payment_status/<int:student_id>/', student_payment_status, name='student_payment_status'),
    path('generate_student_bill/<int:student_id>/', generate_student_bill, name='generate_student_bill'),
    path('manage_invoice/', views.manage_invoice, name='manage_invoice'),
    
    
]