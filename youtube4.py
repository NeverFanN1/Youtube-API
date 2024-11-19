#final program
from googleapiclient.discovery import build
import creds

api_key = creds.api_key
youtube = build('youtube', 'v3', developerKey=api_key)

def chan_search():
    
    search_request = youtube.search().list(
    part='snippet',
    q='Corey Schafer',
    type='channel',
    maxResults=2
    )
    search_response = search_request.execute()
    search_list = search_response['items']
    print()
    #print(search_response['items'][0]['snippet']['channelId'])
    #print(search_response['items'][0]['snippet']['title'])
        #snippet = i.get('snippet', {})
        #print(snippet)
    
    for i in search_list:
        print(i['snippet']['channelId'])
        print(i['snippet']['title'])
        print()


chan_search()