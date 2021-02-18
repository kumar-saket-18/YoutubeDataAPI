import re
import operator
import requests
import random

from django.shortcuts import render
from django.conf import settings
from isodate import parse_duration, parse_datetime
from api.models import SearchHistory
from rest_framework.views import APIView
from nltk.corpus import stopwords
# Create your views here.
class YoutubeSearch(APIView):
    def get(self, request, *args, **kwargs):
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        youtube_data_api_key = self.get_random_api_key()
        search_params = {
            'part' : 'snippet',
            'q' : 'cricket',
            'key' : youtube_data_api_key,   # fetching the youtube_data_api_key randomly
            'maxResults' : 10, # limiting the obtained resulting number of videos to 10
        }

        video_ids = []
        resp = requests.get(search_url, params=search_params)
        results = resp.json()['items']
        for  result in results:
            video_ids.append(result['id']['videoId'])
        video_params = {
            'key' : youtube_data_api_key,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 10, # limiting the obtained resulting number of videos to 10
        }

        resp = requests.get(video_url, params=video_params)
        results = resp.json()['items']

        videos = []
          

        for result in results:
            title = re.sub('\W+',' ', result['snippet']['title'])  # filtering out all the non-essential punctuations from title.
            word_list = title.split(' ')
            filtered_words = [word for word in word_list if word not in stopwords.words('english')]
            filtered_title = ' '.join(filtered_words)

            video_data = {
                'title' : result['snippet']['title'],
                'description' : result['snippet']['description'],
                'published_datetime' : parse_datetime(result['snippet']['publishedAt']),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }', # passing this in context will help in redirect to the selected video
                'id' : result['id'],
            }
            videos.append(video_data)
            
            videos.sort(key = operator.itemgetter('published_datetime'))
            new_search  = SearchHistory()
            new_search.video_id = result['id']
            new_search.video_title = result['snippet']['title']
            new_search.description = result['snippet']['description']
            new_search.published_datetime  = parse_datetime(result['snippet']['publishedAt'])
            new_search.thumbnail = result['snippet']['thumbnails']['high']['url']
            new_search.duration = int(parse_duration(result['contentDetails']['duration']).total_seconds()//60)
            new_search.url = f'https://www.youtube.com/watch?v={ result["id"] }'
            new_search.filtered_title = filtered_title
            new_search.save()

        context = {
            'videos' : videos
        }
        return render(request, 'search/index.html', context)

    def post(self, request, *args, **kwargs):
        videos = []
        search_string = request.data.get('search').lower()
        words = SearchHistory.objects.all()  # fetching all the rows to match the input string
        for row in words:
            if str.__contains__((row.video_title).lower(),search_string):
                video_data = {
                    'title' : row.video_title,
                    'description' : row.description,
                    'published_datetime' : row.published_datetime,
                    'thumbnail' : row.thumbnail,
                    'duration' : row.duration,
                    'url' : row.url, # passing this in context will help in redirect to the selected video
                    'id' : row.video_id,
                }
                videos.append(video_data)

        context = {
            'videos' : videos
        }
        return render(request, 'search/index.html', context)

    def get_random_api_key(self):
        key_list = []
        key_list.append('AIzaSyA6jMSEfy3eJOqQ1NmIpL8-iMbIxZO8XNk')
        key_list.append('AIzaSyDm-tV-X4xA1VHTJSLvUlTBJ2-J2awJ9hk')
        key_list.append('AIzaSyBb-QyCWhOnsTanrtjbWVvAjb1Ryghsrmo')
        key_list.append('AIzaSyCE4_eYSRR_PGyfg96mFanAzPdSzBlN2io')
        return random.choice(key_list)