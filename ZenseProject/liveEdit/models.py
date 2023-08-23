from django.db import models

options = (
    ("ADMIN", "ADMIN"),
    ("EVERYONE", "EVERYONE"),
)

class Document(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(null=True)
    setting = models.CharField(max_length=15, choices=options)

    def __str__(self):
        return self.name
