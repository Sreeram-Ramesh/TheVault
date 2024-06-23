from blog.models import Post , Comment , UserProfileInfo
from django import forms
from django.contrib.auth.models import User
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password','email')

class UserUpdateForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username']

class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic','bio')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','text')
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)
        widgets = {
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
