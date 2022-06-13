from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from string import Template

from AskKozlovApp.models import Profile, Question, Tag, User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.ModelForm):
    login = forms.CharField(label='Login')
    nickname = forms.CharField(label='Nickname', required=False)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    repeat_password = forms.CharField(widget=forms.PasswordInput(), label='Repeat Password')
    user_pfp = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = Profile
        fields = ['login', 'nickname', 'email', 'password', 'repeat_password', 'user_pfp']

    def clean_repeat_password(self):
        password_one = self.cleaned_data['password']
        password_two = self.cleaned_data['repeat_password']
        if password_one != password_two:
            self.add_error('password', '')
            raise ValidationError('passwords do not match')


class QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Question title')
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter a question'}), label='Question text')
    tags = forms.TypedMultipleChoiceField(choices=Tag.objects.all().values_list("pk", "tagname"), label='Tags')

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter an answer',
                                                         'class': 'form-control your-answer-form'}), label='',)

    class Meta:
        model = Question
        fields = ['text']


class SettingsForm(forms.ModelForm):
    login = forms.CharField(label='Login')
    email = forms.EmailField(label='E-mail')
    nickname = forms.CharField(label='Nickname', required=False)
    user_pfp = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = User
        fields = ['login', 'email', 'nickname', 'user_pfp']
