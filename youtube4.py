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
    #figure how to print search responses
    for i in search_response:
        print(search_response[i])


chan_search()