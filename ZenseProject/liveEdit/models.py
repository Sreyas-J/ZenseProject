from django.db import models

class Document(models.Model):
    name=models.CharField(max_length=100)
    content = models.TextField(null=True)
    
    def __str__(self):
        return self.content