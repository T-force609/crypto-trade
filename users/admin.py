from django.contrib import admin
from django_countries.widgets import CountrySelectWidget
from django import forms
from .models import User

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            'country': CountrySelectWidget()
        }


admin.site.register(User)