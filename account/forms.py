from django import forms
from .models import Profile


# ---------------- STEP 1 ----------------
class RegisterStep1Form(forms.Form):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
    )

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


# ---------------- STEP 2 ----------------
class RegisterStep2Form(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']

        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Enter bio'
            })
        }
