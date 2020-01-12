from django import forms
from .models import User, Profile


class AddCommentForm(forms.Form):
    comment = forms.CharField(max_length=500,
                              required=True,
                              widget=forms.Textarea(attrs={
                                  'placeholder': 'Ваш комментарий',
                                  'style': 'width: 90%;'
                              }))


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = Profile
        fields = ('job', 'biography', 'gender', 'country', 'birth')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
