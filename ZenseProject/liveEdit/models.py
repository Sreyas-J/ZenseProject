from django.db import models

class Document(models.Model):
    options=(
        ("ADMIN","ADMIN"),
        ("EVERYONE","EVERYONE"),
    )

    name=models.CharField(max_length=100)
    content = models.TextField(null=True)
    setting=models.CharField(max_length=15,choices=options)
    
    def __str__(self):
        return self.name