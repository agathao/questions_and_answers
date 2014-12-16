from django import forms
from models import TEXT_LENGTH
from models import TITLE_LENGTH

TEXT_HELP_MESSAGE = str(TEXT_LENGTH) + ' characters max.'
TITLE_HELP_MESSAGE = str(TITLE_LENGTH) + ' characters max.'

class CreateQuestion(forms.Form):
    question_title = forms.CharField(max_length=TITLE_LENGTH, help_text=TITLE_HELP_MESSAGE)
    tags = forms.CharField(required=False, help_text='Please provide comma separated list of tags')
    question = forms.CharField(widget=forms.Textarea, max_length=TEXT_LENGTH, help_text=TEXT_HELP_MESSAGE)   

class CreateAnswer(forms.Form):
    answer_title = forms.CharField(max_length=TITLE_LENGTH, help_text=TITLE_HELP_MESSAGE)
    answer = forms.CharField(widget=forms.Textarea, max_length=TEXT_LENGTH, help_text=TEXT_HELP_MESSAGE)
    
class ImageForm(forms.Form):
    imagefile=forms.ImageField(label="Select image to upload.")