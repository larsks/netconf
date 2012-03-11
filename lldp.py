# Support for LLDP (link layer discovery protocol):
# https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol

import struct

LLDP_ETHER_TYPE = 0x88cc
LLDP_TYPE_MASK = 0xfe00
LLDP_LENGTH_LEN = 9
LLDP_LENGTH_MASK = 0x01ff

LLDP_TYPES = {
    0   : 'end_lldpdu',
    1   : 'chassis_id',
    2   : 'port_id',
    3   : 'ttl',
    4   : 'port_description',
    5   : 'system_name',
    6   : 'system_description',
    7   : 'system_capabilities',
    8   : 'management_address',
    127 : 'org_tlv',
    }

class LLDPDU (dict):
    '''Parse the TLV (type-length-value) fields in an LLDP data unit.'''

    def __init__(self, data):
        self.data = data

        while True:
            # The first 16 bits contain the type (7 bits) and
            # length (9 bits) of the value.
            tl = struct.unpack('!H', data[:2])[0]
            data = data[2:]

            tltype = (tl & LLDP_TYPE_MASK) >> LLDP_LENGTH_LEN
            tllen = (tl & LLDP_LENGTH_MASK)

            tlvalue = data[:tllen]
            data = data[tllen:]

            # Right now everything is a list, but this is realy
            # just an artifact of how we're treating organization
            # tlvs.
            if not LLDP_TYPES[tltype] in self:
                self[LLDP_TYPES[tltype]] = []
            self[LLDP_TYPES[tltype]].append(tlvalue)

            # Exit when we have consumed everything.
            if not data: break

if __name__ == '__main__':
    import sys
    t = LLDPDU(open(sys.argv[1]).read())

