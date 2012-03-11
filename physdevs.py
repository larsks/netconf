import os
import threading
from glob import glob

from scapy.all import sniff
import lldp

def probe_lldp(iface, probe):
    try:
        p = sniff(iface=iface],
                filter='ether proto %s' % lldp.LLDP_ETHER_TYPE,
                count=1, timeout=60)
        probe['lldp'] = lldp.LLDPDU(p[0].load)
        probe['status'] = True
    except Exception, detail:
        probe['status'] = False
        probe['exception'] = detail

def probe():
    '''Listens on all physical interfaces in parallel for LLDPDUs.  Starts
    a new thread for each interface, then waits for everything to complete
    (or timeout).'''

    ifaces = []
    pairs = []
    probes = {}

    for ifdir in glob('/sys/class/net/*/device'):
        iface = os.path.basename(os.path.dirname(ifdir))
        ifaces.append(iface)

        probes[iface] = {'iface': iface}

        t = threading.Thread(
                target=probe_lldp,
                name=iface,
                args=(iface, probes[iface],),
                )

        probes[iface]['thread'] = t
        t.start()

    for iface,probe in probes.items():
        thread = probe['thread']

        if thread is not threading.currentThread():
            thread.join()
            if 'lldp' in probe:
                pairs.append((iface, probe['lldp']['port_id'][0][1:]))

    return (ifaces, pairs)
 
