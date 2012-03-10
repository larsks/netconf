import os
import threading
from glob import glob

def probe_lldp(probe):
	try:
		p = sniff(iface=iface, filter='ether proto 0x88cc',
			count=1, timeout=60)
		probe['raw'] = p
		probe['lldp'] = tlv.LLDPDU(p[0].load)
		probe['status'] = True
	except Exception, detail:
		probe['status'] = False
		probe['exception'] = detail

def probe():
    ifaces = []
    pairs = []
    probes = {}

    for ifdir in glob('/sys/class/net/*/device'):
        iface = os.path.basename(os.path.dirname(ifdir))
        ifaces.append(iface)

        probes[iface] = {}

        t = threading.Thread(
                target=probe_lldp,
                name=iface,
                args=(probes[iface]),
                )

        probes[iface]['thread'] = t
        t.start()

    for iface,probe in probes.items():
        thread = probe['thread']

        if thread is not threading.currentThread():
            thread.join()
            pairs.append((iface, probe['lldp']['port_id'][0][1:]))

    return (ifaces, pairs)
 
