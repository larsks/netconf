import os
import glob

def probe():
	ifaces = []
	pairs = []
	for vlan in os.listdir('/proc/net/vlan'):
		if vlan == 'config':
			continue

		ifaces.append(vlan)
		for line in open('/proc/net/vlan/%s' % vlan):
			if line.startswith('Device:'):
				pairs.append((vlan, line.split()[1]))
	
	return (ifaces, pairs)

