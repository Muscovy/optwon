#Optwon
#Spy Personality Core
#---
#Silent and cunning, the Spy lives up to his name. Always watching, always quiet.
#He's got everyone in his sights, and nobody escapes his keen eye.
#Right behind you.
#---

import threading
import os
import random

import databank
import irc_core
import base_core

from ncks import *class Spy(base_core.BaseCore):
    def __init__(self):
        base_core.BaseCore.__init__(self)
        self.logs = self.load() #Loads all saved logs under data\spy
        self.irc = irc_core.IRC(self,'MrCrispy', 'crispy', 'mibbit',channel='#Nebtown')
        self.irc.start()
        self.save()
        print('-- Spy core loaded. --')
        
    def load(self):
        bees = {}
        print('-- Loading all logs --')
        path = os.path.join('data','spy')
        if not os.path.isdir(path):
            os.makedirs(path)
        for log in os.listdir(path):
            name = log.split('.')[0]
            bank = databank.load(name,'data\\spy')
            bees[name] = bank
            
        return bees
        
    def save(self):
        threading.Timer(10.0, self.save).start()
        print('-- Saving all logs --')
        for k,v in self.logs.items():
            v.save(k,'data\\spy')
        
    def process(self,line):
        line = line.split() # :NAME!REAL_NAME@HOSTMASK TYPE (CHANNEL/USER [If PM]) :MESSAGE ///////////////// [0]NAME [1]TYPE [2]CHANNEL/USER [3]MESSAGE
        nick = line[0].split('!')[0][1:]
        if 'privmsg' in line[1].lower():
            text = ' '.join(line[3:])[1:]
            if self.irc.NICK in line[2]:
                pass #Just ignore everything if its a PM
            elif 'mibbit' not in line[0].lower():
                if 'gman' not in nick.lower():
                    typer = self.logs.get(nick)
                    if not typer:
                        self.logs[nick] = databank.Databank()
                        typer = self.logs.get(nick)
                    print('Parsing', '"'+text+'"', 'for', nick.upper())
                    typer.parse(text)
            else:
                print('Disregarding {}, mibbiter'.format(nick))if __name__ == '__main__':
    spy = Spy()