from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def add_class_to_label(original_function):
    def class_to_label_tag(self, *args, **kwargs):
        return original_function(self, attrs={"class": "fw-bold"}, label_suffix="")

    return class_to_label_tag


forms.BoundField.label_tag = add_class_to_label(forms.BoundField.label_tag)


def validate_string_has_no_numbers(value):
    if value.isnumeric():
        raise ValidationError("Los datos ingresados no pueden contener números.")


def validate_id_number_length(value):
    if len(value) not in [7, 8, 11]:
        raise ValidationError("Solo se admiten 7, 8 u 11 dígitos.")


def validate_phone_number(value):
    if not len(value) == 10 or not value.isnumeric():
        raise ValidationError("El teléfono debe contener 10 caracteres numéricos.")


def validate_file_size(value):
    limit = settings.MAX_UPLOAD_SIZE
    if value.size > limit:
        raise ValidationError("El tamaño del archivo no puede superar los 5 MB.")


class LoginForm(forms.Form):
    dni = forms.CharField(
        min_length=7,
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Número de documento o CUIT",
            }
        ),
        label="DNI / CUIT",
        validators=[validate_id_number_length],
    )


class LoginRecoveryForm(forms.Form):
    dni_recovery = forms.CharField(
        min_length=7,
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "class": "form-control first",
                "placeholder": "Número de documento o CUIT",
            }
        ),
        label="DNI / CUIT",
        validators=[validate_id_number_length],
    )
    client_id = forms.CharField(
        label="Número de cliente",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control middle", "placeholder": "Número de contrato"}
        ),
    )
    name_recovery = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control middle", "placeholder": "Nombre y apellido"}
        ),
        label="Nombre completo",
        validators=[validate_string_has_no_numbers],
    )
    phone_recovery = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "form-control middle",
                "placeholder": "Número de teléfono",
            }
        ),
        label="Número de teléfono de contacto",
        validators=[validate_phone_number],
    )
    email_recovery = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control last",
                "placeholder": "Dirección de correo electrónico",
            }
        ),
        label="Email de contacto",
    )


class BaseClaimForm(forms.Form):
    def __init__(self, *args, claim_type, has_open_ticket=False, **kwargs):
        super().__init__(*args, **kwargs)
        if claim_type in ["36", "45", "56"]:
            del self.fields["files"]
            del self.fields["files_second"]
        if has_open_ticket:
            del self.fields["name"]
            del self.fields["phone_number"]
            del self.fields["email"]

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-end",
            }
        ),
        label="Nombre completo",
        validators=[validate_string_has_no_numbers],
    )

    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-end",
            }
        ),
        label="Número de teléfono de contacto",
        validators=[validate_phone_number],
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control rounded-end",
            }
        ),
        label="Email de contacto",
    )

    description = forms.CharField(
        max_length=100,
        widget=forms.Textarea(
            attrs={
                "class": "form-control rounded-end",
                "placeholder": "Incluya información que pueda ayudarnos a identificar y resolver su reclamo...",
                "rows": "auto",
            }
        ),
        label="Descripción",
    )

    files = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control rounded-end",
                "accept": "application/pdf, image/jpeg ,image/png",
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "data-bs-title": "Adjuntar archivo (.pdf, .jpeg o .png)",
            }
        ),
        label="Adjuntar archivo (.pdf, .jpeg o .png)",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "jpeg", "png"],
                message="El archivo seleccionado no tiene un formato válido.",
            ),
            validate_file_size,
        ],
    )

    files_second = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control rounded-end",
                "accept": "application/pdf, image/jpeg ,image/png",
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "top",
                "data-bs-title": "Adjuntar archivo (.pdf, .jpeg o .png)",
            }
        ),
        label="Adjuntar archivo (.pdf, .jpeg o .png)",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "jpeg", "png"],
                message="El archivo seleccionado no tiene un formato válido.",
            ),
            validate_file_size,
        ],
    )
