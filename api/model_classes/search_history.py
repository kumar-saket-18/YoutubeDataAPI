from django.conf import settings
from django.db import models

class SearchHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    video_id = models.CharField(max_length=255)
    video_title = models.CharField(max_length=25000)
    description = models.CharField(max_length=25000)
    published_datetime = models.DateTimeField()
    thumbnail = models.CharField(max_length=4000)
    duration = models.IntegerField()
    filtered_title = models.CharField(max_length=10000)
    url = models.CharField(max_length=255)

class Meta:
    managed = settings.IS_TESTING
    db_table = 'search_history'