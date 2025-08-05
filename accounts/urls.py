from django.urls import path

from . import views


urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
]
