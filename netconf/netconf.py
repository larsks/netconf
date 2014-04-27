#!/usr/bin/python

import os
import sys
import threading

import bonds
import bridges
import vlans
import physdevs

# This defines attributes used when generating the
# dot output.
attrs = {
        # default attributes that will be applied to all interface
        # types unless overridden by a more specific setting.
        '__default__': {
            'subgraph': {
                'rank' : 'same',
                },
            'node': {
                'style' : 'filled',
                },
            },

        'ports': {
            'node': {
                'shape' : 'box',
                },
            },
        'physdevs': {
            'node': {
                'color' : 'firebrick1',
                },
            },
        'bonds': {
            'node': {
                'color' : 'darkgoldenrod1',
                },
            },
        'bridges': {
            'subgraph': {
                'rank' : 'min',
                },
            'node': {
                'color' : 'cornflowerblue',
                },
            },
        'vlans': {
            'node': {
                'color' : 'darkolivegreen2',
                },
            },
        }

def discover():
    data = {}

    for x in [ physdevs, bonds, bridges, vlans ]:
        ifaces, pairs = x.probe()
        iftype = x.__name__.split('.')[-1]

        data[iftype] = (ifaces, pairs)
        if iftype == 'physdevs':
            data['ports'] = ([x[1] for x in pairs], [])

    return data

def render(data):
    '''render() generates the dot output.'''

    print 'digraph net {'
    print '  rankdir=LR;'
    print

    for iftype in [ 'ports', 'physdevs', 'bonds', 'bridges', 'vlans' ]:

        subgraph_attrs = {}
        subgraph_attrs.update(attrs['__default__']['subgraph'])
        subgraph_attrs.update(attrs[iftype].get('subgraph', {}))

        node_attrs = {}
        node_attrs.update(attrs['__default__']['node'])
        node_attrs.update(attrs[iftype].get('node', {}))

        print
        print '  /* %s */' % iftype
        print '  subgraph {'

        for k,v in subgraph_attrs.items():
            print '    %s=%s ;' % (k,v)

        print '    node [%s] ;' % (', '.join(
            ['%s=%s' % (n,v) for n,v in node_attrs.items()]))
        print
        for iface in data[iftype][0]:
            print '    "%s" ;' % iface

        print '  }'

    print
    for iftype in [ 'ports', 'physdevs', 'bonds', 'bridges', 'vlans' ]:
        for k,v in data[iftype][1]:
            print '  "%s" -> "%s" ;' % (k,v)

    print '}'

def main():
    render(discover())

if __name__ == '__main__':
    main()
# The following can be used when testing the rendering code:
#    render({
#        'ports': [['eth104/1/48', 'eth104/1/46'],[]],
#        'physdevs': [['em1', 'em2'],[('em1', 'eth104/1/48'), ('em2',
#            'eth104/1/46')]],
#        'bonds': [[],[]],
#        'bridges': [[],[]],
#        'vlans': [[],[]],
#        })
#
