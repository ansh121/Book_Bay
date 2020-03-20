from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='username')
	password = forms.CharField(widget=forms.PasswordInput())

