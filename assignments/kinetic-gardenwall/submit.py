'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 8 Programming Assignment

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

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import os, time

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'sdn1-001'

# the "Identifier" you used when creating the part
partIds = ['agPA81', 'agPA82', 'agPA83']

# used to generate readable run-time information for students
partFriendlyNames = [' Host Gardenwall', 'Pox Gardenwall', 'Pyretic Gardenwall']

# source files to collect (just for our records)
sourceFiles = ['%s/pyretic/pyretic/kinetic/examples/gardenwall.py' % os.environ[ 'HOME' ],
               '%s/pox/pox/misc/gardenwall.py' % os.environ[ 'HOME' ],
               '%s/pyretic/pyretic/examples/gardenwall.py' % os.environ[ 'HOME' ]]


# My network topology
class MyTopo(Topo):
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        self.addLink(h1, s1)
        h2 = self.addHost('h2')
        self.addLink(h2, s1)
        h3 = self.addHost('h3')
        self.addLink(h3, s1)


def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = ''

  if partIdx == 0:
    # Kinetic
    print "a. Firing up Mininet"
    net = Mininet(topo=MyTopo(),
                  controller=lambda name: RemoteController( 'c0', '127.0.0.1' ),
                  host=CPULimitedHost, link=TCLink,
                  autoSetMacs=True, autoStaticArp=True)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    print "b. Starting Test"
    # Start pings
    outputString += h1.cmdPrint('ping', '-c5', '10.0.0.2')

    # Send infect True event
    print "b.1 Sending Infect (True) Event"
    os.system('python json_sender.py -n infected -l True --flow="{srcip=10.0.0.1}" -a 127.0.0.1 -p 50001 &')
    time.sleep(2)
    outputString += h1.cmdPrint('ping', '-c5', '10.0.0.2')
    # Send exempt True event
    print "b.2 Sending Exempt (True) Event"
    os.system('python json_sender.py -n exempt -l True --flow="{srcip=10.0.0.1}" -a 127.0.0.1 -p 50001 &')
    time.sleep(2)
    outputString += h1.cmdPrint('ping', '-c5', '10.0.0.2')

    print "c. Stopping Mininet"
    net.stop()

  if partIdx == 1 or partIdx == 2:
    # Pyretic/POX
    print "a. Firing up Mininet"
    net = Mininet(topo=MyTopo(),
                  controller=lambda name: RemoteController( 'c0', '127.0.0.1' ),
                  host=CPULimitedHost, link=TCLink,
                  autoSetMacs=True, autoStaticArp=True)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    print "b. Starting Test"
    # Start pings
    outputString += h1.cmdPrint('ping', '-c5', '10.0.0.2')

    # Send infect True event
    print "b.1 Sending Infect (True) Event"
    os.system('python json_sender.py -n infected -l True --flow="{srcmac=00:00:00:00:00:01}" -a 127.0.0.1 -p 50001 &')
    time.sleep(2)
    outputString += h1.cmdPrint('ping', '-c5', '10.0.0.2')

    # Send exempt True event
    print "b.2 Sending Exempt (True) Event"
    os.system('python json_sender.py -n exempt -l True --flow="{srcmac=00:00:00:00:00:01}" -a 127.0.0.1 -p 50001 &')
    time.sleep(2)
    outputString += h1.cmdPrint('ping', '-c5', '10.0.0.2')

    print "c. Stopping Mininet"
    net.stop()

  #print outputString
  return outputString.strip()


submit()
#output(2)
