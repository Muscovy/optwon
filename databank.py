#Optwon
#Databank Library

import random

from ncks import *

class Databank(object):
    def __init__(self):
        self.sentences = []
        
    def parse(self,text):
        if not text: return
        text = text.split()
        first = text.pop(0)
        root = None
        for node in self.sentences:
            if node.value == first:
                root = node
                root.frequency+=1
        if not root: 
            root = Node()
            root.value = first
            self.sentences.append(root)
        
        if not text: return
        
        c_node = root
        for word in text:
            next = Node()
            next.value = word
            c_node.add(next)
            c_node = c_node.exists(word) or next
            
    def random(self):
        bees = []
        node = random.choice(self.sentences)
        while node:
            bees.append(node)
            node = node.randnode()
        bees = ' '.join([str(x) for x in bees])
        return beesclass Node(object):
    def __init__(self):
        self.parent = None
        self.value = None
        self.nodes = []
        self.frequency = 1
        
    def add(self,node):
        for n in self.nodes:
            print(n.value, 'vs', node.value)
            if n.value == node.value:
                n.frequency+=1
                return
        node.parent = self
        self.nodes.append(node)
        
    def exists(self,value):
        for n in self.nodes:
            if n.value == value:
                return n
        
    def next(self, index=0):
        if not self.nodes: return
        return self.nodes[index]
        
    def randnode(self):
        if not self.nodes: return
        return random.choice(self.nodes)
        
    def __str__(self):
        return self.value or ''
        if __name__ == '__main__':
    bank = Databank()
    bank.parse('I like to eat cake.')
    bank.parse('I like to eat apple pie.')
    bank.parse('Your couch is not soft.')
    bank.parse('Your vase is not pretty.')
    bank.parse('Your mother is a mistress of the night.')
    bank.parse('I like to eat ice cream.')
    bank.parse('I like to eat ice cream cake.')
    bank.parse('Your couch is very soft.')
    bank.parse('Your couch is very unappealing.')
    bank.parse('I like to eat nothing.')
    print(bank.sentences)
    
    for node in bank.sentences:
        print('-'*3)
        print(node)
        print(node.frequency)
        for n in node.nodes:
            t_node = n
            while t_node:
                print('-'*3)
                print(t_node)
                print(t_node.frequency)
                t_node = t_node.next()
            print('*'*5)
        print('='*5)
    
    print('\n\n')
    for i in range(5):
        print(bank.random())