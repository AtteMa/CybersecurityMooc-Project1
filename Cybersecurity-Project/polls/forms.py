from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth import password_validation
from django.forms import inlineformset_factory

class UserRegistrationForm(UserCreationForm):
    email = None
    password = None

    class Meta:
        model = UserModel
        fields = ("username","password")

class AddPoll(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['question_text','pub_date']

class AddChoice(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ['choice_text']

QuestionMetaInlineFormset = inlineformset_factory(
    models.Question,
    models.Choice,
    form=AddChoice,
    extra=3
)