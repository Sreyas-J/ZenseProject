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

def Token(request,group):
    Id='41a16d737c284fadb182676757e070ab'
    certificate='49a7c4370085482f84c8e839e79ff023'
    channel=group
    uid=random.randint(1,230)
    expirationTime=3600*24
    timeStamp=time.time()
    privilegeExpiredTs=timeStamp+expirationTime
    role=1
    #print(Id,certificate,channel,uid,expirationTime,timeStamp,privilegeExpiredTs,role)

    token = RtcTokenBuilder.buildTokenWithUid(Id, certificate, channel, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe=False)

@login_required(login_url='signup') 
def home(request):
    profile=Profile.objects.get(user=request.user)
    return render(request,'home.html',{'groups':profile.groups.all()})

@login_required(login_url='signup') 
def room(request,group):
    return render(request,'room.html',{'room':group})

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        try:
            instance=User.objects.get(username=username)
            messages.error(request,'This user already exists. ')
            return redirect('signup')
        except:
            password=request.POST.get('password')
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('home')

    return render(request,'signup.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the profile or desired page after successful login
        else:
            # User authentication failed
            return render(request, 'login.html', {'error_message': 'Invalid credentials.'})
    
    return render(request, 'login.html')

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