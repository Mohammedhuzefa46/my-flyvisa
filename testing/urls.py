# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit-email/', views.submit_email, name='submit_email'),
    path('subscribe/', views.subscribe_email, name='subscribe_email'),
]
