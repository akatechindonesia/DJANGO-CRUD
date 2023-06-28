from django import forms
from .models import Product
from .models import Member
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price','deskripsi','image')


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','gender','phone','email','username','password','is_active','is_staff')

    def save(self, commit=True):
        # Get the password from the form data
        password = self.cleaned_data.get('password')
        
        # Encrypt the password using make_password() function
        encrypted_password = make_password(password)

        # Update the password field with the encrypted password
        self.instance.password = encrypted_password

        return super().save(commit)
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].label = 'Username'
#         self.fields['password'].label = 'Password'

class LoginForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = Member
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'