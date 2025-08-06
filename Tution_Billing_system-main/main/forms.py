from django import forms
from .models import Student, Subject

class StudentForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(),  # Initially empty, will be updated in the view
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Student
        fields = ['name', 'parent_name', 'phone_number1', 'phone_number2', 'address', 'subjects']

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        if branch:
            self.fields['subjects'].queryset = branch.subjects_available.all()
