from django.urls import path
from .views import HomePage, CompanyInfoView, ContactView, DestinationsView, AddReviewView, ReviewsView,RulesView
from . import views

app_name = 'aerorom'  # numele aplicatiei

# lista de rute specifice fiecarei pagini, utilizand clasele din views.py
urlpatterns = [
    path('home/', views.HomePage.as_view(), name='home'),
    path('company-info/', views.CompanyInfoView.as_view(), name='info'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('destinations/', views.DestinationsView.as_view(), name='destinations'),
    path('add-review/', views.AddReviewView.as_view(), name='add_review'),
    path('jobs/', views.JobInfoView.as_view(), name='jobs'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('rules/',views.RulesView.as_view(), name='rules'),
]
