#!/usr/bin/python
import sys, snnow, os
from cookies import Cookies
from optparse import OptionParser

# parse the options
parser = OptionParser()
parser.add_option('-u', '--user', type='string', dest='user',
                  help="Username for authentication")
parser.add_option('-p', '--password', type='string', dest='password',
                  help="Password for authentication")
parser.add_option('-i', '--id', type='int', dest='id',
                  help="Channel ID")
parser.add_option('-m', '--mso', type='string', dest='mso', default='Rogers',
                  help="Multi-system operator (eg: Rogers)")
parser.add_option('-f', '--ffplay', action="store_true", dest='ffplay',
                  help='Choose a stream and get it ready for ffplay')

(options, args) = parser.parse_args()

if not options.user:
    print "ERROR: Please specify user name.\n"
    parser.print_help()
    sys.exit(1)
elif not options.password:
    print "ERROR: Please specify a pasword\n"
    parser.print_help()
    sys.exit(1)

sn = snnow.SportsnetNow()
channels = sn.getChannels()
guide = sn.getGuideData()
abbr = None

for channel in  channels:

    if options.id:
        if options.id == channel['id']:
            abbr = channel['abbr']

    prog = guide[str(channel['id'])]
    print str(channel['id']) + ') ' + channel['name'] + ' (' + \
          channel['abbr'] + ') - ' + str(prog)

if abbr:
    if not sn.authorize(options.user, options.password, options.mso):
        sys.exit(1)
    print "Authorization Complete."
    stream = sn.getChannel(options.id, abbr, options.mso)
    if not stream:
        print "Unable to get stream"
        sys.exit(0)

    cookies = []
    streams = sn.parsePlaylist(stream, cookies)
    print cookies
    bitrates = [int(x) for x in streams.keys()]
    
    stream = None
    for bitrate in reversed(sorted(bitrates)):
        if stream == None:
            stream = streams[str(bitrate)]
    
    if not options.ffplay == None:
        fstream = ""
        fstream += ' -cookies "'
        for cookie in cookies:
            fstream += cookie
        
        fstream += '" "' + stream.split('|')[0] + '"' 
        command = "ffplay " + fstream
        print command
        os.system(command)