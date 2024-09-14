from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.scrape_wikipedia, name='scrape_wikipedia'),
]
