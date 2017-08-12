##
## pings - capture HexChat highlighted messages for review
## Copyright (C) 2017 David McMackins II
##
## Redistributions, modified or unmodified, in whole or in part, must retain
## applicable copyright or other legal privilege notices, these conditions, and
## the following license terms and disclaimer.  Subject to these conditions,
## the holder(s) of copyright or other legal privileges, author(s) or
## assembler(s), and contributors of this work hereby grant to any person who
## obtains a copy of this work in any form:
##
## 1. Permission to reproduce, modify, distribute, publish, sell, sublicense,
## use, and/or otherwise deal in the licensed material without restriction.
##
## 2. A perpetual, worldwide, non-exclusive, royalty-free, irrevocable patent
## license to reproduce, modify, distribute, publish, sell, use, and/or
## otherwise deal in the licensed material without restriction, for any and all
## patents:
##
##     a. Held by each such holder of copyright or other legal privilege,
##     author or assembler, or contributor, necessarily infringed by the
##     contributions alone or by combination with the work, of that privilege
##     holder, author or assembler, or contributor.
##
##     b. Necessarily infringed by the work at the time that holder of
##     copyright or other privilege, author or assembler, or contributor made
##     any contribution to the work.
##
## NO WARRANTY OF ANY KIND IS IMPLIED BY, OR SHOULD BE INFERRED FROM, THIS
## LICENSE OR THE ACT OF DISTRIBUTION UNDER THE TERMS OF THIS LICENSE,
## INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
## A PARTICULAR PURPOSE, AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS,
## ASSEMBLERS, OR HOLDERS OF COPYRIGHT OR OTHER LEGAL PRIVILEGE BE LIABLE FOR
## ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN ACTION OF CONTRACT, TORT,
## OR OTHERWISE ARISING FROM, OUT OF, OR IN CONNECTION WITH THE WORK OR THE USE
## OF OR OTHER DEALINGS IN THE WORK.
##

__module_name__ = 'pings'
__module_version__ = '0.0'
__module_description__ = 'Highlighted message tracker'
__module_author__ = 'David McMackins II'

import hexchat
from datetime import datetime, timedelta

STARTING_TIME = datetime.now()

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
    date = [STARTING_TIME.year, STARTING_TIME.month]
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

                test = datetime(now.year, now.month, now.day, int(time[0]),
                                int(time[1]), int(time[2]))
                if test > now:
                    test -= timedelta(1)
                    date = [test.month, test.day]
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
        time = STARTING_TIME
    elif word[1] == 'clear':
        del PINGS[:]
    else:
        try:
            time = convert_timestamp(word_eol[1])
        except Exception:
            return hexchat.EAT_ALL

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
