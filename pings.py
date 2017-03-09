##
##  pings - capture HexChat highlighted messages for review
##  Copyright (C) 2017 David McMackins II
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU Affero General Public License as published by
##  the Free Software Foundation, version 3 only.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU Affero General Public License for more details.
##
##  You should have received a copy of the GNU Affero General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

__module_name__ = 'pings'
__module_version__ = '0.0'
__module_description__ = 'Highlighted message tracker'
__module_author__ = 'David McMackins II'

import hexchat

def convert_timestamp(stamp):
    raise NotImplemented()

def pings(word, word_eol, userdata):
    if len(word) < 2:
        time = None
    else:
        time = convert_timestamp(word_eol[1]))

    return hexchat.EAT_ALL

def unload(userdata):
    hexchat.prnt('{} unloaded'.format(__module_name__))

def init():
    hexchat.hook_command('pings', pings,
                         help='Usage: PINGS <time>, lists pings since time specified')
    hexchat.hook_unload(unload)
    hexchat.prnt('Loaded {} {}'.format(__module_name__, __module_version__))

init()
