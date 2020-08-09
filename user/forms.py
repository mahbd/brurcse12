from django import forms
from .models import UserInfo


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['blood_group', 'handle', 'profile', 'telegram_id', 'nick_name']
