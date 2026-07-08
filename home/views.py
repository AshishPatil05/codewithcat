
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
        messages.success(request,"Data Submitted")
    return render(request,'contact.html')

def course(request):
    return render(request,'course.html')

def notes(request):
    return render(request,'notes.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "signup.html")

        user = User.objects.create_user(username=username, password=password1)
        user.save()
        login(request, user)
        return redirect("home")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "login.html")

    return render(request, "login.html")