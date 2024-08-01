from django import forms
from .models import Visit, Taluk, Employee, Village

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['employee', 'visit_types', 'taluk', 'village', 'dairy', 'summary', 'gps']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['taluk'].queryset = Taluk.objects.none()

        if 'employee' in self.data:
            try:
                employee_id = int(self.data.get('employee'))
                self.fields['taluk'].queryset = Taluk.objects.filter(employees__id=employee_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['taluk'].queryset = self.instance.employee.taluks.order_by('name')
