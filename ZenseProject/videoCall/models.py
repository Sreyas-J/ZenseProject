from django.db import models
from django.contrib.auth.models import User
from liveEdit.models import Document,options

class Recording(models.Model):
    name=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    uid=models.CharField(max_length=25)
    sid=models.CharField(max_length=25,null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Group(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    doc=models.ManyToManyField(Document,related_name='groups')
    setting=models.CharField(max_length=15,choices=options)
    records=models.ManyToManyField(Recording,related_name='room')
    icon=models.ImageField(upload_to='icon',null=True,default="")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    groups=models.ManyToManyField(Group,related_name='user_profile')
    admin=models.ManyToManyField(Group,related_name='admin_right')
    recordings=models.ManyToManyField(Recording,related_name='recorder')
    
    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    description=models.TextField()
    seen=models.ManyToManyField(Profile,related_name='seen_notifications')
    created=models.DateTimeField(auto_now_add=True)
    profiles=models.ManyToManyField(Profile,related_name='all_notifications')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.description
    
class RoomMember(models.Model):
    name=models.ForeignKey(Profile,related_name='room',on_delete=models.CASCADE)
    uid=models.CharField(max_length=5)
    room=models.CharField(max_length=100)

    def __str__(self):
        return self.name.user.username