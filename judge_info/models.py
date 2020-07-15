from django.db import models


class UriInfo(models.Model):
    name = models.CharField(max_length=100)
    profile_url = models.CharField(max_length=100)
    points = models.CharField(max_length=20)
    solved = models.CharField(max_length=10)

    class Meta:
        ordering = ['-solved']

    def __str__(self):
        return self.name
