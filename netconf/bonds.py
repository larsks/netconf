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
