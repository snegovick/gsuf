#!/usr/bin/env python

import sys
import traceback
from subprocess import Popen, PIPE
DEBUG=False

def parse_options(argv, expected_options):
    #print "parsing options"
    opt = None
    for o in argv:
        #print o
        if o[0] == "-":
            if o in expected_options:
                opt = o
                expected_options[opt] = True
        elif opt:
            expected_options[opt] = o
            opt = None

def get_branch():
    try:
        # Work around an apparent bug in git:
        # http://comments.gmane.org/gmane.comp.version-control.git/178169
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()
        
        command = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readline().strip()
        #print line
        return line
    except:
        if DEBUG:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        return None

def get_description():
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        command = ['git', 'describe', '--abbrev=8', '--tags', '--dirty', '--match=*']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readline().strip()
        #print line
        return line
    except:
        if DEBUG:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        return None

def get_revision():
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        command = ['git', 'rev-parse', '--short=8', 'HEAD']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readline().strip()
        #print line
        return line
    except:
        if DEBUG:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        return None

def get_dirty():
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        command = ['git', 'diff-index', '--quiet', 'HEAD']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.wait()
        p.stderr.close()
        p.stdout.close()
        if p.returncode != 0:
            return True
        return False
    except:
        if DEBUG:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        return None

def main():
    out = ""
    b = get_branch()
    desc = get_description()
    dirty = ""
    if (get_dirty()):
        dirty="-dirty"
    if (b == None):
        out = 'norev'
    elif ((b != 'staging') or (len(desc) == 0)):
        out = b+"-"+get_revision()+dirty
    else:
        out = desc
    return out

if __name__=="__main__":
    print main()
