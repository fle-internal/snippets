#!/bin/env python
import os
import subprocess
import sys

def git(*command):
    try:
        subprocess.call(['git'] + list(command))
    except OSError as e:
        if e.errno == os.errno.ENOENT: # git binary does not exist
            print 'The git binary does not exist. Install that first.'
            sys.exit(1)
        else:
            raise

def clone_repo(repo_name, username):
    print 'Cloning %s onto the current directory' % repo_name

    repo_url = 'git@github.com:%s/%s.git' % (username, repo_name)
    print 'Cloning %s' % repo_url
    git('clone', repo_url)
    print 'Great success cloning %s repo' % repo_name

def setup_repo(kalite_dir):
    print 'Setting up the repo in %s' % kalite_dir

    managepy = os.path.join(kalite_dir, 'manage.py')

    subprocess.call(['python', managepy, 'setup', '--username=admin', '--password=pass', '--noinput'])

    print 'Great success setting up %s' % kalite_dir

def setup_localsettings(kalite_dir):
    with open(os.path.join(kalite_dir, "local_settings.py"), "w") as fp:
        fp.write("DEBUG = True\n")
        fp.write("CENTRAL_SERVER_HOST = '127.0.0.1:8000'\n")
        fp.write("SECURESYNC_PROTOCOL = 'http'\n")

if __name__ == '__main__':
    print "I'm assuming you've already forked the learningequality/ka-lite repo on GitHub"
    username = raw_input('What is your github username?')

    clone_repo('ka-lite', username)
    os.chdir('ka-lite')
    git('remote', 'add', 'upstream', 'git@github.com:learningequality/ka-lite.git')
    git('remote', 'add', 'bcipolli', 'git@github.com:bcipolli/ka-lite.git')
    git('remote', 'add', 'aronasorman', 'git@github.com:aronasorman/ka-lite.git')
    git('checkout', 'develop')
    setup_repo('kalite')
    setup_localsettings('kalite')
