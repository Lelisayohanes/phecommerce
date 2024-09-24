from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        """description"""
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """description"""
    class Meta:
        """description"""
        model = CustomUser
        fields = ("email",)

