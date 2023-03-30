from django.db import models

# Create your models here.
class Youtube(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    file_object = models.FileField(null=True, blank=True)
    file_type = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.title} | audio"
