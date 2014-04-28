# Copyright 2014 Lars Kellogg-Stedman <lars@oddbit.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

