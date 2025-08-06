# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models import Student, Branch

@receiver(pre_save, sender=Student)
def set_reg_id(sender, instance, **kwargs):
    if not instance.reg_id:  # If reg_id is not set
        branch = instance.branch
        students_in_branch = Student.objects.filter(branch=branch)
        counter = students_in_branch.count() + 1  # Get the count of students in the branch and increment by 1
        instance.reg_id = f"{branch.name.lower()}_{counter}"
