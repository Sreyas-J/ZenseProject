from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    groups=models.ManyToManyField(Group,related_name='user_profile')
    
    def __str__(self):
        return self.user.username