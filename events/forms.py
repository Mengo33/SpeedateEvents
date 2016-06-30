from django import forms

from events.models import Gender, Status


class LoginForm(forms.Form):
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=300)
    last_name = forms.CharField(max_length=300)
    username = forms.CharField(max_length=300)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput())
    password_recheck = forms.CharField(max_length=300, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=300)
    gender = forms.ChoiceField(choices=Gender.choices)
    status = forms.ChoiceField(choices=Status.choices)
    is_cohen = forms.BooleanField(required=False)
    is_matchmaker = forms.BooleanField(required=False)
    is_single = forms.BooleanField(required=False)
