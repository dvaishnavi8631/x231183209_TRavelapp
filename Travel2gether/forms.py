# pylint: disable=C0115
""" forms.py file 
    for the TravelSosh
    app """
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Post, Comment


# Form for registering new user
class UserForm(forms.ModelForm): # class for the userform
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# Form for updating user email
class UpdateUserForm(forms.ModelForm): # class for updating userform
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ['email']


# Form for updating profile
class UpdateProfileForm(forms.ModelForm): # class for updating the profile

    class Meta:
        model = Profile
        fields = ['status_info', 'profile_photo']


# Form for creating a post
class CreatePost(forms.ModelForm): # class for creating post

    class Meta:
        model = Post
        fields = ['post_text', 'post_picture']


# Form for creating a comment
class CreateComment(forms.ModelForm): # class for creating comment

    class Meta:
        model = Comment
        fields = ['comment_text']
