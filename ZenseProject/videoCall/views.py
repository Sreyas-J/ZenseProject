from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

from agora_token_builder import RtcTokenBuilder
import random 
import time

Id='41a16d737c284fadb182676757e070ab'
certificate='49a7c4370085482f84c8e839e79ff023'
expirationTime=3600*24
role=1

def Token(request,group):
    channel=group
    timeStamp=time.time()
    privilegeExpiredTs=timeStamp+expirationTime
    uid=random.randint(1,2**32-1)
    token = RtcTokenBuilder.buildTokenWithUid(Id, certificate, channel, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe=False)

@login_required(login_url='videoCall:login') 
def home(request):
    profile=Profile.objects.get(user=request.user)
    return render(request,'home.html',{'groups':profile.groups.all()})

@login_required(login_url='videoCall:login') 
def room(request,group):
    grp=Group.objects.get(name=group)
    #context={}

    # if request.method=="POST":
    #     if "yes" in request:
    #         channel=group
    #         timeStamp=time.time()
    #         privilegeExpiredTs=timeStamp+expirationTime
    #         uid=random.randint(1,2**32-1)
    #         token = RtcTokenBuilder.buildTokenWithUid(Id, certificate, channel, uid, role, privilegeExpiredTs)
    #         context={"rec_uid":uid,"rec_token":token}
            
    #context['group':grp]

    return render(request,'room.html',{'group':grp})

@login_required(login_url='videoCall:login')
def addMember(request, group):
    grp = Group.objects.get(name=group)

    if request.method=='POST':
        name=request.POST.get('member')
        profile=Profile.objects.get(user__username=name)

        if grp in profile.groups.all():
            messages.error(request,f'{name} is already in {group}')
            return redirect('videoCall:home')

        profile.groups.add(grp)
        profile.save()

        messages.success(request,f'{name} has been added to {group}')
        return redirect('videoCall:home')

    return render(request,'addMember.html',{'profiles':Profile.objects.exclude(groups=grp)})

@login_required(login_url='videoCall:login')
def addDoc(request,group):
    grp=Group.objects.get(name=group)
    profile=Profile.objects.get(user=request.user)

    if grp not in profile.groups.all():
        messages.error(request,f"You aren't a member of {group}")
        return redirect('videoCall:home')
    
    if request.method=="POST":
        doc_name=request.POST.get('document')
        try:
            Document.objects.get(name=doc_name,groups=grp)
        except:
            document=Document.objects.create(name=doc_name,setting=request.POST.get("setting"))

            grp.doc.add(document)
            grp.save()
            messages.success(request,f"{doc_name} has been created in {group}")
            return redirect('videoCall:home')
        messages.error(request,f"Document with name:{doc_name} already exists in the group")
        return redirect('videoCall:addDoc',group=group)

    return render(request,'addDoc.html',{'group':grp})

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        try:
            instance=User.objects.get(username=username)
            messages.error(request,'This user already exists. ')
            return redirect('videoCall:signup')
        except:
            password=request.POST.get('password')
            confirm_password=request.POST.get('confirm_password')
            if password==confirm_password:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user)
                login(request,user)
            else:
                messages.error(request,"Password and Confirm password don't match.")
                return redirect('videoCall:signup')
            return redirect('videoCall:home')

    return render(request,'signup.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('videoCall:home')  # Redirect to the profile or desired page after successful login
        else:
            # User authentication failed
            return render(request, 'login.html', {'error_message': 'Invalid credentials.'})
    
    return render(request, 'login.html')

@login_required
def lobby(request,group):
    return render(request,'lobby.html',{'room':group,'user':request.user})

@csrf_exempt
def createMember(request):
    data=json.loads(request.body)

    member,created=RoomMember.objects.get_or_create(
        name=Profile.objects.get(user__username=data['name']),
        uid=data['UID'],
        room=data['room_name']
    )

    return JsonResponse({'name':data['name']},safe=False)