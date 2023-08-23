from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from videoCall.models import *

@login_required(login_url='videoCall:login')
def doc(request,group,doc):
    profile=Profile.objects.get(user=request.user)
    grp=Group.objects.get(name=group)

    if grp not in profile.groups.all():
        messages.error(request,"You don't have access to this group")
        return redirect("videoCall:home")
    
    document=Document.objects.get(name=doc)
    context={"Room":grp,"Doc":document}

    if document in grp.doc.all():

        if document.setting=="ADMIN":
            context["admin"]=Profile.objects.filter(admin=grp)
            context["profile"]=profile

    else:
        messages.error(request,"There's no such document")
        return redirect("videoCall:home")
    
    return render(request,'doc.html',context)
