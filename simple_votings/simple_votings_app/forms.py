from django import forms
from .models import User, Profile


class AddVotingForm(forms.Form):
    question = forms.CharField(max_length=200,
                               required=True,
                               label='Ваш вопрос')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)
