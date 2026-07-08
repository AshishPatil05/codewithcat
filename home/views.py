from django.shortcuts import render,HttpResponse
from home.models import Contact

# Create your views here.
def home(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'aboutus.html')

def contact(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name,email=email,message=message)
        contact.save()
    return render(request,'contact.html')

def course(request):
    return render(request,'course.html')

def notes(request):
    return render(request,'notes.html')

