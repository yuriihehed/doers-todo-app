from django.db import models

# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=255)
    elapsed_time = models.DurationField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
