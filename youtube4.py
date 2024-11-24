from googleapiclient.discovery import build
import creds

api_key = creds.api_key
youtube = build('youtube', 'v3', developerKey=api_key)

def chan_search(channel):
    
    search_request = youtube.search().list(
    part='snippet',
    q=channel,
    type='channel',
    maxResults=2
    )
    search_response = search_request.execute()
    search_list = search_response['items']
    Id_list = []
    name_list = []
    
    for i in search_list:
        #print(i['snippet']['channelId'])
        #print(i['snippet']['title'])
        #print()
            
        Id_list.append(i['snippet']['channelId'])
        name_list.append(i['snippet']['title'])

    return Id_list, name_list

def pl_find(select, Id_list, name_list):
    print("Entered func")
    for i in range(len(Id_list)):
        if Id_list[i] == select - 1:
            print("Entered if")
            pl_request = youtube.playlists().list(
                part='contentDetails, snippet',
                channelId=Id_list[i]
            )
            pl_response = pl_request.execute()

            for i in pl_response['items']:
                print(i)
                print()
        else:
            print("Entered else")



def menu():
    search = 1
    while search != 0:
        channel = input("Enter channel to search for: ")
        print()

        Id_list, name_list = chan_search(channel)
        #print("IDs: ", Id_list)
        #print("Channels: ", name_list)
        
        for i in range(len(Id_list)):
            print(i+1,end=", ")
            print(name_list[i], end=", ")
            print(Id_list[i])
            
        select = int(input("Select channel: "))
        pl_find(select, Id_list, name_list)

        #search = 0

menu()
