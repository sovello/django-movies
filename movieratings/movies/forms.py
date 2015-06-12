from django import forms
from movies.models import Rater
from django.contrib.auth.models import User
from .models import Rater

class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('gender', 'occupation', 'age', 'zip_code')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password')
