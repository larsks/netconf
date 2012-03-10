#!/usr/bin/python

import os
import sys
import threading

from scapy.all import *

import lldp

import bonds
import bridges
import vlans
import physdevs

attrs = {
        'physdevs'  : {'color':'firebrick1'},
        'bonds'     : {'color':'darkgoldenrod1'},
        'bridges'   : {'color':'cornflowerblue'},
        'vlans'     : {'color':'darkolivegreen2'},
        }

def discover():
    ifaces = {}
    pairs = []

    for x in [ physdevs, bonds, bridges, vlans ]:
        res = x.probe()

        ifaces[x.__name__] = res[0]
        pairs.extend(res[1])

    return (ifaces, pairs)

def render(ifaces, pairs):
    print 'digraph net {'
    print 'graph [rankdir=LR]'
    print
    for iftype,ifaces in ifaces.items():
        nodeattr = ' '.join(['%s=%s' % (n,v) for n,v in attrs[iftype].items()])
        for iface in ifaces:
            print '"%s" [%s]' % (iface, nodeattr)

    for a,b in pairs:
        print '"%s" -> "%s"' % (a,b)
    print '}'

render(*discover())

