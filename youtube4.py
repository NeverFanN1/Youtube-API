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
    
    for i in search_list: #keep this to make it print faster?
        #print(i['snippet']['channelId'])
        #print(i['snippet']['title'])
        #print()
            
        Id_list.append(i['snippet']['channelId'])
        name_list.append(i['snippet']['title'])

    return Id_list, name_list


def pl_find(select, Id_list): 
    
    plId_list = []
    plTitle_list = []

    pl_request = youtube.playlists().list(
        part='contentDetails, snippet',
        channelId=Id_list[select]
    )
    pl_response = pl_request.execute()

    for i in pl_response:
        print()

    for i in pl_response['items']:
        #print(i['id'])
        #print(i['snippet']['title'])
        #print()

        plId_list.append(i['id'])
        plTitle_list.append(i['snippet']['title'])
    
    return plTitle_list, plId_list


def vid_find(pl_select, plId_list):
    titleList = []
    nextPageToken = None
    while True: #in while loop so can take more than 5 videos
        #gets playlist video IDs
        pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=plId_list[pl_select],
        maxResults=50, #50 is the maximum number of results per page
        pageToken=nextPageToken
    )
        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response['items']: #gets videoIds of first 5 videos
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list( #requests info about videos
            part="snippet",
            id=','.join(vid_ids) #limit of 50 video ids
        )

        vid_response = vid_request.execute()

        for i in vid_response['items']:
            titleList.append(i['snippet']['title'])

        nextPageToken = pl_response.get('nextPageToken') #returns non if no more pages 
        if not nextPageToken:
            break

    return vid_response, titleList


def menu():
    search = 1
    while search != 0:
        channel = input("Enter channel to search for: ")
        print()

        Id_list, name_list = chan_search(channel)
        
        for i in range(len(Id_list)):
            print(i+1,end=", ")
            print(name_list[i], end=", ")
            print(Id_list[i])
            
        select = int(input("Select channel: "))
        select = select - 1
        plTitle_list, plId_list = pl_find(select, Id_list) #loop to keep trying pl_find?

        pl_search = 1

        while pl_search != 0:

            for i in range(len(Id_list)):
                print(i+1,end=", ")
                print(plTitle_list[i], end=", ")
                print(plId_list[i])
            
            pl_select = int(input("Select playlist: ")) #variable for selecting which playlist
            pl_select = pl_select - 1
            print("pl_select: ", pl_select)
            vid_response, titleList = vid_find(pl_select, plId_list)

            #print(vid_response)
            print(titleList) #make it print titleList with spaces down, but also print other aspects of viseos, like URL, and title length


        search = 0

menu()
