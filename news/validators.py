from django.core.exceptions import ValidationError


def validate_title(value):
    if len(value.split()) == 1:
        raise ValidationError('O título deve conter pelo menos 2 palavras.')
