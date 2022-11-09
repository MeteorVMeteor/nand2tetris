from Parser import *
from CodeWriter import *

def main(addr, filename):
    newfile = Parser(f'{addr}\{filename}')
    writefile = CodeWriter(addr)
    writefile.setFileName(filename.split('.')[0])
    while newfile.hasMoreCommands():
        newfile.advance()
        cmdtype = newfile.commandType()
        code1 = None
        code2 = None
        try:
            code1 = newfile.arg1()
            code2 = newfile.arg2()
        except:
            pass
        writefile.apply(cmdtype, code1, code2)
    writefile.Close()

# SimpleAdd success
# main(r'D:\Download\nand2tetris\projects\07\StackArithmetic\SimpleAdd', r'SimpleAdd.vm')
# StackTest success
# main(r'D:\Download\nand2tetris\projects\07\StackArithmetic\StackTest', r'StackTest.vm')
# BasicTest success
# main(r'D:\Download\nand2tetris\projects\07\MemoryAccess\BasicTest', r'BasicTest.vm')
# PointerTest success
# main(r'D:\Download\nand2tetris\projects\07\MemoryAccess\PointerTest', r'PointerTest.vm')
# StaticTest success
# main(r'D:\Download\nand2tetris\projects\07\MemoryAccess\StaticTest', r'StaticTest.vm')