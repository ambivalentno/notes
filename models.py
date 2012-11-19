from django.db import models


class Note(models.Model):

    title = models.CharField(max_length=50)
    text = models.TextField()
    image = models.ImageField(upload_to = 'images/', null=True, blank=True)

    def __unicode__(self):
        return self.title
