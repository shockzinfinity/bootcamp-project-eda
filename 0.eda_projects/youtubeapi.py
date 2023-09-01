import requests
import pandas as pd
from urllib import parse

class YoutubeApi():
  def __init__(self, apiKey, use_columns = []):
    self.apiKey = apiKey
    self.use_columns = use_columns
    self.url = 'https://youtube.googleapis.com/youtube/v3/'
  
  def search_channel_id_by(self, names):
    query = f"search?part=id&key={self.apiKey}&type=channel&q={parse.quote(names)}"
    channel_id = requests.get(self.url + query).json()['items'][0]['id']['channelId']
    
    return channel_id
  
  def search_videos(self, searchTerm, publishedAfter='2018-01-01T00:00:00Z', publishedBefore='2019-01-01T00:00:00Z'):
    query = f"search?part=snippet&key={self.apiKey}&maxResults=10&publishedAfter={publishedAfter}&publishedBefore={publishedBefore}&order=viewcount&type=video&q={parse.quote(searchTerm)}"
    results = requests.get(self.url + query).json()
    
    return results['items']
  
  def get_channel_statistics_by(self, channelId):
    query = f"channels?part=statistics&key={self.apiKey}&id={channelId}"
    stats = requests.get(self.url + query).json()['items'][0]['statistics']
    
    return stats

  def get_video_statistics_by(self, videoId):
    query = f"videos?part=statistics&maxResults=1&key={self.apiKey}&id={parse.quote(videoId)}"
    stats = requests.get(self.url + query).json()
    
    return stats['items'][0]['statistics']
  
  def get_video_dataframe(self, items, country):
    videos = pd.DataFrame()
    
    for item in items:
      query = f"videos?part=snippet,statistics&maxResults=1&key={self.apiKey}&id={parse.quote(item['id']['videoId'])}"
      res = requests.get(self.url + query).json()

      video = pd.json_normalize(res['items'][0]['snippet'])
      video['videoId'] = res['items'][0]['id']
      video['country'] = country
      
      stats = pd.json_normalize(res['items'][0]['statistics'])

      video = pd.concat([video, stats], axis=1)
      videos = pd.concat([videos, video])
    
    if len(self.use_columns) > 0:
      videos = videos[self.use_columns]
    
    # count data type 변환
    videos[['viewCount', 'likeCount', 'favoriteCount', 'commentCount']] = videos[['viewCount', 'likeCount', 'favoriteCount', 'commentCount']].fillna(0).astype('int64')
    
    # datetime 변환 및 추가 컬럼 설정
    videos['publishedAt'] = pd.to_datetime(videos['publishedAt'])
    videos['publishedAtYear'] = videos['publishedAt'].dt.year
    videos['publishedAtMonth'] = videos['publishedAt'].dt.month
    # videos['prevYear'] = videos['publishedAt'] + pd.DateOffset(years=-1)
    # videos['prevMonth'] = videos['publishedAt'] + pd.DateOffset(years=-1)
    # videos['nextYear'] = videos['publishedAt'] + pd.DateOffset(years=1)
    # videos['nextMonth'] = videos['publishedAt'] + pd.DateOffset(years=1)
    
    videos = videos.reset_index(drop=True)
    
    return videos

    