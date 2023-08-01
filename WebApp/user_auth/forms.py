from django import forms




class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, required=True, strip=True)
    password = forms.CharField(widget=forms.PasswordInput())
