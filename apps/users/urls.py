from django.urls import path
from apps.users.views import auth_views

# Placeholder URL patterns - Views need to be implemented first
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', auth_views.RegisterView.as_view(), name='register'),
]
