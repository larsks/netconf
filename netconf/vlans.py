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
