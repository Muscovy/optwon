#Optwon
#IRC Engine/Interface

import sys
import socket
import time

from ncks import *

class IRC(object):
    def __init__(self, p_core, host, port, channel, nick, ident, realname):
        self.personality_core = p_core
        self.HOST = host #gmod.nebtown.info (IP)
        self.PORT = port #27033 (Default is 6667)
        self.CHANNEL = channel # #Nebtwon
        self.NICK = nick #John_of_Bop (Nickname)
        self.IDENT = ident #john (The stuff before the hostmask, I think. Like john@192.168.0.1)
        self.REALNAME = realname #John Freeman (Whois info)
        self.readbuffer = ''
        
        self.s = socket.socket()
        self.s.connect( (self.HOST, self.PORT) )
        self.send('NICK {}'.format(self.NICK))
        self.send('USER {} {} bla :{}'.format(self.IDENT, self.HOST, self.REALNAME))
        time.sleep(2) #Wait for USER auth to pass through
        self.send('JOIN {}\r\n'.format(self.CHANNEL))
        time.sleep(2) #Wait for the stupid history to load so that we can...
        self.s.recv(1024 * 4) #Throw away the first chunk, pretty much.
        print('-- IRC Core Loaded. --')
        
    def msg(self, msg):
        self.send('PRIVMSG {} :{}\r\n'.format(self.CHANNEL, msg))
        
    def send(self, cmd):
        self.s.send(bytes(cmd+'\r\n','UTF-8'))
        
    def mainloop(self):
        while 1:
            self.readbuffer = self.readbuffer + self.s.recv(1024).decode('UTF-8')
            temp = self.readbuffer.split('\n')
            self.readbuffer = temp.pop()
            
            for line in temp:
                print(line)
                
                self.personality_core.process(line)
                
                line = line.split()
                
                if line[0] == 'PING':
                    self.send('PONG {}'.format(line[1]))