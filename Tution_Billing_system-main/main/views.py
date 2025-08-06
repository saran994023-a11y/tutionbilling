from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Branch, Student, Payment, Invoice,DeletedStudent
from .forms import StudentForm


from django.http import HttpResponse

from .models import Student

def landing_page(request):
    """Render a general landing page."""
    return render(request, 'main/index.html')

def branch_login(request):
    """Handle branch login and authentication."""
    if request.method == 'POST':
        branch_name = request.POST.get('branch_name')
        password = request.POST.get('password')
        if branch_name and password:
            try:
                branch = Branch.objects.get(name=branch_name, password=password)
                request.session['branch_id'] = branch.id
                messages.success(request, f"Welcome {branch_name}!")
                return redirect('branch_home')
            except Branch.DoesNotExist:
                messages.error(request, "Invalid branch name or password.")
        else:
            messages.error(request, "Please provide both branch name and password.")
    return render(request, 'main/branch_login.html')

def branch_home(request):
    """Display branch home page after successful login."""
    branch_id = request.session.get('branch_id')
    if not branch_id:
        return redirect('index')
    
    branch = get_object_or_404(Branch, id=branch_id)
    return render(request, 'main/branch_home.html', {'branch': branch})


from django.db.models import Q

def manage_students(request):
    """View and manage students for the logged-in branch."""
    branch_id = request.session.get('branch_id')
    if not branch_id:
        return redirect('index')

    branch = get_object_or_404(Branch, id=branch_id)
    students = Student.objects.filter(branch=branch)

    # Search functionality across specified fields
    search_term = request.GET.get('search', '')
    if search_term:
        students = students.filter(
            Q(name__icontains=search_term) |
            Q(parent_name__icontains=search_term) |
            Q(phone_number1__icontains=search_term) |
            Q(address__icontains=search_term) |
            Q(subjects__name__icontains=search_term)
        ).distinct()

    return render(request, 'main/manage_students.html', {
        'students': students,
        'branch': branch,
        'search_term': search_term
    })

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Branch, Student, Invoice
from django.core.paginator import Paginator
from .models import Invoice

def manage_invoice(request):
    branch_id = request.session.get('branch_id')
    if not branch_id:
        return redirect('index')

    branch = get_object_or_404(Branch, id=branch_id)
    invoices = Invoice.objects.filter(student__branch=branch)

    # Search functionality
    search_term = request.GET.get('search', '')
    if search_term:
        invoices = invoices.filter(
            Q(student__name__icontains=search_term) |
            Q(student__parent_name__icontains=search_term) |
            Q(student__phone_number1__icontains=search_term) |
            Q(invoice_number__icontains=search_term)
        ).distinct()

    # Sorting functionality (by date_created or total_amount)
    sort_by = request.GET.get('sort_by', 'date_created')  # Default sorting by 'date_created'
    if sort_by == 'amount':
        invoices = invoices.order_by('-total_amount')
    else:
        invoices = invoices.order_by('-date_created')

    # Paginate the invoices (10 invoices per page)
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_invoices = paginator.get_page(page_number)

    return render(request, 'main/manage_invoice.html', {
        'invoices': page_invoices,
        'branch': branch,
        'search_term': search_term,
        'sort_by': sort_by,
    })


def add_student(request):
    """Add a new student for the logged-in branch."""
    branch_id = request.session.get('branch_id')
    if not branch_id:
        return redirect('index')

    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, branch=branch)  # Pass branch to form
        if form.is_valid():
            student = form.save(commit=False)
            student.branch = branch  # Assign the student to the logged-in branch
            student.save()
            form.save_m2m()  # Save many-to-many data for the form
            messages.success(request, f"Student {student.name} added successfully!")
            return redirect('manage_students')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentForm(branch=branch)  # Pass branch to form

    return render(request, 'main/add_student.html', {'form': form})


# def delete_student(request, student_id):
#     """Delete a student and return to the student management page."""
#     student = get_object_or_404(Student, id=student_id)
#     student.delete()
#     messages.success(request, f"Student {student.name} deleted successfully!")
#     return redirect('manage_students')
# from .models import Student, DeletedStudent

def delete_student(request, student_id):
    """Delete a student and store their data in the DeletedStudent model."""
    student = get_object_or_404(Student, id=student_id)

    # Save deleted student's data into DeletedStudent model
    DeletedStudent.objects.create(
        name=student.name,
        parent_name=student.parent_name,
        phone_number1=student.phone_number1,
        address=student.address,
        total_fees=student.total_fees if not callable(student.total_fees) else student.total_fees(),
        advance_payment_months=student.advance_payment_months,
        subjects=", ".join([subject.name for subject in student.subjects.all()]),  # Save as comma-separated string
    )

    # Delete the original student record
    student.delete()
    messages.success(request, f"Student {student.name} deleted successfully and data archived!")
    return redirect('manage_students')
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Student, Payment  # Adjust import based on your project structure

from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student, Payment  # Adjust this import based on your project structure
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal


from decimal import Decimal

def student_payment_status(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student)
    total_fees = student.total_fees()  # Fees per month
    total_payment_made = sum(payment.amount for payment in payments)

    # Initialize months
    months = int(request.POST.get('months', '0'))
    amount_paid = Decimal(request.POST.get('amount', '0'))

    new_total_fees = total_fees * months
    remaining_balance = new_total_fees - (total_payment_made + amount_paid)

    # Create a new payment entry in the database
    if amount_paid > 0:
        Payment.objects.create(student=student, amount=amount_paid)

    # Convert Decimal values to float before storing them in the session
    request.session['months'] = months
    request.session['total_fees'] = float(new_total_fees)  # Convert to float
    request.session['remaining_balance'] = float(remaining_balance)  # Convert to float
    request.session['total_payment_made'] = float(total_payment_made)  # Convert to float

    return render(request, 'main/student_payment_status.html', {
        'student': student,
        'payments': payments,
        'total_fees': total_fees,
        'remaining_balance': remaining_balance,
        'total_payment_made': total_payment_made,
        'months': months,
        'new_total_fees': new_total_fees,
    })


    



from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import uuid
from django.http import HttpResponse
from .models import Student
from datetime import datetime
from .models import Invoice
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import uuid
from datetime import datetime
from django.template.loader import get_template
from .models import Invoice
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from xhtml2pdf import pisa
from datetime import datetime
from django.template.loader import get_template
import uuid

def generate_student_bill(request, student_id):
    # Retrieve the student from the database
    student = get_object_or_404(Student, id=student_id)

    # Retrieve data from session
    months = request.session.get('months', 0)
    total_fees = request.session.get('total_fees', 0)
    remaining_balance = request.session.get('remaining_balance', 0)
    total_payment_made = request.session.get('total_payment_made', 0)

    # Generate a unique invoice number
    invoice_number = uuid.uuid4().hex[:8].upper()

    # Save the invoice data to the database
    invoice = Invoice.objects.create(
        student=student,
        invoice_number=invoice_number,
        total_fees=total_fees,
        remaining_balance=remaining_balance,
        total_payment_made=total_payment_made,
        months=months,
        date_created=datetime.now()
    )

    # Prepare the data for rendering in the template
    data = {
        "invoice_number": invoice_number,
        "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "student_name": student.name,
        "reg_id": student.reg_id,
        "parent_name": student.parent_name,
        "phone_number": student.phone_number1,
        "address": student.address,
        "months": months,
        "total_fees": f"{total_fees:.2f}",
        "remaining_balance": f"{remaining_balance:.2f}",
        "total_payment_made": f"{total_payment_made:.2f}",
        "subjects": []
    }

    # Add subjects and fees
    for subject in student.subjects.all():
        data['subjects'].append({
            'name': subject.name,
            'fee': f"{subject.fee:.2f}"
        })

    # Load the template
    template = get_template('main/invoice_template.html')
    html = template.render(data)

    # Create a HttpResponse object with content_type as 'application/pdf'
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="bill_{datetime.now()}_{student.name}_{invoice_number}.pdf"'
    response['Content-Disposition'] = f'attachment; filename="bill_{datetime.now().strftime("%Y-%m-%d")}{student.name}{invoice_number}.pdf"'

    # Convert the rendered HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check for errors
    if pisa_status.err:
        return HttpResponse('We had some errors generating the invoice PDF')

    # Return the response containing the PDF
    return response


from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .models import Student, Payment

def student_payment_status(request, student_id):
    # Fetch the student and their payment history
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student)
    
    # Get total fees per month and calculate the sum of all previous payments
    total_fees_per_month = student.total_fees()  # This function should return the monthly fee
    total_payment_made = sum(payment.amount for payment in payments)  # Sum of existing payments

    # Retrieve number of months and the new amount paid from the form submission
    months = int(request.POST.get('months', '0'))
    amount_paid = Decimal(request.POST.get('amount', '0'))

    # Calculate new total fees based on selected months and updated remaining balance
    new_total_fees = total_fees_per_month * months
    remaining_balance = new_total_fees -  amount_paid

    # Update total payment with the new amount and save the payment record
    if amount_paid > 0:
        Payment.objects.create(student=student, amount=amount_paid)
        total_payment_made += amount_paid

    # Update session data for easy access
    request.session['months'] = months
    request.session['total_fees'] = float(new_total_fees)  # Store as float
    request.session['remaining_balance'] = float(remaining_balance)  # Store as float
    request.session['total_payment_made'] = float(total_payment_made)  # Store as float

    # Render the template with the updated context
    return render(request, 'main/student_payment_status.html', {
        'student': student,
        'payments': payments,
        'total_fees': total_fees_per_month,
        'remaining_balance': remaining_balance,
        'total_payment_made': total_payment_made,
        'months': months,
        'new_total_fees': new_total_fees,
    })
from django.shortcuts import render, redirect
from datetime import date
from .models import Student

def student_payment_status(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST' and 'submit_payment' in request.POST:
        months = int(request.POST.get('months', 0)) -1
        
        # Update advance payment months and last payment date
        student.advance_payment_months = months 
        student.last_payment_date = date.today()  # Set last payment date to today
        student.save()
        
        # Redirect to manage_students after updating
        return redirect('manage_students')

    return render(request, './main/student_payment_status.html', {'student': student})
from datetime import date
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student, Payment

def student_payment_status(request, student_id):
    # Fetch the student and their payment history
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student)

    # Get total fees per month and calculate the sum of all previous payments
    total_fees_per_month = student.total_fees()  # This function should return the monthly fee
    total_payment_made = sum(payment.amount for payment in payments)  # Sum of existing payments

    # Handle POST request for payment submission
    if request.method == 'POST' and 'submit_payment' in request.POST:
        # Retrieve number of months and the new amount paid from the form submission
        months = int(request.POST.get('months', '0'))
        amount_paid = Decimal(request.POST.get('amount', '0'))

        # Calculate new total fees based on selected months and updated remaining balance
        new_total_fees = total_fees_per_month * months
        remaining_balance = new_total_fees - amount_paid

        # Update total payment with the new amount and save the payment record
        if amount_paid > 0:
            Payment.objects.create(student=student, amount=amount_paid)
            total_payment_made += amount_paid

        # Update advance payment months and last payment date
        student.advance_payment_months = months - 1  # Set advance payment months
        student.last_payment_date = date.today()  # Set last payment date to today
        student.save()

        # Update session data for easy access
        request.session['months'] = months
        request.session['total_fees'] = float(new_total_fees)  # Store as float
        request.session['remaining_balance'] = float(remaining_balance)  # Store as float
        request.session['total_payment_made'] = float(total_payment_made)  # Store as float

        # Redirect to manage_students after updating
        return redirect('manage_students')

    # Render the template with the updated context
    return render(request, 'main/student_payment_status.html', {
        'student': student,
        'payments': payments,
        'total_fees': total_fees_per_month,
        'remaining_balance': remaining_balance if 'remaining_balance' in locals() else None,
        'total_payment_made': total_payment_made,
        'months': request.session.get('months', 0),
        'new_total_fees': new_total_fees if 'new_total_fees' in locals() else None,
    })
