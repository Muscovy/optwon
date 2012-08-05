#Optwon
#Base Personality Core

import random
import string

from ncks import *

class BaseCore(object):
    def __init__(self):
        self.irc = None
        self.mods = ['kris', 'alex']
        self.delaymod = [0.065, 0.07] #[Min, Max]
        self.mistypemod = [0.0065, 0.00015] #[Base percent, Increment per letter] (Percent represented in decimal format)
        
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
                        self.irc.pm(nick, 'Quitting with message ' + '"' + ' '.join(s_text[1:]) + '"')
                        self.irc.quit(' '.join(s_text[1:]))
                    elif s_text[0] == 'nick':
                        self.irc.pm(nick, 'Changing nickname to ' + '"' + '_'.join(s_text[1:]) + '"')
                        self.irc.setnick('_'.join(s_text[1:])) #Names can't have spaces so might as well join the string using _'s (So "John Freeman of Bop" turns into "John_Freeman_Of_Bop")
                    elif s_text[0] == 'chan':
                        self.irc.pm(nick, 'Changing channel to ' + ''.join(s_text[1:]))
                        self.irc.setchannel(''.join(s_text[1:]))
                    elif s_text[0] == 'pm':
                        if len(s_text) <= 2: return #Not enough args
                        self.irc.pm(nick, 'Sending PM "' + ' '.join(s_text[2:]) + '" to ' + s_text[1])
                        self.irc.pm(s_text[1], ' '.join(s_text[2:]))
                    elif s_text[0] == 'msg':
                        self.irc.pm(nick, 'Sending this message to current channel: ' + '"' + ' '.join(s_text[1:]) + '"')
                        self.irc.msg(' '.join(s_text[1:]))    
    def typo(self,phrase): #Makes typos happen
        def trans_leopard(phrase): #This method just exchanges the unique symbols (Things preceeded with [*]) with their proper "effect".
            bees = phrase #Make a copy of the phrase (It's an exploded array of every letter, like the word "cake" becomes ['c','a','k','e'])
            for letter in phrase:
                if letter[0:3] == '[*]': #If its a unique symbol
                    key = letter[3:] #This part is the ID.
                    
                    if key == 'BKSP': #Backspace! We delete the letter preceeding the symbol.
                        try:
                            del bees[bees.index(letter)-1]
                        except IndexError: #If the index doesn't exist then just ignore
                            pass
                    elif key == 'CAPS': #Makes everything after the symbol caps.
                        bees[bees.index(letter):] = [x.upper() for x in bees[bees.index(letter):]]
                    elif key == 'RETN': #We cut the array where it is, simulating like someone accidentally pushed "Enter" and sent their message premature.
                        bees = bees[:bees.index(letter)]
                        break #<-- Note the break
                    elif key == 'SHFT': #Makes the next letter uppercase.
                        try:
                            mod = bees[bees.index(letter)+1]
                        except IndexError:
                            pass
                        if mod:
                            bees[min(len(bees)-1,bees.index(letter)+1)] = mod.upper()
                    elif key == 'CTRL': #I added these to simulate the ability for someone to hit them accidentally. They don't do anything though.
                        pass #Feel free to make them do something though. I can't think of what.
                    elif key == 'SUPR':
                        pass
                    elif key == 'ALTL':
                        pass
                    elif key == 'ALTR':
                        pass
                    elif key == 'MENU':
                        pass
                        
                    bees.remove(letter) #We remove the unique symbol after.
            
            return bees #Return the exploded array.
        #//////////////////////////////////
        bees = list(phrase) #Explode the string into individual letters
        phrase = phrase.lower() #Case insensitivity. The most CRUCIAL thing to remember is that bees and phrase are SEPARATE. This is extremely important.
        leopard = [ #If they weren't separate then you would have concurrency errors.
            ['`','1','2','3','4','5','6','7','8','9','0','-','=','[*]BKSP'],
            ['    ','q','w','e','r','t','y','u','i','o','p','[',']','\','],
            ['[*]CAPS','a','s','d','f','g','h','j','k','l',';',"'",'[*]RETN'],
            ['[*]SHFT','z','x','c','v','b','n','m',',','.','/','[*]SHFT'],
            ['[*]CTRL','[*]SUPR','[*]ALTL', ' ',' ',' ',' ',' ',' ', '[*]ATLR','[*]SUPR','[*]MENU','[*]CTRL'] #This is the leopard fully laid out.
        ] #It's just a multidimensional array of the keyboard. So leopard[1][1] is the letter Q. This lets us do vector math on the keyboard. XD
        #Quiz time! What do you get when you take leopard[1][1] and +1 to the x axis and +2 to the y axis?
        #(The answer is the letter "d")
        
        mistype_chance = self.mistypemod[0] + (self.mistypemod[1] * len(phrase)) #Mistype chance calculation.
        #<OTHER CHANCE CALCULATIONS GO HERE>
        
        for l in phrase: #Iterate each letter.
            index = []
            for i in range(len(leopard)): #We find the index of the letter inside the keyboard array. Slightly hacky.
                row = leopard[i]
                try:
                    index = [i, row.index(l)]
                except ValueError:
                    pass
                    
            if not index: continue #This means that the letter doesn't exist inside the leopard (Would happen if its something like a shifted puncuation like %)
            #We just ignore it, then.
            
            if chance(mistype_chance): #Using the previously set mistype chance, we call NCKS's chance() function. Check it out
                letter = leopard[clamp(0, index[0]+random.randint(-1,1), len(leopard)-1)][clamp(0, index[1]+random.randint(-1,1), len(leopard[index[0]])-1)]
                #Vector math on leopard. Essentially just gets the letter one square away in any direction, including diagonals. We clamp it to prevent errors.
                if bees[phrase.index(l)].isupper(): #Preserve the case
                    letter = letter.upper()
                bees[phrase.index(l)] = letter
                print('MISTYPE:', l, 'TO', letter) #Debug prints
            
            #<OTHER MISTAKE IF STATMENTS GO HERE>
            
        bees = trans_leopard(bees) #The function we wrote above.
        
        return ''.join(bees)
        
    def delay(self,phrase):
        bees = 0
        for i in range(len(phrase)):
            bees+= random.uniform(self.delaymod[0], self.delaymod[1])
            
        print('DELAY:', bees, '(MIN:', self.delaymod[0], 'MAX:', str(self.delaymod[1]) + ')')
        return bees
    
    def humanize(self,phrase):
        bees = []
        phrase = self.typo(phrase)
        bees.append(phrase)
        bees.append(self.delay(phrase))
        
        return beesif __name__ == '__main__':
    gman = BaseCore()
    for i in range(10):
        bees = gman.typo('I like to eat cake.')
        print(bees)
        print(gman.delay(bees))