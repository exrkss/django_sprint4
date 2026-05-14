from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('registration/', views.registration, name='registration'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
