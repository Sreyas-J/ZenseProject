from django.db import models
from django.contrib.auth.models import User
from liveEdit.models import Document

class Group(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    doc=models.ManyToManyField(Document,related_name='groups')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    groups=models.ManyToManyField(Group,related_name='user_profile')
    
    def __str__(self):
        return self.user.username
    
class RoomMember(models.Model):
    name=models.ForeignKey(Profile,related_name='room',on_delete=models.CASCADE)
    uid=models.CharField(max_length=5)
    room=models.CharField(max_length=100)

    def __str__(self):
        return self.name.user.username