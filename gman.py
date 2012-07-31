#Optwon
#Gman (IRC Client from the Gman box) Personality Core
#---
#As characteristic of the true Gman, he lies silent and watchful, seeing everything that goes on. He is the commander of Optwon, the one that
#coordinates the otherwise unruly swarm of bots.
#United we stand, Divided we fall.
#---

import base_core
import irc_core

import threading

from ncks import *

class Gman(base_core.BaseCore):
    def __init__(self):
        base_core.BaseCore.__init__(self)
        self.irc = irc_core.IRC(self, 'John_of_Bop', 'john', 'John Freeman') #format is USERNAME, IDENT, REALNAME
        self.irc.start()
        self.irc.msg('FUK YEAH IM JOHNFREMAN') #Send message
        print('-- Gman core loaded. --')
        
    def process(self,line):
        if 'john: quit' in line.lower():
            self.irc.msg('yea ok fuk u guys im leving')
            self.irc.send('QUIT :#Nebtwon')