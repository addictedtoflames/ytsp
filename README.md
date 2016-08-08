# ytsp
A simple tool to collate a list of youtube subscriptions from the command line and play them using mpv

# INSTALLATION

Install the required dependencies:
  ytsubs
  python-lxml
  python-texttable
  mpv
  
Save ytsp.py to a location of your choice

# USAGE

Run ytsp.py from a terminal
On first run you will see a setup prompt; fill in the required information:
  Username=your youtube username
  API Key=your youtube api key (see ytsubs documentation to find out how to get one)
  Collect videos from previous X days=number of days to collect videos from
  Maximum video height=maximum video resolution to play based on video height in pixels (e.g. 1080,720,360,etc.)
  
Once you have entered the necessary information the subscriptions list will begin to load. This will take a few minutes if you as the youtube v3 API is very inefficient at dealing with these requests.

Once the video list has loaded you can play a video by typing the number next to its title and hitting return.

To refresh the video list type 'r'

If you want to change your configuration (e.g. to change the video resolution of the number of days to collect video for, you can return to the setup prompts by typing 'setup' however you must retype the information for each prompt or it will be lost. I do intend to fix this at some point but for the time being users may prefer to manually edit the config file (located at ~/.config/ytsp/ytsprc) and then restart the program

To exit the program type 'q'

# NOTE

I am aware that my code is horrible, this is my first real coding project and I only wrote it because I needed it to do a job for me and it does do that job. I'm sharing it on the basis that others may find it useful so if anyone wants to suggest improvements or give me some pointers on where to learn how to code properly I would be very grateful, just please don't tell me my coding sucks, I already know that.
