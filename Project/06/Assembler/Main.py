import Parser
import Symbol
import os
def main():
    # address = r'D:\Download\CS\nand2tetris\nand2tetris\projects\06\add\Add.txt' #add
    write_add = r'D:\Download\CS\nand2tetris\nand2tetris\projects\06\Mine'
    # address = r'D:\Download\CS\nand2tetris\nand2tetris\projects\06\max\Max.txt' #max
    address = r'D:\Download\CS\nand2tetris\nand2tetris\projects\06\pong\Pong.txt'#pong
    doc = Parser.parser(address)
    cnt = 0
    symtable = Symbol.symbol_iter(doc)
    symtable1 = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
                    'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
                    'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
                    'SCREEN':0x4000, 'KBD':0x6000}
    symtable = symtable | symtable1
    index = 0
    file = open(write_add + '\Pong' + '.hack','w')
    while Parser.hasMoreCommands(cnt, doc):
        text = Parser.advance(cnt, doc)
        type = Parser.commandType(text)
        res = 0
        if 'A' in type:
            res, symtable, index = Symbol.symbol(text, symtable, index)
            file.write(res + '\n')
        elif 'C' in type:
            res = Parser.comp(text) + Parser.dest(text) + Parser.jump(text)
            file.write(res + '\n')
        cnt += 1
    file.close()