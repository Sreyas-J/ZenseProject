from django.db import models

class Document(models.Model):
    name=models.CharField(max_length=100)
<<<<<<< HEAD
    content = models.TextField(null=True)
=======
    content = models.TextField()
>>>>>>> 193076cf095e1cf2b4ad889d7eb75c93e4744e43
    
    def __str__(self):
        return self.name