from .views import RegistrationView, UsernameValidationView, EmailValidationView, LogoutView, VerificationView, LoginView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    #path("login_view", views.login_view, name="login"),
    #path("logout", views.logout_view, name="logout"),
    #path("register", views.register, name="register"),
    #path("userdetails", views.UserDetailsView, name="userdetails"),
    path("createListing", views.createListing, name="createListing"),
]
