from django.contrib.auth.models import User
from django.db import models


class GroupInfo(models.Model):
    name = models.CharField(max_length=50)
    User = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Message(models.Model):
    SUBJECT_MAX_LENGTH = 120
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    telegram_sender = models.CharField(max_length=200, null=True, blank=True)
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE, null=True, blank=True)
    recipient_id = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_archived = models.BooleanField(default=False)
    recipient_archived = models.BooleanField(default=False)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
    # moderation fields
    moderation_status = models.CharField(max_length=1, default='a')
    moderation_by = models.CharField(max_length=150, null=True, blank=True)
    moderation_date = models.DateTimeField(null=True, blank=True)
    moderation_reason = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.message[:50]


class LastMessage(models.Model):
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    recipient_id = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    room_name = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.message

    def group_check(self, group_id):
        return self.group.id == group_id
