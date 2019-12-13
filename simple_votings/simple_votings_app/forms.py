from django import forms


class AddVotingForm(forms.Form):
    question = forms.CharField(max_length=200, required=True, label='Ваш вопрос')
    answers = forms.CharField(widget=forms.Textarea(), required=False)
