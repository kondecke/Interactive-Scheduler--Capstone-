from django import forms

class LoginForm(forms.Form):
    userName = forms.CharField(label="User Name", required=True)
    passWord = forms.CharField(widget=forms.PasswordInput())
