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
    dark_mode = models.BooleanField(default=False)
    blood_group = models.CharField(max_length=5, blank=True, choices=bg, default="NOT")
    user_code = models.CharField(max_length=100, default='not_added')
    handle = models.CharField(max_length=100, default='not_added')
    profile = models.CharField(max_length=100, default='not_added')
    telegram_id = models.CharField(max_length=100, default='not_added')
    nick_name = models.CharField(max_length=100, default='not_added')
    profile_image = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['nick_name']

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


class UserDevice(models.Model):
    username = models.CharField(max_length=100)
    device = models.TextField()
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-time']
