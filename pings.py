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
from datetime import datetime

class Ping:
    def __init__(self, time, user, message):
        self.time = time
        self.user = user
        self.message = message

    def __str__(self):
        timestamp = '[{0:%m-%d %H:%M:%S}]'.format(self.time)
        return ' '.join([timestamp, self.user + ':', self.message])

PINGS = []

def convert_timestamp(stamp):
    now = datetime.now()
    date = ['1','1']
    time = ['0', '0', '0']
    stamp = stamp.split(' ')
    if len(stamp) == 1:
        if '-' in stamp[0]:
            date = stamp[0].split('-')
            if len(date) != 2:
                hexchat.prnt('Date must be formatted MM-DD')
                raise Exception()
        elif ':' in stamp[0]:
            date = [now.month, now.day]
            stamp = stamp[0].split(':')
            try:
                for i in range(len(stamp)):
                    time[i] = stamp[i]
            except IndexError:
                hexchat.prnt('Time must be formatted hh:mm[:ss]')
                raise Exception()
        else:
            hexchat.prnt('Must enter a date and/or time')
            raise Exception()
    elif len(stamp) == 2:
        date = stamp[0].split('-')
        if len(date) != 2:
            hexchat.prnt('Date must be formatted MM-DD')
            raise Exception()

        stamp = stamp[1].split(':')
        try:
            if len(stamp) == 1:
                raise IndexError()

            for i in range(len(stamp)):
                time[i] = stamp[i]
        except IndexError:
            hexchat.prnt('Time must be formatted hh:mm[:ss]')
            raise Exception()

    for i in range(len(date)):
        date[i] = int(date[i])

    for i in range(len(time)):
        time[i] = int(time[i])

    test = datetime(now.year, date[0], date[1], time[0], time[1], time[2])
    diff = test - now
    year = (now.year - 1) if diff.days >= 0 else now.year

    return datetime(year, date[0], date[1], time[0], time[1], time[2])

def pings(word, word_eol, userdata):
    if len(word) < 2:
        time = datetime(datetime.now().year - 1, 1, 1)
    elif word[1] == 'clear':
        del PINGS[:]
    else:
        try:
            time = convert_timestamp(word_eol[1])
        except Exception:
            return hexchat.EAT_ALL

    if PINGS:
        hexchat.prnt('Pings since ' + str(time))

    for ping in PINGS:
        diff = ping.time - time
        if diff.days >= 0:
            hexchat.prnt(str(ping))

    return hexchat.EAT_ALL

def catch(word, word_eol, userdata):
    PINGS.append(Ping(datetime.now(), word[0], word[1]))
    return hexchat.EAT_NONE

def unload(userdata):
    hexchat.prnt('{} unloaded'.format(__module_name__))

def init():
    hexchat.hook_command('pings', pings,
                         help='Usage: PINGS [date (MM-DD)] [time (hh:mm[:ss])], lists pings since time specified')
    hexchat.hook_print('Channel Msg Hilight', catch)
    hexchat.hook_unload(unload)
    hexchat.prnt('Loaded {} {}'.format(__module_name__, __module_version__))

init()
