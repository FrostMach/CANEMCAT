from django.contrib import admin
from django.urls import path, include
from users.views import landing_page
urlpatterns = [
    path('', landing_page, name='landing_page'),
]