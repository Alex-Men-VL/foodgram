from django.contrib.auth import forms

from .models import CustomUser


class CustomUserCreationForm(forms.UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
        )


class CustomUserChangeForm(forms.UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
        )
