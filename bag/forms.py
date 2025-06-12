from django import forms
from products.models import ProductVariant, Accessory

class AddToBagForm(forms.Form):
    variant = forms.ModelChoiceField(
        queryset=ProductVariant.objects.all(),
        empty_label="Select a size",
        widget=forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'})
    )
    accessories = forms.ModelMultipleChoiceField(
        queryset=Accessory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'w-20 border px-2 py-1 rounded'})
    )
