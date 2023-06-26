from django import forms
from .models import Product
from .models import Member

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price')


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name', 'email')

