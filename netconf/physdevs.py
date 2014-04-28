# Copyright (C) 2014 Lars Kellogg-Stedman <lars@oddbit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import threading
from glob import glob

from scapy.all import sniff
import lldp


def probe_lldp(iface, probe):
    try:
        p = sniff(iface=iface,
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

    for iface, probe in probes.items():
        thread = probe['thread']

        if thread is not threading.currentThread():
            thread.join()
            if 'lldp' in probe:
                pairs.append((iface, probe['lldp']['port_id'][1:]))

    return (ifaces, pairs)
