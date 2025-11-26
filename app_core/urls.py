from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
    path("register/", RegisterView.as_view(), name="register"),
    path("legal/", LegalView.as_view(), name="legal")  
] 