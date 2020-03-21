from django import forms

from bookbayapp.models import *


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class LoginCredentialForm(forms.ModelForm):
    class Meta:
        model = LoginCredential
        fields = "__all__"

    def updateuser(self,id):
        self.user=id
