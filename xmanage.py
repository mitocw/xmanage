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
    print "restart-lms     - restart the LMS (for vagrant boxes, running at http://192.168.42.2)"
    print "                  This will force re-loading of course data"
    print "restart-cms     - restart the CMS (aka the Studio system)"
    print "restart-edge    - restart the Edge server (part of the Studio system)"
    print "restart-preview - restart the Preview server (part of the Studio system)"
    print
    print "activate <user> - activate user specified by username <user>"
    print
    print "update          - update this management script (from central repo)"
    print "help            - print out this message, as well as local NOTES.txt file"

if len(sys.argv)<2:
    usage()

avcnt = 1
cmd = sys.argv[avcnt]
avcnt += 1

ROOT = "/home/vagrant/mitx_all"
DIST = "mitx"

def bash_command(cmd):
    sp = subprocess.Popen(['/bin/bash', '-c', cmd])
    sp.wait()
        
def do_cmd(cmd):
    os.chdir(ROOT)
    #os.system('source STARTUP; cd %s; %s' % (DIST, cmd))
    bash_command('source STARTUP; cd %s; %s' % (DIST, cmd))

if cmd=='restart-lms':
    do_cmd('./RESTART-GUNICORN')

elif cmd=='restart-cms':
    do_cmd('./RESTART-GUNICORN-CMS')

elif cmd=='restart-edge':
    do_cmd('./RESTART-GUNICORN-EDGE')

elif cmd=='restart-preview':
    do_cmd('./RESTART-GUNICORN-preview')

elif cmd=='activate':
    uname = sys.argv[avcnt]
    print "activating user %s" % uname
    do_cmd('./DJANGO-ADMIN activate_user %s' % uname)

elif cmd=='update':
    bash_command('cd mitx_all/xmanage; git pull; chmod +x *.py')

elif cmd=='help':
    usage()
    NOTES = "NOTES.txt"
    if os.path.exists(NOTES):
        print "----------------------------------------"
        print "Notes file:"
        print open(NOTES).read()

else:
    print "Unknown command %s" % cmd
    print
    usage()
    


