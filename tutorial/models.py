from django.db import models
from django.contrib.auth.models import User


class ContestName(models.Model):
    contest_name = models.CharField(max_length=200)
    contest_link = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-end']

    def __str__(self):
        return self.contest_name


class Topics(models.Model):
    topic_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['topic_name']

    def __str__(self):
        return self.topic_name


class Tutorial(models.Model):
    tut_title = models.CharField(max_length=30)
    question_link = models.CharField(max_length=200, blank=True, null=True)
    tut_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    topic_name = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True, blank=True)
    contest_name = models.ForeignKey(ContestName, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    hidden = models.BooleanField(default=False, blank=True, null=True)
    beginner = models.CharField(max_length=50, blank=True, null=True)
    hidden_till = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.tut_title
