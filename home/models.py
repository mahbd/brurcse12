from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea

Text30Dict = {'id': 'Text30', 'class': 'form-control', 'style': 'background-color: #b8daff', 'rows': 1}
Text00Dict = {'id': 'Text00', 'class': 'form-control', 'style': 'background-color: #b8daff', 'rows': 10}


class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.question


class Announce(models.Model):
    ann_title = models.CharField(max_length=30)
    ann_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.ann_title


class UpdateTime(models.Model):
    topic = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True, default=0)


class AnnForm(ModelForm):
    class Meta:
        model = Announce
        fields = ['ann_title', 'ann_text']
        labels = {'ann_title': 'Announcement Title', 'ann_text': 'Announcement text'}
        widgets = {
            'ann_title': Textarea(attrs=Text30Dict),
            'ann_text': Textarea(attrs=Text00Dict),
        }
        error_messages = {
            'ann_title': {
                'max_length': "Title is too big",
                'required': "Don't Keep it blank"
            },
            'ann_text': {
                'required': "Don't Keep it blank"
            }
        }


class SecretKeys(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DData(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default='all')
    data = models.TextField()
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-added']
        verbose_name_plural = 'dData'
