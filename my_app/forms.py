from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=15)
    last_name=forms.CharField(max_length=15)
    class Meta:
        model=User
        fields=["email","first_name","last_name","password1","password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set username to email
        user.is_active = False  # Set user account to inactive
        if commit:
            user.save()
        return user
    

    