from django import forms
from django.contrib.auth.models import User
from django.db import models


class Keywords(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Problems(models.Model):
    name = models.TextField(blank=True, null=True)
    link = models.URLField()
    solve = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    tags = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(blank=True, null=True)
    total_visit = models.TextField(blank=True, null=True)
    creator = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']


class Topic(models.Model):
    name = models.TextField()
    problems = models.ManyToManyField(Problems, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(blank=True, null=True)
    total_visit = models.TextField(blank=True, null=True)
    creator = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date']


class Technique(models.Model):
    topic = models.ManyToManyField(Topic, blank=True)
    problems = models.ManyToManyField(Problems, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(blank=True, null=True)
    total_visit = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    keywords = models.ManyToManyField(Keywords, blank=True)
    code = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ['date']


class Handle(models.Model):
    handle = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    last_submission = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProblemForm(forms.Form):
    link = forms.URLField(required=True)
    solved = forms.URLField(required=False)
