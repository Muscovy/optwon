#Optwon
#Noobfish Personality Core
#---
#"Who's that?" They ask, with no response availed.
#"Just some noob" Everyone says, and they all exhaled. 
#Little do they know, he's watching your every move.
#---

import threading
import os
import random
import string

import databank
import irc_core
import base_core

from ncks import *

class Noobfish(base_core.BaseCore):
    def __init__(self):
        base_core.BaseCore.__init__(self)
        self.switch = 0
        self.log = self.load() #Loads all saved logs under data\noobfish
        self.irc = irc_core.IRC(self,'Walter', 'walter', 'mibbit', channel='#Nebtown')
        self.irc.start()
        self.save()
        print('-- Noobfish core loaded. --')
        
    def load(self):
        print('-- Loading log --')
        path = os.path.join('data','noobfish')
        file = os.path.join('data','noobfish','noobfish.optwon')
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.exists(file):
            bees = databank.Databank()
            bees.save('noobfish','data\\noobfish')
        bank = databank.load('noobfish','data\\noobfish')
        return bank
        
    def save(self):
        threading.Timer(10.0, self.save).start()
        print('-- Saving log --')
        self.log.save('noobfish','data\\noobfish')
        
    def process(self,line):
        line = line.split() # :NAME!REAL_NAME@HOSTMASK TYPE (CHANNEL/USER [If PM]) :MESSAGE ///////////////// [0]NAME [1]TYPE [2]CHANNEL/USER [3]MESSAGE
        nick = line[0].split('!')[0][1:]
        if nick is not self.irc.NICK:
            if 'privmsg' in line[1].lower():
                text = ' '.join(line[3:])[1:]
                if self.irc.NICK in line[2]:
                    if self.checkmod(nick):
                        if 'switch' in text.lower():
                            self.switch = not self.switch
                            self.irc.pm(nick,'Changed TALK mode to ' + str(self.switch))
                        elif self.irc.NICK.lower() in text.lower():
                            temp = text.split()
                            if len(temp) > 1:
                                temp = [x for x in temp if self.irc.NICK.lower() not in x.lower()]
                                temp = [x for x in temp if x not in string.punctuation]
                                temp = random.choice(temp)
                                temp = self.log.random3(temp)
                                temp = self.humanize(temp)
                                threading.Timer(temp[1], self.irc.pm, [nick, temp[0]]).start()
                            else:
                                temp = self.log.random3(temp)
                                temp = self.humanize(temp)
                                threading.Timer(temp[1], self.irc.pm, [nick, temp[0]]).start()
                elif self.irc.NICK.lower() not in text.lower():     
                    if 'gman' not in nick.lower() and self.irc.NICK.lower() not in text.lower():
                        print('Parsing', '"'+text+'"', 'for', nick.upper())
                        self.log.parse(text)
                                
                if self.switch:
                    if self.irc.NICK.lower() in text.lower():
                        temp = text.split()
                        if len(temp) > 1:
                            temp = [x for x in temp if self.irc.NICK.lower() not in x.lower()]
                            temp = [x for x in temp if x not in string.punctuation]
                            temp = random.choice(temp)
                            temp = self.log.random3(temp)
                            temp = self.humanize(temp)
                            threading.Timer(temp[1], self.irc.msg, [temp[0]]).start()
                        else:
                            temp = self.log.random2()
                            temp = self.humanize(temp)
                            threading.Timer(temp[1], self.irc.msg, [temp[0]]).start()

if __name__ == '__main__':
    noobfish = Noobfish()