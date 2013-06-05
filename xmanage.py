#!/usr/bin/python
#
# simple script for managing mitx / edx instance via vagrant
#
# usage examples:
#
# vagrant ssh -- xmanage restart-lms
# vagrant ssh -- xmanage restart-cms

import os, sys, string, re
import subprocess

def usage():
    print "Welcome to the MITx / edX instance management tool"
    print
    print "Commands available:"
    print
    print "restart-lms    - restart the LMS (for vagrant boxes, running at http://192.168.42.2)"
    print "                 This will force re-loading of course data"
    print
    print "restart-cms    - restart the CMS (aka the Studio system)"
    print
    print "update         - update this management script (from central repo)"

if len(sys.argv)<2:
    usage()

avcnt = 1
cmd = sys.argv[avcnt]
avcnt += 1

ROOT = "/home/vagrant/mitx_all"
DIST = "mitx"

def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])
        
def do_cmd(cmd):
    os.chdir(ROOT)
    #os.system('source STARTUP; cd %s; %s' % (DIST, cmd))
    bash_command('source STARTUP; cd %s; %s' % (DIST, cmd))

if cmd=='restart-lms':
    do_cmd('./RESTART-GUNICORN')

elif cmd=='restart-cms':
    do_cmd('./RESTART-GUNICORN-CMS')

elif cmd=='update':
    bash_command('cd mitx_all/xmanage; git pull; chmod +x xmanage/*.py')

elif cmd=='help':
    usage()

else:
    print "Unknown command %s" % cmd
    print
    usage()
    


