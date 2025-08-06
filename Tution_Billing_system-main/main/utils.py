# utils.py
from main.models import Student, Branch

def update_reg_ids():
    # Function implementation
    branches = Branch.objects.all()
    
    for branch in branches:
        students = Student.objects.filter(branch=branch, reg_id__isnull=True)
        counter = 1
        
        for student in students:
            student.reg_id = f"{branch.name.lower()}_{counter}"
            student.save()
            counter += 1
