from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BlogModel, File


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=36, required=True)
    last_name = forms.CharField(max_length=36, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AuthForm(forms.Form):
    username = forms.CharField(max_length=36)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateBlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'special',
                                                          'placeholder': 'Заголовок'
                                                          }),
                            label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form_control',
                                                           'placeholder': 'Содержание'
                                                           }),
                              label='')

    class Meta:
        model = BlogModel
        fields = ['title', 'content', 'created_by']


class FileBlogForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = File
        fields = ['file']
