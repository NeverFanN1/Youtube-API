from googleapiclient.discovery import build
import creds
import csv
import re

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


def pl_find(select, Id_list): #prints channel playlists?
    
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

#test code
def pl_find(pltitle_select): #prints channel playlists
    
    plId_list = []
    plTitle_list = []

    pl_request = youtube.playlists().list(
        part='contentDetails, snippet',
        channelId=pltitle_select
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


def vid_find(pl_id): #gets videos in playlist 
    vid_titlelist = []
    vid_channamelist = [] #for names of channels whose videos in playlist
    vid_idlist = [] # for video ids
    nextPageToken = None
    while True: #in while loop so can take more than 5 videos
        #gets playlist video IDs
        pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=pl_id,
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
            #print(i)
            vid_titlelist.append(i['snippet']['title'])
            vid_channamelist.append(i['snippet']['channelTitle'])
            vid_idlist.append(i['id'])

        nextPageToken = pl_response.get('nextPageToken') #returns non if no more pages 
        if not nextPageToken:
            break

    return vid_response,vid_titlelist, vid_channamelist, vid_idlist

def pl_csv(vid_titlelist, vid_chananmelist, vid_idlist):

    pl_vids = [
        {'Title': vid_title, 'Channel':vid_channel, 'Video ID':vid_id}
        for vid_title, vid_channel, vid_id in zip(vid_titlelist, vid_chananmelist, vid_idlist)
    ]


    with open('playlist.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Channel', 'Video ID']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(pl_vids)

def pl_url(url):
    regex = r"(?:list=)([a-zA-Z0-9_-]+)"

    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None



def menu():
    csvchoice = '0'
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
        plTitle_select = Id_list[select]
        plTitle_list, plId_list = pl_find(plTitle_select) #gets playlists from channel

        pl_search = 1

        while pl_search != 0:

            for i in range(len(Id_list)):
                print(i+1,end=", ")
                print(plTitle_list[i], end=", ")
                print(plId_list[i])
            
            pl_select = int(input("Select playlist: ")) #variable for selecting which playlist
            pl_select = pl_select - 1
            print("pl_select: ", pl_select)
            pl_id = plId_list[pl_select] 
            vid_response, vid_titlelist , vid_channamelist, vid_idlist = vid_find(pl_id) #gets videos in playlist

        
            for i in range(len(vid_titlelist)):
                print(i+1,end=", ")
                print("Title: ",vid_titlelist[i], " Channel: ", vid_channamelist[i], " Video ID: ", vid_idlist[i])
            
            pl_search = 0 #changed to 0 so it doesn't print willy nilly

            print()
            while csvchoice == '0':
                csvchoice = input("Want to print to csv? Y for yes, N for no: ")
                if csvchoice == 'y' or csvchoice == 'Y':
                    pl_csv(vid_titlelist, vid_channamelist, vid_idlist)
                    print("CSV printed")
                elif csvchoice == 'n':
                    break
                else:
                    print("Invalid input, enter 'y' or 'n'.")
                

        search = 0

def csvmenu(vid_titlelist, vid_channamelist, vid_idlist, go):
    csvchoice = '0'
    while csvchoice == '0':
        csvchoice = input("Want to print to csv? Y for yes, N for no: ")
        if csvchoice == 'y' or csvchoice == 'Y':
            pl_csv(vid_titlelist, vid_channamelist, vid_idlist)
            print("CSV printed")
        elif csvchoice == 'n':
            go = False
            return go
        else:
            print("Invalid input, enter 'y' or 'n'.")


def menu2():
    csvchoice = '0'
    choice = 1
    while choice != 0:
        choice2 = input("Enter 'a' search for channel and get playlists, 'b' to enter channel URL, 'c' to enter playlist URL, and 'd' to exit: ")
        if choice2 == 'a':
            channel = input("Enter channel to search for: ")
            print()

            Id_list, name_list = chan_search(channel) #searches channels
            
            for i in range(len(Id_list)): #prints out channel search
                print(i+1,end=", ")
                print(name_list[i], end=", ")
                print(Id_list[i])
                
            select = int(input("Select channel: ")) #selects channel
            select = select - 1
            plTitle_select = Id_list[select]
            plTitle_list, plId_list = pl_find(plTitle_select) #gets playlists from channel

            pl_search = 1

            while pl_search != 0:

                for i in range(len(Id_list)):
                    print(i+1,end=", ")
                    print(plTitle_list[i], end=", ")
                    print(plId_list[i])
                
                pl_select = int(input("Select playlist: ")) #variable for selecting which playlist
                pl_select = pl_select - 1
                print("pl_select: ", pl_select)
                pl_id = plId_list[pl_select] 
                vid_response, vid_titlelist , vid_channamelist, vid_idlist = vid_find(pl_id) #gets videos in playlist
                go  = True

            
                for i in range(len(vid_titlelist)):
                    print(i+1,end=", ")
                    print("Title: ",vid_titlelist[i], " Channel: ", vid_channamelist[i], " Video ID: ", vid_idlist[i])
                
                pl_search = 0 #changed to 0 so it doesn't print willy nilly

                go = csvmenu(vid_titlelist, vid_channamelist, vid_idlist, go)
                if go is False:
                    break

                print()
        elif choice2 == 'b': #will have option for getting channel ID from channel URL
            print("Placeholder")
        elif choice2 == 'c': #add option to search playlist videos by title or whatnot
            url = input("Enter playlist URL: ")
            pl_id = pl_url(url) #gets playlist ID from URL
            vid_response, vid_titlelist , vid_channamelist, vid_idlist = vid_find(pl_id)
            go  = True
            go = csvmenu(vid_titlelist, vid_channamelist, vid_idlist, go)
            if go is False:
                break
        elif choice2 == 'd':
            print("Exiting")
            choice = 1
        else:
            print("Wrong input entered")




            


#menu()
menu2()
