from django.urls import path
from auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
]
