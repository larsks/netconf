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

import errno


def probe():
    ifaces = []
    pairs = []
    try:
        for iface in open('/sys/class/net/bonding_masters').read().split():
            ifaces.append(iface)
            for line in open(
                    '/sys/class/net/%s/bonding/slaves' % iface
            ).read().split():
                pairs.append((iface, line.strip()))
    except IOError, detail:
        if detail.errno != errno.ENOENT:
            raise

    return (ifaces, pairs)
