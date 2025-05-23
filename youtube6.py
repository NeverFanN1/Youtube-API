from googleapiclient.discovery import build
import creds
import csv
import re
import requests

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


def pl_find(channelID): #prints channel playlists?
    
    plId_list = []
    plTitle_list = []

    pl_request = youtube.playlists().list(
        part='contentDetails, snippet',
        channelId=channelID
    )
    pl_response = pl_request.execute()

    for i in pl_response:
        print()

    for i in pl_response['items']:

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

def chan_search_menu():
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
    print("plTitle_select ,", plTitle_select)
    chan_playlist_print(plTitle_select)


def chan_url(url): #work on channel later, won't work for 
    gotId = False
    matchno = 0

    regex = re.compile(r"^https?://(?:www\.)?youtube\.com/(?:" 
                     r"channel/(UC[\w-]{22})|"    #Channel ID
                     r"c/([\w-]+)|"              #Custom URL
                     r"user/([\w-]+)|"           #/user
                     r"(@[\w-]+)"                #Handle URL
                     r")/?$")  #Make trailing slash optional

    match = re.search(regex, url)
    if match:
        if match.group(1):  #Channel ID (Starts with 'UC')
            matchno = 1
            return match.group(1), True, matchno
        elif match.group(2):  #Custom URL, works
            matchno = 2
            return match.group(2), False, matchno
        elif match.group(3):   #/user
            matchno = 3
            return match.group(3), False, matchno
        elif match.group(4):  #Handle (@username)
            matchno = 4
            print("matchno 4")
            return match.group(4), False, matchno
    else:
        print("Else")
        return None, False, -1
    
def chan_url_runner():
    url = input("Enter channel  URL: ")

    matchtest, gotId, matchno = chan_url(url)
    #print(matchtest)
    print(matchno)
    if matchno == 2 or matchno == 3:
        channelID = chan_username(matchtest)
        print(channelID)
        chan_playlist_print(channelID)
    elif matchno == 4:
        channelID = chan_handle(matchtest)
        print(channelID)
        chan_playlist_print(channelID)
    else:
        #channelID = chan_username(matchtest)
        print(matchtest) #matchtest should be channelID
        chan_playlist_print(matchtest)


def chan_playlist_print(channelID):
    plTitle_list, plId_list = pl_find(channelID) #gets playlists from channel

    if not plTitle_list:
        print("No public playlists found.\n")
        pl_search = 0
    else:
        pl_search = 1

    while pl_search != 0:

        for i in range(len(plTitle_list)):
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

#haven't tested chan_username() and chan_handle() before
def chan_username(username):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={username}&key={api_key}"
    response = requests.get(url).json()

    if "items" in response and response["items"]:
        return response["items"][0]["id"]  # Channel ID
    else: # or return none
        print("ID not found by chan_username()")
        return None

def chan_handle(handle):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={handle}&key={api_key}"

    response = requests.get(url).json()
    if "items" in response and response["items"]:
        return response["items"][0]["id"] #channel id
    else: # or return none
        print("ID not found by chan_handle()")
        return None



#maybe change menu csv thing to broader function?
def menu2():
    csvchoice = '0'
    choice = 1
    while choice != 0:
        choice2 = input("\nEnter 'a' search for channel and get playlists, 'b' to enter channel URL, 'c' to enter playlist URL, and 'd' to exit: ")
        if choice2 == 'a':
            chan_search_menu()
        elif choice2 == 'b':
            chan_url_runner()
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




menu2()
