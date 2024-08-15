from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PatientProfile, DoctorProfile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    address_line1 = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=6)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'user_type', 'address_line1', 'city', 'state', 'pincode', 'profile_picture')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
