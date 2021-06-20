from django import forms
from core.forms import BaseModelForm

from .models import Product


class ProductForm(BaseModelForm):
    name = forms.CharField(max_length=255)
    base_price = forms.IntegerField()
    description = forms.CharField(max_length=255)
    


    class Meta(BaseModelForm.Meta):
        model = Product
    
