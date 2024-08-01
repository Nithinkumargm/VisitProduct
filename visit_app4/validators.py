from django.core.exceptions import ValidationError

def validate_case_insensitive_unique(model, field, value):
    if model.objects.filter(**{f'{field}__iexact': value}).exists():
        raise ValidationError(f"{model._meta.verbose_name} with this {field} already exists.")
