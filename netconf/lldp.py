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

# Support for LLDP (link layer discovery protocol):
# https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol

import struct

LLDP_ETHER_TYPE                   = 0x88cc
LLDP_TYPE_MASK                    = 0xfe00
LLDP_LENGTH_LEN                   = 9
LLDP_LENGTH_MASK                  = 0x01ff

LLDP_TLV_TYPE_END                 = 0
LLDP_TLV_TYPE_CHASSIS_ID          = 1
LLDP_TLV_TYPE_PORT_ID             = 2
LLDP_TLV_TYPE_TTL                 = 3
LLDP_TLV_TYPE_PORT_DESCRIPTION    = 4
LLDP_TLV_TYPE_SYSTEM_NAME         = 5
LLDP_TLV_TYPE_SYSTEM_DESCRIPTION  = 6
LLDP_TLV_TYPE_SYSTEM_CAPABILITIES = 7
LLDP_TLV_TYPE_MANAGEMENT_ADDRESS  = 8
LLDP_TLV_TYPE_ORG                 = 127

LLDP_TLV_TYPES = {
    LLDP_TLV_TYPE_END                 : 'end',
    LLDP_TLV_TYPE_CHASSIS_ID          : 'chassis_id',
    LLDP_TLV_TYPE_PORT_ID             : 'port_id',
    LLDP_TLV_TYPE_TTL                 : 'ttl',
    LLDP_TLV_TYPE_PORT_DESCRIPTION    : 'port_description',
    LLDP_TLV_TYPE_SYSTEM_NAME         : 'system_name',
    LLDP_TLV_TYPE_SYSTEM_DESCRIPTION  : 'system_description',
    LLDP_TLV_TYPE_SYSTEM_CAPABILITIES : 'system_capabilities',
    LLDP_TLV_TYPE_MANAGEMENT_ADDRESS  : 'management_address',

    LLDP_TLV_TYPE_ORG                 : 'org_tlv',
}


def parse_tlv(buffer):
    '''Turn a buffer containing TLV data into an iterator over the
    TLV fields.'''

    while buffer:
        tlvhdr = struct.unpack('!H', buffer[:2])[0]

        tlvtype = (tlvhdr & LLDP_TYPE_MASK) >> LLDP_LENGTH_LEN
        tlvlen = (tlvhdr & LLDP_LENGTH_MASK)
        tlvdata = buffer[2:tlvlen+2]
        buffer = buffer[tlvlen+2:]

        yield(tlvtype, tlvdata)


class LLDPDU (dict):
    '''Parse the TLV (type-length-value) fields in an LLDP data unit.'''

    def __init__(self, data):
        self.data = data

        for tlv in parse_tlv(data):
            if tlv[0] == LLDP_TLV_TYPE_ORG:
                if 'org_tlv' not in self:
                    self['org_tlv'] = []
                self['org_tlv'].append(tlv[1])
            else:
                self[LLDP_TLV_TYPES[tlv[0]]] = tlv[1]

            # Exit when we have consumed everything.
            if not data:
                break

if __name__ == '__main__':
    import binascii

    b = binascii.a2b_hex(open('pdu').read().strip())
    t = parse_tlv(b)

