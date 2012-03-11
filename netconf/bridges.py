import os
import glob

def probe():
	ifaces = []
	pairs = []
	for brdir in glob.glob('/sys/class/net/*/bridge'):
		brdev=os.path.basename(os.path.dirname(brdir))
		ifaces.append(brdev)
		for brif in os.listdir(os.path.join(
			os.path.dirname(brdir), 'brif')):
			pairs.append((brif, brdev))

	return (ifaces, pairs)

