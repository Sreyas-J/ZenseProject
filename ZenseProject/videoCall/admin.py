from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(RoomMember)
admin.site.register(Recording)