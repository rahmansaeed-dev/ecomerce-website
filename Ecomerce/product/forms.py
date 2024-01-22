from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Customer

class PasswordChange(PasswordChangeForm):
        old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True , 'class':'form-control'}
        ),
    )
        new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
        new_password2 = forms.CharField(
            label=_("New password confirmation"),
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
        )

class PasswordResetFormView(PasswordResetForm):
        email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class':'form-control'}),
    )
        

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'})
    )
        
class ProfileForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    class Meta:
        model = Customer
        fields = ['Name','city','state','zipcode','locality']
        widgets = {
            'Name':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            # 'address2':forms.TextInput(attrs={'class':'form-control'}),

                  }
        
# class LoginFormView(AuthenticationForm):
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password",'class':'form-control w-50'}),
#     )
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control w-50'}),
#     )




