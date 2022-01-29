from django import forms
from django.forms.models import ModelMultipleChoiceField
from .models import StockSymbol


class SelectStockForm(forms.ModelForm):
    class Meta:
        model = StockSymbol
        fields = ['id']
    
    select_stock = ModelMultipleChoiceField(queryset=StockSymbol.objects.all(), widget=forms.CheckboxSelectMultiple)
