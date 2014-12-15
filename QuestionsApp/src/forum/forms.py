from django import forms

class CreateQuestion(forms.Form):
    question = forms.CharField(widget=forms.Textarea, max_length=10000, help_text='10000 characters max.')
    tags = forms.CharField(required=False, help_text='Please provide comma separated list of tags')

class CreateAnswer(forms.Form):
    answer = forms.CharField(widget=forms.Textarea, max_length=10000, help_text='10000 characters max.')