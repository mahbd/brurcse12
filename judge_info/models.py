from django.db import models


class UriInfo(models.Model):
    name = models.CharField(max_length=100)
    profile_url = models.CharField(max_length=100)
    points = models.CharField(max_length=20)
    solves = models.IntegerField(default=0)

    class Meta:
        ordering = ['-solves']

    def __str__(self):
        return self.name
