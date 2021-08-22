from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Culink

class CulinkForm(forms.ModelForm):
    class Meta:
        model = Culink
        fields = ['shortlink_text', 'longlink_text']
        labels = {'shortlink_text' : '', 'longlink_text' : ''}
        widgets = {'shortlink_text' : forms.TextInput(attrs={'required' : True,
        'placeholder' : 'Type your shortcut', 'minlength' : 6, 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}),
            'longlink_text' : forms.URLInput(attrs={'required' : True,
            'placeholder' : 'Paste your link to shorten', 'minlength' : 15, 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'})}


class CulinkOneForm(forms.ModelForm):
    class Meta:
        model = Culink
        fields = ['longlink_text']
        labels = {'longlink_text' : ''}
        widgets = {'longlink_text' : forms.URLInput(attrs={'required' : True,
            'placeholder' : 'Paste your link to shorten', 'minlength' : 15, 'class': 'form-control border border-primary border-3 rounded-3'})}


class CulinkCheckOneForm(forms.ModelForm):
    class Meta:
        model = Culink
        fields = ['shortlink_text']
        labels = {'shortlink_text' : ''}
        widgets = {'shortlink_text' : forms.TextInput(attrs={'required' : True,
            'placeholder' : 'Type your link to check', 'minlength' : 6, 'class': 'form-control border border-primary border-3 rounded-3'})}


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={'placeholder' : 'Username', 'minlength' : 6, 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))
    password = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder' : 'Password', 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={'placeholder' : 'Username', 'minlength' : 6, 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))
    password1 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder' : 'Password', 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))
    password2 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder' : 'Password', 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder' : 'Old Password', 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))
    new_password1 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder' : 'New Password', 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))
    new_password2 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder' : 'New Password', 'class': 'my-2 fs-5 form-control border border-primary border-3 rounded-3'}))
