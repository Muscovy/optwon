#Optwon
#Aubergine Personality Core
#---
#Flushed a shade deeper than even its name itself.
#There is nothing more ridiculed than the legend himself.
#Watch out, Aubergine's coming to a channel near you.
#---

import threading
import os
import random
import string

import databank
import irc_core
import base_core

from ncks import *

class Aubergine(base_core.BaseCore):
    def __init__(self):
        base_core.BaseCore.__init__(self)
        self.log = self.load() #Loads the saved log under data\aubergine
        self.irc = irc_core.IRC(self,'Aubergine', 'aubergine', 'purple')
        self.irc.start()
        self.save()
        print('-- Aubergine core loaded. --')
        
    def load(self):
        print('-- Loading log --')
        path = os.path.join('data','aubergine')
        file = os.path.join('data','aubergine','aubergine.optwon')
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.exists(file):
            bees = databank.Databank()
            bees.save('aubergine','data\\aubergine')
        bank = databank.load('aubergine','data\\aubergine')
        return bank
        
    def save(self):
        threading.Timer(10.0, self.save).start()
        print('-- Saving log --')
        self.log.save('aubergine','data\\aubergine')
        
    def process(self,line):
        line = line.split() # :NAME!REAL_NAME@HOSTMASK TYPE (CHANNEL/USER [If PM]) :MESSAGE ///////////////// [0]NAME [1]TYPE [2]CHANNEL/USER [3]MESSAGE
        nick = line[0].split('!')[0][1:]
        if nick is not self.irc.NICK:
            if 'privmsg' in line[1].lower():
                text = ' '.join(line[3:])[1:]
                if self.irc.NICK in line[2]:    
                    pass
                elif self.irc.NICK.lower() in text.lower():
                    temp = text.split()
                    if len(temp) > 1:
                        temp = [x for x in temp if self.irc.NICK.lower() not in x.lower()]
                        temp = [x for x in temp if x not in string.punctuation]
                        temp = random.choice(temp)
                        temp = self.humanize(self.log.random3(temp)) # Format: [<MESSAGE>, <DELAY>] str/float
                        threading.Timer(temp[1], self.irc.msg, [temp[0]]).start()
                    else:
                        temp = self.log.random2()
                        temp = self.humanize(temp)
                        threading.Timer(temp[1], self.irc.msg, [temp[0]]).start()
                else:     
                    print('Parsing', '"'+text+'"', 'for', nick.upper())
                    self.log.parse(text)

if __name__ == '__main__':
    aubergine = Aubergine()