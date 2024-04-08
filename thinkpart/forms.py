from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

from thinkpart.models import Part, Laptop, LaptopPart, UserLaptop, UserReplacedPart, PART_TYPE_CHOICES


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput())
    re_password = forms.CharField(label='Re-Password', max_length=64, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get('re_password')
        if password != re_password:
            raise ValidationError("Passwords do not match")


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput())


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'


class PartSearchForm(forms.Form):
    types = PART_TYPE_CHOICES
    types.insert(0, ('', ''))

    compatible_laptop = forms.ModelChoiceField(label='Compatible laptop', queryset=Laptop.objects.all(), required=False)
    name = forms.CharField(label='Name', max_length=255, required=False)
    type = forms.ChoiceField(label='Type', choices=types, required=False)
    manufacturer = forms.CharField(label='Manufacturer', max_length=255, required=False)
    product_code = forms.CharField(label='Product code', max_length=255, required=False)


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'


class PartLaptopForm(forms.ModelForm):
    class Meta:
        model = LaptopPart
        fields = ['laptop', 'alternative']


class LaptopPartForm(forms.ModelForm):
    class Meta:
        model = LaptopPart
        fields = ['part', 'alternative']


class UserLaptopForm(forms.ModelForm):
    class Meta:
        model = UserLaptop
        fields = ['laptop', 'serial']


class UserReplacedPartForm(forms.ModelForm):
    # limit queryset to original part and alternatives
    def __init__(self, laptop_part, *args, **kwargs):
        super(UserReplacedPartForm, self).__init__(*args, **kwargs)
        compatible_parts = Part.objects.filter(
            Q(alternative_part__part=laptop_part.part) | Q(pk=laptop_part.part.pk)
        ).distinct()
        self.fields['part_current'].queryset = compatible_parts

    class Meta:
        model = UserReplacedPart
        fields = ['part_current', 'comment']
