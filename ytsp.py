#!/usr/bin/python

## Import xml parser
from lxml import etree
## Print function
import pprint
## Call system processes
from subprocess import call
## Allows writing data to a file
from contextlib import redirect_stdout
## Allow use of ~ for home directory
from os.path import expanduser
import os
import configparser
import texttable as tt

call(["clear"])
## Check if config directory is set up correctly and contains the right files
confdir = expanduser("~") + "/.config/ytsp/"
if not os.path.exists(confdir):
    os.mkdir(confdir)

config = configparser.ConfigParser()

def setup():
    configfile = open(confdir + "ytsprc", "+w")    
    try:
        config.add_section('ytsubs') 
    except configparser.DuplicateSectionError:
        pass
    username = input("Username: ")
    if username is not '':
        config.set('ytsubs', 'username', username)
    key = input("API Key: ")
    if key is not '':
        config.set('ytsubs', 'key', key)
    days = input("Collect vidoeos from previous x days: ")
    if days is not '':
        config.set('ytsubs', 'days', days)
    resolution = input("Maximum video height: ")
    if resolution is not '':
        config.set('ytsubs', 'height', resolution)
    config.write(configfile)
    configfile.close()
    main()
    

## Displays help information
def help():
    call(["clear"])
    print("Type a number to play the corresponding video \n\n Type 'q' to exit program \n Type 'r' to refresh video listing. (Note that this may take some time depending on the number of channels you are subscribed to) \n Type 'setup' for setup \n Type 'h' to display this message again\n\n")

## Parse config directory
def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
               DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
## Refreshes subscription list
def refresh():
    config.read(confdir + "ytsprc")
    username = ConfigSectionMap("ytsubs")['username']
    key = ConfigSectionMap("ytsubs")['key']
    days = ConfigSectionMap("ytsubs")['days']
    call(["clear"])
    print("Refreshing subscriptions list. This may take a few minutes")
    subscriptions = open(confdir + "subscriptions.rss", 'w')
    call(["ytsubs", "-c", username, "-k",  key, "-s", days], stdout=subscriptions)
    main()
    

def main():
    rssFeed = confdir + r'subscriptions.rss'
    try:
        tree = etree.parse(rssFeed)
    except SyntaxError:
        refresh()
    link = []
    tag_path = tree.xpath('//item')
    number = 1
## Print list of videos
    videos = tt.Texttable()
    header = ['', 'Video Title', 'Date Uploaded']
    videos.header(header)
    for elem in tag_path:
        if elem.find('.//title') is not None:
            num = str(number)
            item = elem.xpath('.//title')[0].text.split('*')
            video = str(item)[2:-2]
            datestamp = elem.xpath('.//published')[0].text.split('*')
            date = str(datestamp)[2:-2]
            #print(str(number) + '. ' + str(item)[2:-2])
            row = [ num, video, date]
            videos.add_row(row)
            number = number+1
            
## Table Formating
    videos.set_cols_width([4,72, 28])
    videos.set_cols_align(['l','l','r'])
    videoList = videos.draw()
    print(videoList)
## Select list of links for videos and write to 'link' variable
    for elem in tag_path:
     if elem.find('.//link') is not None:
         link.append(elem.xpath('.//link')[0].text.split('   '))

## Prompt for video selection or command
    instruction = input('Select a video or enter a command: ')
## Test if input is an integer
    try:
        vidNum = int(instruction)
## Test if integer is in range
        try:
            vidLink = ''.join(str(link[vidNum-1]))
## If integer is out of range print error message and return to selection screen
        except IndexError:
            call(["clear"])
            print("There is no video with this number")
            main()
## If no exceptions play the selected video
        config.read(confdir + "ytsprc")
        height = ConfigSectionMap("ytsubs")['height']
        call(["mpv", "--ytdl-format=bestvideo[height<=?"+height+"]+bestaudio/best", vidLink[2:-2]])
## If input is not an integer see if there is a command with that name
    except ValueError:
## Exit program by pressing 'q'
        if instruction == 'q':
            exit()
        elif instruction == 'setup':
            setup()
        elif instruction == 'h':
            help()
        elif instruction == 'r':
            refresh()
## If no option with that name, print error message and return to selection screen
        else:
            call(["clear"])
            print("Not a valid option or video number")
            main()
        
# Return to selection screen once script is complete
    main()

## Initial call of main function
help()
main()
