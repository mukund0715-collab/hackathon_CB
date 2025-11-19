from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('analyze/<int:email_id>/', views.analyze_email, name='analyze_email'),
]