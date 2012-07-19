#!/usr/bin/env python

import sys

from admin import (Account, Component,
                   HAproxyProcess8000, NginxProcess, PostgreSQLProcess, Memcached, Backend, Worker,
                   whoami)

####################
# A configuration
####################

# define two important local accounts
local_user = Account(username=whoami, hostname='localhost')

log_database = "postgresql://localhost:5432/sagews"

postgresql = Component('postgreSQL', [PostgreSQLProcess(local_user, 0, log_database=log_database)])
nginx      = Component('nginx', [NginxProcess(local_user, 0, log_database=log_database)])
haproxy    = Component('haproxy', [HAproxyProcess8000(local_user, 0, log_database=log_database)])
memcached  = Component('memcached', [Memcached(local_user, 0, log_database=log_database)])
backend    = Component('backend', [Backend(local_user, 0, 5000, log_database=log_database)])
worker     = Component('worker', [Worker(local_user, 0, 6000, log_database=log_database)])

all = {'postgresql':postgresql, 'nginx':nginx, 'haproxy':haproxy,
       'memcached':memcached, 'backend':backend, 'worker':worker}

ALL = ','.join(all.keys())

def action(c, what):
    print '%s %s:'%(what, c)
    c = c.strip()
    if not c: return
    if c not in all:
        print "no component '%s'"%c
        sys.exit(1)
    print ' '*10 + str(getattr(all[c], what)())

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Launch a simple testing sagews setup, where everything runs locally on one server as the same user.")

    parser.add_argument("--start", dest='start', type=str, default='',
                        help="start comma separated list of components (or 'all'='%s')"%ALL)

    parser.add_argument("--stop", dest='stop', type=str, default='', help="stop given components")
    
    parser.add_argument("--status", dest='status', type=str, default='', help="status of given components")

    parser.add_argument("--restart", dest='restart', type=str, default='', help="restart given components")
    
    args = parser.parse_args()

    if args.start == 'all':
        args.start = ALL
    if args.stop == 'all':
        args.stop = ALL
    if args.status == 'all':
        args.status = ALL
    if args.restart == 'all':
        args.restart = ALL
        
    for c in args.start.split(','):
        action(c, 'start')
    for c in args.stop.split(','):
        action(c, 'stop')
    for c in args.status.split(','):
        action(c, 'status')
    for c in args.restart.split(','):
        action(c, 'restart')
    
        
