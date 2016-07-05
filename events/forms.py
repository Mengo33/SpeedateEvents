from django import forms
from django.forms import ModelForm, CharField, EmailField, PasswordInput, models

from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


class SignupForm(ModelForm):
    first_name = CharField(max_length=300)
    last_name = CharField(max_length=300)
    username = CharField(max_length=300)
    password = CharField(max_length=300, widget=PasswordInput())
    password_confirm = CharField(max_length=300, widget=PasswordInput())
    email = EmailField(max_length=300)

    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'password_confirm',
            'email',
            'gender',
            'status',
            'is_cohen',
            'is_matchmaker',
            'is_single',
        ]



# class SignupForm(forms.Form):
#     first_name = forms.CharField(max_length=300)
#     last_name = forms.CharField(max_length=300)
#     username = forms.CharField(max_length=300)
#     password = forms.CharField(max_length=300, widget=forms.PasswordInput())
#     password_confirm = forms.CharField(max_length=300, widget=forms.PasswordInput())
#     email = forms.EmailField(max_length=300)
#     # gender = forms.IntegerField(choices=Gender.choices)
#     gender = forms.ChoiceField(choices=Gender.choices)
#     # status = forms.IntegerField(choices=Status.choices)
#     status = forms.ChoiceField(choices=Status.choices)
#     is_cohen = forms.BooleanField(required=False)
#     is_matchmaker = forms.BooleanField(required=False)
#     is_single = forms.BooleanField(required=False)
