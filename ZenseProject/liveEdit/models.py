from django.db import models

class Document(models.Model):
    content = models.TextField()
    
    def __str__(self):
        return self.content