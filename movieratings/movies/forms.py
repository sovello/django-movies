from django import forms
from movies.models import Rater, Ratings, Occupation
from django.contrib.auth.models import User


class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('gender', 'occupation', 'age', 'zip_code', 'photo')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('age', 'occupation', 'zip_code', 'photo')
        widgets = {
'photo' : forms.ClearableFileInput(attrs={'accept': 'image/*', 'name':'image'}),
            }
    #fields = ('occupation', 'age', 'zip_code', 'photo')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['rating']

        
class ContactForm(forms.Form):
    name = forms.CharField(label = "Your Name", max_length = 255)
    subject = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)
