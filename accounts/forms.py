from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    bio = forms.CharField(max_length=50, initial='Hi! I\'m on miniblog!')

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'bio', 'password1', 'password2',
        )
