from Parser import *
from CodeWriter import *

def main(addr, filename, Init=False):
    newfile = Parser(f'{addr}\{filename}')
    writefile = CodeWriter(addr)
    writefile.setFileName(filename.split('.')[0], Init)
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

# Use rString when reading file, or it will become D:\\Do...

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
# BasicLoop success
# main(r'D:\Download\nand2tetris\projects\08\ProgramFlow\BasicLoop', r'BasicLoop.vm')
# FibonacciSeries success
# main(r'D:\Download\nand2tetris\projects\08\ProgramFlow\FibonacciSeries', r'FibonacciSeries.vm')
# SimpleFunction success
# main(r'D:\Download\nand2tetris\projects\08\FunctionCalls\SimpleFunction', r'SimpleFunction.vm')
# NestedCall success
# main(r'D:\Download\nand2tetris\projects\08\FunctionCalls\NestedCall', r'NestedCall.vm', Init = True)
# FibonacciElement success
# main(r'D:\Download\nand2tetris\projects\08\FunctionCalls\FibonacciElement', r'FibonacciElement.vm', Init = True)
# StaticsTest success
# main(r'D:\Download\nand2tetris\projects\08\FunctionCalls\StaticsTest', r'StaticsTest.vm', Init = True)