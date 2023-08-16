from django.shortcuts import render

def doc(request,group,doc):
    return render(request,'doc.html')
