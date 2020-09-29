#!/usr/bin/env python3

import os
import sys
import traceback
from subprocess import Popen, PIPE
DEBUG=True

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
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
        return None

def get_description(with_hash):
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        if with_hash:
            command = ['git', 'describe', '--abbrev=8', '--tags', '--dirty', '--match=*']
        else:
            command = ['git', 'describe', '--abbrev=0', '--tags', '--dirty', '--match=*']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readline().strip()
        #print line
        return line
    except:
        if DEBUG:
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
        return None

def get_revision():
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        command = ['git', 'rev-parse', '--short=8', 'HEAD']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.wait()
        p.stderr.close()
        line = p.stdout.readline().strip()
        p.stdout.close()
        #print line
        return line
    except:
        if DEBUG:
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
        return None

def get_last_tag_rev():
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        #git rev-list --tags --no-walk --max-count=1
        command = ['git', 'rev-list', '--tags', '--no-walk', '--max-count=1']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.wait()
        p.stderr.close()
        line = p.stdout.readline().strip()
        p.stdout.close()
        return line
    except:
        if DEBUG:
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
        return None

def get_revs_since_last_tag():
    #git rev-list  tag..HEAD --count
    rev = get_last_tag_rev()
    if (rev == None):
        return None
    try:
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        #git rev-list --tags --no-walk --max-count=1
        command = ['git', 'rev-list', str(rev)+"..HEAD", '--count']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.wait()
        p.stderr.close()
        line = p.stdout.readline().strip()
        p.stdout.close()
        return line
    except:
        if DEBUG:
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
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
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
        return None

def main():
    out = ""
    b = get_branch().decode("utf-8")
    dirty = ""
    main_branch = "master"
    add_hash = True
    prefix = ""
    working_dir=""
    
    options = {"--main-branch": None, "--no-hash": None, "--prefix": None, "--cd": None, "--is-dirty": None, "--last-tag-rev": None, "--revs-since-last-tag": None}
    parse_options(sys.argv[1:], options)
    if (options["--is-dirty"]!=None):
        if (get_dirty()):
            exit(0)
        else:
            exit(1)

    if (options["--last-tag-rev"]!=None):
        line = get_last_tag_rev().decode('utf-8')
        if (line!=None):
            print(line)
            exit(0)
        else:
            exit(1)

    if (options["--revs-since-last-tag"]!=None):
        line = get_revs_since_last_tag().decode('utf-8')
        if (line!=None):
            print(line)
            exit(0)
        else:
            exit(1)

    if (options["--main-branch"]!=None):
        if(options["--main-branch"] == True):
            print("--main-branch requires string argument")
            exit(-1)
        else:
            main_branch = options["--main-branch"]

    if (options["--no-hash"]!=None):
        if(options["--no-hash"] == True):
            add_hash = False

    desc = get_description(add_hash).decode('utf-8')

    if (options["--prefix"]!=None):
        if(options["--prefix"] == True):
            print("--prefix requires string argument")
            exit(-1)
        else:
            prefix = options["--prefix"]

    if (options["--cd"]!=None):
        if(options["--cd"] == True):
            print("--cd requires string argument")
            exit(-1)
        else:
            working_dir = options["--cd"]

    cwd = os.getcwd();
    if working_dir!="":
        if os.path.isdir(working_dir):
            os.chdir(working_dir)
        else:
            exit(-2)

    if (get_dirty()):
        dirty="-dirty"

    if (b == None):
        out = 'norev'
    elif ((b != main_branch) or (len(desc) == 0)):
        if add_hash:
            out = b+"-"+get_revision().decode("utf-8")+dirty
        else:
            out = b+dirty
    else:
        out = desc
    if prefix!="":
        out=prefix+"-"+out
    return out

if __name__=="__main__":
    print(main())
