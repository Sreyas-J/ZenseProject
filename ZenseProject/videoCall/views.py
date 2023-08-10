from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time

def Token(request):
    Id='41a16d737c284fadb182676757e070ab'
    certificate='49a7c4370085482f84c8e839e79ff023'
    channel=request.GET.get('channel')
    uid=random.randint(1,230)
    expirationTime=3600*24
    timeStamp=time.time()
    privilegeExpiredTs=timeStamp+expirationTime
    role=1
    print(Id,certificate,channel,uid,expirationTime,timeStamp,privilegeExpiredTs,role)

    token = RtcTokenBuilder.buildTokenWithUid(Id, certificate, channel, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe=False)

def home(request):
    return render(request,'home.html')

def room(request):
    return render(request,'room.html')

def signup(request):
    return render(request,'signup.html')