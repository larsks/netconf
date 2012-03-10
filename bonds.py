import os
import glob

def probe():
	ifaces = []
	pairs = []
	for iface in open('/sys/class/net/bonding_masters').read().split():
		ifaces.append(iface)
		for line in open('/sys/class/net/%s/bonding/slaves' % iface).read().split():
			pairs.append((iface, line.strip()))

	return (ifaces, pairs)

