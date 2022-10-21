import Symbol
import Code
from ast import main

def parser(address):
    file = open(address, 'r')
    doc = []
    for line in file:
        line = line.strip('\n')
        doc += [line]
    file.close()
    return doc

def hasMoreCommands(cnt, doc):
    return cnt < len(doc)

def advance(cnt, doc):
    return doc[cnt]

def commandType(text):
    if '@' in text:
        return 'A'
    elif '(' in text and ')' in text:
        return 'L'
    else:
        return 'C'

def comp(text):
    return Code.comp(text)

def dest(text):
    return Code.dest(text)

def jump(text):
    return Code.jump(text)