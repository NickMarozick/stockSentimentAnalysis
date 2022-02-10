from django import forms
from django.db.models import Case, Value, When
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from .models import StockSymbol


choices = StockSymbol.objects.all().values_list('id', 'name')


class SelectStockForm(forms.Form):
    selected_stock = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=choices,
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_list = cleaned_data.get("selected_stock")

        if len(selected_list) > 25:
            msg = "Please select 25 or less stock"
            self.add_error('selected_stock', msg)
    
    def save(self):
        StockSymbol.objects.update(
            user_selected=Case(When(id__in=self.cleaned_data['selected_stock'], then=Value(True)), 
            default=Value(False)))

    
    # class Meta:
    #     model = StockSymbol
    #     fields=['user_selected']
    #     widgets = {
    #         'user_selected': forms.CheckboxSelectMultiple
    #  }

# class SelectStockForm(forms.ModelForm):
#     class Meta:
#         model = StockSymbol
#         fields=['user_selected']
#         widgets = {
#             'user_selected': forms.CheckboxSelectMultiple
#         }
    # def __init__(self, *args, **kwargs):
    #     super(SelectStockForm, self).__init__(*args, **kwargs)
    #     self.fields['user_selected'].queryset = StockSymbol.objects.all().values_list('name', 'user_selected')

    # select_stock = forms.ModelMultipleChoiceField(queryset=StockSymbol.objects.all().values_list('name', 'user_selected'), initial=StockSymbol.objects.filter(user_selected=True), widget=forms.CheckboxSelectMultiple, label='')
