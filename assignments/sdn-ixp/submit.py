'''
    Coursera:
    - Software Defined Networking (SDN) course
    -- Module 7 Programming Assignment

    Professor: Nick Feamster
    Teaching Assistant: Arpit Gupta


'''


### The only things you'll have to edit (unless you're porting this script over to a different language)
### are at the bottom of this file.

import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys

""""""""""""""""""""
""""""""""""""""""""

class NullDevice:
    def write(self, s):
        pass

def submit():
    print '==\n== [sandbox] Submitting Solutions \n=='

    (login, password) = loginPrompt()
    if not login:
        print '!! Submission Cancelled'
        return

    print '\n== Connecting to Coursera ... '

    # Part Identifier
    (partIdx, sid) = partPrompt()

    # Get Challenge
    (login, ch, state, ch_aux) = getChallenge(login, sid) #sid is the "part identifier"
    if((not login) or (not ch) or (not state)):
        # Some error occured, error string in first return element.
        print '\n!! Error: %s\n' % login
        return

    # Attempt Submission with Challenge
    ch_resp = challengeResponse(login, password, ch)
    (result, string) = submitSolution(login, ch_resp, sid, output(partIdx), \
                                      source(partIdx), state, ch_aux)

    print '== %s' % string.strip()


# =========================== LOGIN HELPERS - NO NEED TO CONFIGURE THIS =======================================

def loginPrompt():
    """Prompt the user for login credentials. Returns a tuple (login, password)."""
    (login, password) = basicPrompt()
    return login, password


def basicPrompt():
    """Prompt the user for login credentials. Returns a tuple (login, password)."""
    login = raw_input('Login (Email address): ')
    password = raw_input('One-time Password (from the assignment page. This is NOT your own account\'s password): ')
    return login, password

def partPrompt():
    print 'Hello! These are the assignment parts that you can submit:'
    counter = 0
    for part in partFriendlyNames:
        counter += 1
        print str(counter) + ') ' + partFriendlyNames[counter - 1]
    partIdx = int(raw_input('Please enter which part you want to submit (1-' + str(counter) + '): ')) - 1
    return (partIdx, partIds[partIdx])

def getChallenge(email, sid):
    """Gets the challenge salt from the server. Returns (email,ch,state,ch_aux)."""
    url = challenge_url()
    values = {'email_address' : email, 'assignment_part_sid' : sid, 'response_encoding' : 'delim'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    text = response.read().strip()

    # text is of the form email|ch|signature
    splits = text.split('|')
    if(len(splits) != 9):
        print 'Badly formatted challenge response: %s' % text
        return None
    return (splits[2], splits[4], splits[6], splits[8])

def challengeResponse(email, passwd, challenge):
    sha1 = hashlib.sha1()
    sha1.update("".join([challenge, passwd])) # hash the first elements
    digest = sha1.hexdigest()
    strAnswer = ''
    for i in range(0, len(digest)):
        strAnswer = strAnswer + digest[i]
    return strAnswer

def challenge_url():
    """Returns the challenge url."""
    return "https://class.coursera.org/" + URL + "/assignment/challenge"

def submit_url():
    """Returns the submission url."""
    return "https://class.coursera.org/" + URL + "/assignment/submit"

def submitSolution(email_address, ch_resp, sid, output, source, state, ch_aux):
    """Submits a solution to the server. Returns (result, string)."""
    source_64_msg = email.message.Message()
    source_64_msg.set_payload(source)
    email.encoders.encode_base64(source_64_msg)

    output_64_msg = email.message.Message()
    output_64_msg.set_payload(output)
    email.encoders.encode_base64(output_64_msg)
    values = { 'assignment_part_sid' : sid, \
        'email_address' : email_address, \
        'submission' : output_64_msg.get_payload(), \
        'submission_aux' : source_64_msg.get_payload(), \
        'challenge_response' : ch_resp, \
        'state' : state \
        }
    url = submit_url()
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    string = response.read().strip()

    result = 0
    return result, string

## This collects the source code (just for logging purposes)
def source(partIdx):
    # open the file, get all lines
    f = open(sourceFiles[partIdx])
    src = f.read()
    f.close()
    return src


############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############


import os, time
from sdx_mininext import *


# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'sdn1-001'

# the "Identifier" you used when creating the part
partIds = ['agPA7']
# used to generate readable run-time information for students
partFriendlyNames = ['Confgiure topology and policies for SDX']
# source files to collect (just for our records)
sourceFiles = ['%s/sdx-ryu/examples/simple/mininet/sdx_mininext.py' % os.environ[ 'HOME' ],
               '%s/sdx-ryu/examples/simple/mininet/configs/a1/bgpd.conf' % os.environ[ 'HOME' ],
               '%s/sdx-ryu/examples/simple/mininet/configs/b1/bgpd.conf' % os.environ[ 'HOME' ],
               '%s/sdx-ryu/examples/simple/mininet/configs/c1/bgpd.conf' % os.environ[ 'HOME' ],
               '%s/sdx-ryu/examples/simple/controller/participant_policies/participant_1.py' % os.environ[ 'HOME' ],
               '%s/sdx-ryu/examples/simple/controller/participant_policies/participant_2.py' % os.environ[ 'HOME' ],
               '%s/sdx-ryu/examples/simple/controller/participant_policies/participant_3.py' % os.environ[ 'HOME' ]]


'Set the OF Protocol for SDXs switch'
cmd_ovs = 'sudo ovs-vsctl set bridge s1 protocols=OpenFlow13'

'Start the Ryu based SDX controller'
cmd_ryu = 'ryu-manager ~/sdx-ryu/ctrl/asdx.py --asdx-dir simple > /dev/null 2>&1&'

'Start the Route Server'
cmd_xrs = 'cd ~/sdx-ryu/xrs ; sudo ./route_server.py simple > /dev/null 2>&1 &'

'Start the exabgp module'
cmd_exabgp = 'sudo su - vagrant -c "exabgp ~/sdx-ryu/examples/simple/controller/sdx_config/bgp.conf > /dev/null 2>&1 &"'

def output(partIdx):
    outputString = ''
    if partIdx == 0:

    	f = open('output.log', 'w')

    	'Create Topology'
    	topo = QuaggaTopo()
    	net = Mininext(topo=topo,
    		controller=lambda name: RemoteController( name, ip='127.0.0.1' ))

    	'Start the network'
    	net.start()
    	addInterfacesForSDXNetwork(net)

    	'Set OF protocol'
    	os.system(cmd_ovs)

    	'Start various modules'
    	os.system(cmd_ryu)
    	os.system(cmd_xrs)
    	os.system(cmd_exabgp)

    	a1 = net.get('a1')
    	b1 = net.get('b1')
    	c1 = net.get('c1')
    	c2 = net.get('c2')

    	'Wait for all the route exchanges'
    	while True:
    		routingDump = a1.cmdPrint('route -n')
            	n_routes = len(routingDump.split('a1-eth0'))-1
    		# Make sure that your routing table has 7 entries
    		if n_routes == 7:
    			outputString += routingDump
    			break
    		else:
    			time.sleep(2)
    	print "Routes exchanged."

    	print "Staring Iperf Server ..."
    	b1.cmdPrint('iperf -s -B 140.0.0.1 -p 80 &')
    	c2.cmdPrint('iperf -s -B 180.0.0.1 -p 80 &')

    	'Wait for some time ...'
    	time.sleep(5)

    	print "Starting Iperf Client ..."
    	outputString += a1.cmd('iperf -c 140.0.0.1 -B 100.0.0.1 -p 80 -t 2')
    	outputString += a1.cmd('iperf -c 180.0.0.1 -B 100.0.0.2 -p 80 -t 2')

    	print " Completed Iperf Experiment."
    	net.stop()
    	print "---Test Completed---"
    	print outputString
    	f.write(outputString)
    	f.close()

    return outputString.strip()

#output(0)
submit()
