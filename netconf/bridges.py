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
import glob


def probe():
    ifaces = []
    pairs = []
    for brdir in glob.glob('/sys/class/net/*/bridge'):
        brdev = os.path.basename(os.path.dirname(brdir))
        ifaces.append(brdev)
        for brif in os.listdir(os.path.join(
                os.path.dirname(brdir), 'brif')):
            pairs.append((brif, brdev))

    return (ifaces, pairs)
