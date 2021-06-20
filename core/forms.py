from django import forms
from .models import BaseModel


# Forms


class BaseModelForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        exclude = (
            "created_date",
            "updated_date",
            "deleted_date",
        )
