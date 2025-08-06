from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('branch_login/', views.branch_login, name='branch_login'),
    path('branch_home/', views.branch_home, name='branch_home'),
    path('manage_students/', views.manage_students, name='manage_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('student_payment_status/<int:student_id>/', views.student_payment_status, name='student_payment_status'),
    path('generate_student_bill/<int:student_id>/', views.generate_student_bill, name='generate_student_bill'),
    path('manage_invoice/', views.manage_invoice, name='manage_invoice'), 
    path('index/', views.landing_page, name='landing_page'),
    path('student/<int:student_id>/update_payment/', views.update_payment_status, name='update_payment_status'),
]
