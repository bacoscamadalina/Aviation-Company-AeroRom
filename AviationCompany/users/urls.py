from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import MyLoginView, logout_view

app_name = 'users'
# lista cu URL-urile din users
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('contul_meu/', views.contul_meu, name='contul_meu'),
]
