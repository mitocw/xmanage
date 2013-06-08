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
    print "restart-lms      - restart the LMS (for vagrant boxes, running at http://192.168.42.2)"
    print "                   This will force re-loading of course data"
    print "restart-cms      - restart the CMS (aka the Studio system)"
    print "restart-edge     - restart the Edge server (part of the Studio system)"
    print "restart-preview  - restart the Preview server (part of the Studio system)"
    print
    print "restart-xqueue   - restart the xqueue main system"
    print "restart-consumer - restart the xqueue consumer"
    print "restart-xserver  - restart the xserver (python code grader)"
    print
    print "logs <appname>   - view last 100 lines of log file for <appname>"
    print "                   appname should be one of lms, cms, edge, preview, xserver, xqueue"
    print
    print "activate <user>  - activate user specified by username <user>"
    print "setstaff <user>  - make user (specified by username <user>) into staff"
    print
    print "update-mitx      - update mitx system code (use with care!)"
    print "update           - update this management script (from central repo)"
    print "help             - print out this message, as well as local NOTES.txt file"

if len(sys.argv)<2:
    usage()

avcnt = 1
cmd = sys.argv[avcnt]
avcnt += 1

HOME = "/home/vagrant"

appinfo = {'lms': dict(dir='edx-platform', log='LOG.gunicorn'),
           'cms': dict(dir='edx-platform', log='LOG.gunicorn.cms'),
           'edge': dict(dir='edx-platform', log='LOG.gunicorn.edge'),
           'preview': dict(dir='edx-platform', log='LOG.gunicorn.preview'),
           'xserver': dict(dir='xserver', log='LOG.gunicorn'),
           'consumer': dict(dir='xqueue', log='LOG.consumer'),
           'xqueue': dict(dir='xqueue', log='LOG.gunicorn'),
           }

if os.path.exists("%s/mitx_all" % HOME):
    ROOT = HOME + "/mitx_all"
    DIST = "mitx"

elif os.path.exists("%s/edx_all" % HOME):
    ROOT = HOME + "/edx_all"
    DIST = "edx-platform"

def bash_command(cmd):
    sp = subprocess.Popen(['/bin/bash', '-c', cmd])
    sp.wait()
        
def do_cmd(cmd, ddir=DIST):
    os.chdir(ROOT)
    #os.system('source STARTUP; cd %s; %s' % (DIST, cmd))
    bash_command('source STARTUP; cd %s; %s' % (ddir, cmd))

if cmd=='restart-lms':
    do_cmd('./RESTART-GUNICORN')

elif cmd=='restart-cms':
    do_cmd('./RESTART-GUNICORN-CMS')

elif cmd=='restart-edge':
    do_cmd('./RESTART-GUNICORN-EDGE')

elif cmd=='restart-preview':
    do_cmd('./RESTART-GUNICORN-preview')

elif cmd=='restart-consumer':
    do_cmd('./RESTART-CONSUMER', ddir="xqueue")

elif cmd=='restart-xqueue':
    do_cmd('./RESTART-GUNICORN', ddir="xqueue")

elif cmd=='restart-xserver':
    do_cmd('./RESTART-GUNICORN', ddir="xserver")

elif cmd=='activate':
    uname = sys.argv[avcnt]
    print "activating user %s" % uname
    do_cmd('./DJANGO-ADMIN activate_user %s' % uname)
    print "To complete the activation, please logout then log back in"

elif cmd=='setstaff':
    uname = sys.argv[avcnt]
    print "making user %s staff" % uname
    do_cmd('./DJANGO-ADMIN set_staff %s' % uname)
    print "To complete conversion to staff, please logout then log back in"

elif cmd=='logs':
    app = sys.argv[avcnt]
    avcnt += 1
    opts = "-100"
    if len(sys.argv)>=avcnt:
        opts = ' '.join(sys.argv[avcnt:])
    if not app in appinfo:
        print "unknown appname %s" % app
        print "known apps: " % appinfo.keys()
        usage()
    else:
        ai = appinfo[app]
        bash_command('cd %s/%s; tail %s %s' % (ROOT, ai['dir'], opts, ai['log']))

elif cmd=='update-mitx':
    bash_command('cd %s/%s; git pull' % (ROOT, DIST))

elif cmd=='update':
    bash_command('cd %s/xmanage; git pull; chmod +x *.py' % ROOT)

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
    


