from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from thinkpart.models import Part, Laptop


class UserRegisterForm(forms.ModelForm):
    re_password = forms.CharField(label='Re-Password', max_length=64, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get('re_password')
        if password != re_password:
            raise ValidationError("Passwords do not match")


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'
