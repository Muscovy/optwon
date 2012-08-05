#Optwon
#Base Personality Core

import random
import string

from ncks import *

class BaseCore(object):
    def __init__(self):
        self.irc = None
        self.mods = ['kris', 'alex']
        self.delaymod = [0.15, 0.5]
    
    def process(self,line):
        pass
        
    def checkmod(self,user):
        user = user.lower()
        for mod in self.mods:
            if mod in user:
                return 1
        
    def standards(self,line):
        line = line.split() # :NAME!REAL_NAME@HOSTMASK TYPE (CHANNEL/USER [If PM]) :MESSAGE ///////////////// [0]NAME [1]TYPE [2]CHANNEL/USER [3]MESSAGE
        nick = line[0].split('!')[0][1:]
        
        if 'privmsg' in line[1].lower():
            text = ' '.join(line[3:])[1:]
            s_text = text.split() #For detection purposes
            if self.irc.NICK in line[2]:
                if self.checkmod(nick):
                    if text == 'ping':
                        self.irc.pm(nick, 'pong')
                        
                    if len(s_text) <=1: return #There is only ONE argument given, just run
                    
                    if s_text[0] == 'quit':
                        self.irc.pm(nick, 'Quitting with message ' + ' '.join(s_text[1:]))
                        self.irc.quit(' '.join(s_text[1:]))
                    elif s_text[0] == 'nick':
                        self.irc.pm(nick, 'Changing nickname to ' + '_'.join(s_text[1:]))
                        self.irc.setnick('_'.join(s_text[1:])) #Names can't have spaces so might as well join the string using _'s (So "John Freeman of Bop" turns into "John_Freeman_Of_Bop")
                    elif s_text[0] == 'chan':
                        self.irc.pm(nick, 'Changing channel to ' + ''.join(s_text[1:]))
                        self.irc.setchannel(''.join(s_text[1:]))
                    elif s_text[0] == 'pm':
                        if len(s_text) <= 2: return #Not enough args
                        self.irc.pm(nick, 'Sending PM "' + ' '.join(s_text[2:]) + '" to ' + s_text[1])
                        self.irc.pm(s_text[1], ' '.join(s_text[2:]))
                    elif s_text[0] == 'msg':
                        self.irc.pm(nick, 'Sending this message to current channel: ' + ' '.join(s_text[1:]))
                        self.irc.msg(' '.join(s_text[1:]))    
    def typo(self,phrase):
        phrase = phrase.lower()
        leopard = [
            ['`','1','2','3','4','5','6','7','8','9','0','-','=','[*]BKSP'],
            ['    ','q','w','e','r','t','y','u','i','o','p','[',']','\','],
            ['[*]CAPS','a','s','d','f','g','h','j','k','l',';',"'",'[*]RETN'],
            ['[*]SHFT','z','x','c','v','b','n','m',',','.','/','[*]SHFT'],
            ['[*]CTRL','[*]SUPR','[*]ALTL', ' ',' ',' ',' ',' ',' ', '[*]ATLR','[*]SUPR','[*]MENU','[*]CTRL']
        ]
        
        for l in phrase:
            index = [0,0]
            for i in range(len(leopard)):
                row = leopard[i]
                try:
                    index = [i, leopard.index(l)]
                except ValueError:
                    
        
    def delay(self,phrase):
        bees = 0
        for i in len(phrase):
            bees+= random.uniform(self.delaymod[0], self.delaymod[1])
            
        print('DELAY:', bees, '(MIN:', self.delaymod[0], 'MAX:', self.delaymod[1] + ')')
        return bees
    
    def humanize(self,phrase):
        bees = []
        
        