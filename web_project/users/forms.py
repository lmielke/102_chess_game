from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'musterman@company.com'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'musterman@company.com'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        phone = forms.RegexField(label="Telefon", regex=r'^\+?1?\d{9,20}$', error_messages={'invalid': 'falsches format'})
        fields = ['image', 'hello_world', 'phone']
