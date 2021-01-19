from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

from . import models as account_models


######################################################################################################################


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = account_models.CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email address'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = account_models.Profile
        exclude = ('user', )
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'bio_input_area input_area'}),
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].label = 'Write something about you'
        self.fields['profile_pic'].label = 'Upload your profile picture'










