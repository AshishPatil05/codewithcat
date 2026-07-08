from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from .models import Contact, Note
import os

def home(request):
    return render(request, "index.html")

def aboutus(request):
    return render(request, "aboutus.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, "Data Submitted")
    return render(request, "contact.html")

def course(request):
    return render(request, "course.html")

@login_required(login_url="login")
def notes(request):
    notes_list = Note.objects.filter(user=request.user).order_by("-id")
    return render(request, "notes.html", {"notes_list": notes_list})

@login_required(login_url="login")
def add_note(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        Note.objects.create(
            user=request.user,
            title=title,
            description=description,
            image=image
        )
        return redirect("notes")
    return render(request, "add_note.html")

@login_required(login_url="login")
def update_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")
        if request.FILES.get("image"):
            note.image = request.FILES.get("image")
        note.save()
        return redirect("notes")
    return render(request, "update_note.html", {"note": note})

@login_required(login_url="login")
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect("notes")
    return render(request, "delete_note.html", {"note": note})

@login_required(login_url="login")
def download_note_image(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if not note.image:
        raise Http404("No image found")
    return FileResponse(note.image.open("rb"), as_attachment=True, filename=os.path.basename(note.image.name))

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
        auth_login(request, user)
        return redirect("home")

    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password")

    return render(request, "login.html")