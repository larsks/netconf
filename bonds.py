import os
import glob
import errno

def probe():
	ifaces = []
	pairs = []
    try:
        for iface in open('/sys/class/net/bonding_masters').read().split():
            ifaces.append(iface)
            for line in open('/sys/class/net/%s/bonding/slaves' % iface).read().split():
                pairs.append((iface, line.strip()))
    except IOError, detail:
        if detail.errno != errno.ENOENT:
            raise

	return (ifaces, pairs)

