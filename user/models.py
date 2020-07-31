from django.db import models
from django.contrib.auth.models import User

bg = (
    ('NOT', 'NOT'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    blood_group = models.CharField(max_length=5, blank=True, choices=bg)
    user_code = models.CharField(max_length=100, default='not_added')
    handle = models.CharField(max_length=100, default='not_added')
    profile = models.CharField(max_length=100, default='not_added')
    telegram_id = models.CharField(max_length=100, default='not_added')
    nick_name = models.CharField(max_length=100, default='not_added')

    class Meta:
        ordering = ['-blood_group']

    def __str__(self):
        return self.nick_name


class Token(models.Model):
    token = models.CharField(max_length=20)
    identity = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    # Register your models here.
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.type + self.token
