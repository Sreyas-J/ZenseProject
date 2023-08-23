from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required

from videoCall.models import *

@login_required(login_url='videoCall:login')
def doc(request,group,doc):
    profile=Profile.objects.get(user=request.user)
    if Group.objects.get(name=group) not in profile.groups.all():
        return HttpResponse("You don't have access to this group", status=403)

    return render(request,'doc.html',{"Room":group,"Doc":doc})
