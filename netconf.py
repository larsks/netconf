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

def discover():
    pairs = []

    for x in [ physdevs, bonds, bridges, vlans ]:
        pairs.extend(x.probe()[1])

    return pairs

def render(pairs):
    print 'digraph net {'
    print 'graph [rank=LR]'
    print
    for a,b in pairs:
        print '"%s" -> "%s"' % (a,b)
    print '}'

render(discover())

