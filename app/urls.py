from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.google_login, name="oauth-login-google"),
    path("logout", views.logout_session, name="logout"),
]
