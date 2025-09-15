from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    assigned_admin = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='admin'),
        label="Assigned Admin",
        required=False,  # Make it optional if it's not always required
        empty_label="-- Select an Admin --"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'name', 'role', 'assigned_admin']

class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'name', 'role']
        