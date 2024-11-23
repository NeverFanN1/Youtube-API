#final program
from googleapiclient.discovery import build
import creds

api_key = creds.api_key
youtube = build('youtube', 'v3', developerKey=api_key)

def chan_search(channel):
    
    search_request = youtube.search().list(
    part='snippet',
    #q='Corey Schafer',
    q=channel,
    type='channel',
    maxResults=2
    )
    search_response = search_request.execute()
    search_list = search_response['items']
    Id_list = []
    name_list = []
    
    for i in search_list:
        print(i['snippet']['channelId'])
        print(i['snippet']['title'])
        print()
            
        Id_list.append(i['snippet']['channelId'])
        name_list.append(i['snippet']['title'])

    return Id_list, name_list


def menu():
    search = 1
    while search != 0:
        channel = input("Enter channel to search for: ")

        #chan_search(channel)
        Id_list, name_list = chan_search(channel)
        print("IDs: ", Id_list)
        print("Channels: ", name_list)
        search = 0

#chan_search('Corey Schafer')
menu()
