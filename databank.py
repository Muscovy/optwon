#Optwon
#Databank Library

import random
import pickle
import os

from ncks import *

class Databank(object):
    def __init__(self):
        self.root = Node()
        
    def parse(self,text):
        if not text: return
        text = text.split()
        first = text.pop(0)
        start = None
        check = self.root.exists(first)
        if check:
            start = check
            start.frequency+=1
        if not start:
            start = Node()
            start.value = first
            self.root.add(start)
        
        if not text: return
        
        c_node = start
        for word in text:
            check = c_node.exists_family(word)
            if check:
                next = check
                c_node.add(next)
                c_node = next
                continue
            next = Node()
            next.value = word
            c_node.add(next)
            if text.index(word) == (len(text)-1):
                next.end = 1
            c_node = c_node.exists(word) or next
            
    def random(self):
        bees = []
        node = self.root.randnode()
        while node:
            bees.append(node)
            node = node.randnode()
        bees = ' '.join([str(x) for x in bees])
        return bees
        
    def random2(self):
        bees = []
        node = self.root.randnode()
        print('USING:',node.value)
        while node:
            temp = node.randnode()
            if not temp:
                print('END')
                break
            print('TRAWL:',temp.value)
            node = temp
            if node.end:
                break
        
        while node:
            print('BUILD:',node.value)
            temp = node.randparent()
            if not temp: break
            if temp.end: continue
            bees.append(node)
            node = temp
            
        bees = ' '.join(reversed([str(x) for x in bees]))
        return bees
        
    def save(self,name,path='data'):
        path = path.split('\\')
        dir = os.path.join(*path)
        path = os.path.join(dir,name+'.optwon')
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(path,'wb') as save:
            pickle.dump(self,save)

class Node(object):
    def __init__(self):
        self.value = None
        self.parents = []
        self.nodes = []
        self.end = 0
        self.frequency = 1
        
    def add(self,node):
        if self.end: return
        check = self.exists_family(node.value)
        if check:
            check.frequency+=1
            
        p_check = 0
        if node.parents:
            for p in node.parents:
                if p.value == self.value:
                    p_check = 1
        if not node.parents or not p_check:
            node.parents.append(self)
        if not self.exists(node.value):
            self.nodes.append(node)
        
    def exists(self,value):
        for n in self.nodes:
            if n.value == value:
                return n
                
    def exists_family(self,value):
        for p in self.parents:
            for n in p.nodes:
                for s in n.nodes:
                    if s.value == value:
                        return s
        
    def next(self, index=0):
        if not self.nodes or self.end: return
        return self.nodes[index]
        
    def prev(self,index=0):
        if not self.parents: return
        return self.parents[index]
        
    def randparent(self):
        if not self.parents: return
        return random.choice(self.parents)
        
    def randnode(self):
        if not self.nodes or self.end: return
        return random.choice(self.nodes)
        
    def __str__(self):
        return self.value or ''def load(name,path='data'):
    path = path.split('\\') + [name+'.optwon']
    path = os.path.join(*path)
    with open(path,'rb') as load:
        bank = pickle.load(load)
        print('--', name.upper(), 'Loaded. --')
        return bank
        
if __name__ == '__main__':
    # bank = load('aubergine','data\\aubergine')
    # bank.parse('Your couch is not soft.')
    # bank.parse('Your couch is very unappealing.')
    # bank.parse('Your couch is very soft.')
    # bank.parse('Your mother is a mistress of the night.')
    # bank.parse('Your vase is not pretty.')
    # bank.parse('I like to eat cake.')
    # bank.parse('I like to eat apple pie.')
    # bank.parse('I like to eat ice cream.')
    # bank.parse('I like to eat ice cream cake.')
    # bank.parse('I like to eat nothing.')
    # bank.parse('My couch is awesome.')
    # bank.parse('My couch sucks.')
    # bank.parse('My vase really sucks.')
    # print(bank.root.nodes)
    
    # for node in bank.root.nodes:
        # print('-'*3)
        # print(node)
        # print(node.frequency)
        # for n in node.nodes:
            # t_node = n
            # while t_node:
                # print('-'*3)
                # print('PARENT:',[x.value for x in t_node.parents])
                # print('NODE:',t_node)
                # print('FREQUENCY',t_node.frequency)
                # t_node = t_node.next()
            # print('*'*5)
        # print('='*5)
    
    # print('\n\n')
    # words = []
    # for i in range(10):
        # next = bank.random2()
        # words.append(next)
        # print(next)
    
    # for w in words:
        # print(w)
        
    # bank.save('Toast')
    
    #/////////////////////////////////////////////////////////////////////
    
    # bank = load('aubergine','data\\aubergine')
    
    # words = []
    # for i in range(10):
        # next = bank.random2()
        # words.append(next)
        # print(next)
    
    # for w in words:
        # print(w)
        
   #/////////////////////////////////////////////////////////////////////
   
    bank = Databank()
    
    bank.parse('I like to eat cake')
    bank.parse('You like to eat cake')
    bank.parse('I hate cake')
    bank.parse('You love cake')