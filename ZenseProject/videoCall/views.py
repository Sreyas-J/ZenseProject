from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings

from agora_token_builder import RtcTokenBuilder
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

import random 
import time
import datetime

Id=os.getenv("APP_ID", None)
certificate=os.getenv("APP_CERTIFICATE",None)
expirationTime=3600*24
role=1

s3 = boto3.client('s3', aws_access_key_id=os.getenv("Access_key_ID", None), aws_secret_access_key=os.getenv("Secret_access_key", None), region_name='ap-south-1')
bucket='zense-project-videocall-recording'

def Token(request,group):
    channel=group
    timeStamp=time.time()
    privilegeExpiredTs=timeStamp+expirationTime
    uid=random.randint(1,2**32-1)
    token = RtcTokenBuilder.buildTokenWithUid(Id, certificate, channel, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe=False)

def record(request,group):
    user=request.user
    uid=request.GET.get("uid")
    rec=Recording.objects.create(name=user.username,uid=uid)
    rec.name=f"{rec.name}_{rec.created.strftime('%Y_%m_%d_%H_%M%S')}"
    rec.save()

    grp=Group.objects.get(name=group)
    grp.records.add(rec)
    grp.save()

    profile=Profile.objects.get(user=user)
    profile.recordings.add(rec)
    profile.save()

    s3.put_object(Bucket=bucket, Key=f'{group}/{user.username}/{uid}/')
    print(f'{group}/{rec.name}/')

    return JsonResponse({'name':rec.name,'time':rec.created},safe=False)

def update_record(request,group):
    try:
        SID=request.GET.get("sid")
        rec=Recording.objects.get(name=request.GET.get("rec_name"))
        rec.sid=SID
        rec.save()
        print("sid: ",rec.sid)
        return JsonResponse({"message": "Recording updated successfully"})
    except Recording.DoesNotExist:
        return JsonResponse({"error": "Recording not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required(login_url='videoCall:login') 
def home(request):
    profile=Profile.objects.get(user=request.user)
    return render(request,'home.html',{'groups':profile.groups.all(),"profile":profile})

@login_required(login_url='videoCall:login') 
def room(request,group):
    grp=Group.objects.get(name=group)
    return render(request,'room.html',{'group':grp,'profile':Profile.objects.get(user=request.user)})

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
        if request.POST.get("action")=="Done":
            print("done")
            return redirect('videoCall:home')
        else:
            return redirect('videoCall:addMember',group=group)

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
    print("Id: ",Id)
    return render(request,'lobby.html',{'room':group,'user':request.user,'id':Id,'customerKey':os.getenv("customerKey", None),'customerSecret':os.getenv("customerSecret", None)})

@csrf_exempt
def createMember(request):
    data=json.loads(request.body)

    member,created=RoomMember.objects.get_or_create(
        name=Profile.objects.get(user__username=data['name']),
        uid=data['UID'],
        room=data['room_name']
    )

    return JsonResponse({'name':data['name']},safe=False)

def createGroup(request):
    if request.method=="POST":
        name=request.POST.get("group")

        if Group.objects.filter(name=name).exists():
            messages.error(request,"This group already exists")

        else:
            s3.put_object(Bucket=bucket, Key=f'{name}/')
            icon_file = request.FILES.get('icon')
            icon_path = f'icon/{name}_{icon_file.name}'
            icon_path = default_storage.save(icon_path, icon_file)

            profile=Profile.objects.get(user=request.user)
            grp=Group.objects.create(name=name,setting=request.POST.get("setting"),icon=icon_path)

            profile.groups.add(grp)
            profile.admin.add(grp)
            profile.save()

            messages.success(request,f'{name} has been created')

            return redirect("videoCall:addMember",group=name)

    return render(request,"addGroup.html")


def get_presigned_url(group,recording):
    rec=Recording.objects.get(name=recording)
    grp=Group.objects.get(name=group)
    profile=Profile.objects.get(recordings=rec)

    if rec in grp.records.all():
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': f'{group}/{profile.user.username}/{rec.uid}/{rec.sid}_{group}_0.mp4'},
            ExpiresIn=3600  # URL expiration time in seconds
        )
        return presigned_url
    return None
    
def view_recording(request,group,record):
    url=get_presigned_url(group,record)
    print(url)
    if url:
        return render(request,"recording.html",{"url":url,"record":record,"group":Group.objects.get(name=group)})
    messages.error(request,"This recording doesn't exist")
    return redirect('videoCall:home')

def remove_member(request,group,member):
    grp=Group.objects.get(name=group)
    profile=Profile.objects.get(user=User.objects.get(username=member))
    profile.groups.remove(grp)
    profile.save()
    return redirect('videoCall:home')

def edit_recording(request,group,recording):
    rec=Recording.objects.get(name=recording)
    if request.method=="POST":
        name=request.POST.get("name")
        rec.name=name
        rec.save()
        messages.success(request,f'{recording} has been renamed to {name}')
        return redirect('videoCall:home')

    return render(request,'editRecording.html',context={"name":recording})