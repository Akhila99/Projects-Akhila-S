from django.urls import path
from . import views1

urlpatterns = [
    path('', views1.index1, name='index1'),
]
