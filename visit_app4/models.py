from django.utils import timezone
from django.db import models
from django.conf import settings
from .validators import validate_case_insensitive_unique
from django.core.exceptions import ValidationError


class Dairy(models.Model):
    name = models.CharField(max_length=255)
    village = models.ForeignKey('Village', on_delete=models.CASCADE, related_name='diaries')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='dairies_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='dairies_modified')

    class Meta:
        unique_together = ('name', 'village')

    def clean(self):
        if Dairy.objects.filter(village=self.village, name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError(f"A dairy with the name '{self.name}' already exists in the village '{self.village.name}'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Taluk(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='taluks_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='taluks_modified')

    def clean(self):
        validate_case_insensitive_unique(Taluk, 'name', self.name)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=255)
    taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='villages_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='villages_modified')

    def clean(self):
        if Village.objects.filter(taluk=self.taluk, name__iexact=self.name).exclude(id=self.id).exists():
            raise ValidationError(f"A village with the name '{self.name}' already exists in the taluk '{self.taluk.name}'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.taluk.name})"

class Employee(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    taluks = models.ManyToManyField(Taluk, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='employees_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='employees_modified')
 
    def __str__(self):
        return self.name


class VisitType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='visit_types_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='visit_types_modified')

    def __str__(self):
        return self.name


class Visit(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    visit_types = models.ManyToManyField(VisitType)
    taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    dairy = models.ForeignKey(Dairy, on_delete=models.CASCADE)
    summary = models.TextField(max_length=1500)
    date_created = models.DateTimeField(auto_now_add=True)
    gps = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='visits_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='visits_modified')


    def __str__(self):
        return f"Visit by {self.employee.name} on {self.date_created}"


class Photo(models.Model):
    visit = models.ForeignKey(Visit, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    date_taken = models.DateTimeField(auto_now_add=True)
    gps = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                   related_name='photos_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=True,
                                    related_name='photos_modified')

    def __str__(self):
        return f"Photo taken on {self.date_taken}"
