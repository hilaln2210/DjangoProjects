from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        min_length = 8

        if len(password) < min_length:
            raise forms.ValidationError(f'The password must be at least {min_length} characters long.')
        return password

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        min_length = 8

        if len(password) < min_length:
            raise forms.ValidationError(f'The password must be at least {min_length} characters long.')
        return password

class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
