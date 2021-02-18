from django.urls import path
from . import views

urlpatterns = [
    path('', views.YoutubeSearch.as_view(), name='youtube_search'),
]