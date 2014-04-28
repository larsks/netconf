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
