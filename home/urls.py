from django.contrib import admin
from django.urls import path
from home import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("contact/", views.contact, name="contact"),
    path("course/", views.course, name="course"),
    path("notes/", views.notes, name="notes"),
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/update/<int:pk>/", views.update_note, name="update_note"),
    path("notes/delete/<int:pk>/", views.delete_note, name="delete_note"),
    path("notes/download/<int:pk>/", views.download_note_image, name="download_note_image"),
]