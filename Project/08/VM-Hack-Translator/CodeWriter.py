class CodeWriter:
    #use in add, sub, and, or operation
    take_two_arg = ('@SP\n' 
                    + 'AM=M-1\n' #first operator(M[M[SP]-1]) and stackpointer -= 1
                    + 'D=M\n' #take first operator in D
                    + 'A=A-1\n' #second operator(M[A]) and stackpointer nochange
                    )
    #use in neg, not, pop operation, if-goto
    take_one_arg = ('@SP\n'
                    + 'AM=M-1\n' #first operator in M[M[SP]-1] and stackpointer -= 1
                    )
    stack_pointer_inc = ('@SP\n'
                    + 'M=M+1\n'
                    )

    def __init__(self, addr):
        self.addr = addr
        self.file = None
        self.output = None
        self.nameindex = 0
    
    def setFileName(self, name, Init = False):
        self.name = [name]
        filename = f'{self.addr}\{name}.asm'
        self.file = open(filename, 'w')
        if Init:
            self.apply('INIT')

    def apply(self, cmdtype, arg1 = None, arg2 = None):
        if cmdtype == 'C_ARITHMETIC':
            self.writeArithmetic(arg1)
        elif cmdtype == 'C_PUSH' or cmdtype == 'C_POP':
            self.writePushPop(cmdtype, arg1, arg2)
        elif cmdtype == 'C_LABEL':
            self.output = f'({arg1})\n'
        elif cmdtype == 'C_GOTO' or cmdtype == 'C_IF':
            self.writeGoToIf(cmdtype, arg1)
        elif cmdtype == 'C_FUNCTION':
            self.writeFunction(arg1, arg2)
        elif cmdtype == 'C_RETURN':
            self.writeReturn()
        elif cmdtype == 'C_CALL':
            self.writeCall(arg1, arg2)
        elif cmdtype == 'INIT':
            self.writeInit()
        self.file.write(self.output)

    def writeInit(self):
        self.output = ('@256\n'
                        + 'D=A\n'
                        + '@SP\n'
                        + 'M=D\n' # set SP = 256
                        + self.writeCall('Sys.init', 0, Init=True) # call Sys.init
        )

    def writeArithmetic(self, command):
        if(command == 'add'):
            self.output = self.take_two_arg + 'M=M+D\n'
        elif(command == 'sub'):
            self.output = self.take_two_arg + 'M=M-D\n'
        elif(command == 'and'):
            self.output = self.take_two_arg + 'M=M&D\n'
        elif(command == 'or'):
            self.output = self.take_two_arg + 'M=M|D\n'
        elif(command == 'neg'):
            self.output = self.take_one_arg + 'M=-M\n' + self.stack_pointer_inc
        elif(command == 'not'):
            self.output = self.take_one_arg + 'M=!M\n' + self.stack_pointer_inc
        elif(command == 'eq'):
            self.output = self.conditionJudge('JEQ')
        elif(command == 'gt'):
            self.output = self.conditionJudge('JGT')
        elif(command == 'lt'):
            self.output = self.conditionJudge('JLT')

    def conditionJudge(self, c_command):
        output = (self.take_two_arg
                + 'D=M-D\n' #judge > or = or <
                + f'@STATEMENT{self.nameindex}\n'
                + f'D;{c_command}\n'
                
                + '@SP\n' #if false
                + 'A=M-1\n'
                + 'M=0\n'
                + f'@CONTINUE{self.nameindex}\n'
                + '0;JMP\n'

                + f'(STATEMENT{self.nameindex})\n' #if true
                + '@SP\n'
                + 'A=M-1\n'
                + 'M=-1\n'

                + f'(CONTINUE{self.nameindex})\n'
                )
        self.nameindex += 1
        return output

    def writePushPop(self, command, segment, index):
        if command == 'C_PUSH':
            self.output = self.pushfunc(segment, index)
        elif command == 'C_POP':
            self.output = self.popfunc(segment, index)

    def writeGoToIf(self, cmdtype, funcname):
        output = None
        if cmdtype == 'C_IF':
            output = (self.take_one_arg
                    + 'D=M\n'
                    + f'@{funcname}\n'
                    + 'D;JNE\n'
                    )
        else:
            output = (f'@{funcname}\n' 
                    + '0;JMP\n'
                    ) 
        self.output = output

#  make sp go down argN times with pushing 0
    def writeFunction(self, funcname, argN):
        # self.name for static value, static name taken by class name
        self.name += [funcname.split('.')[0]]
        output = f'({funcname})\n'
        for _ in range(int(argN)):
            output += self.pushfunc('constant', 0)
        self.output = output

    def writeReturn(self):
        self.name = self.name[:-1]
        output = ('@LCL\n'
                + 'D=M\n' # D-register save LCL
                # ERROR because using R13 save LCL-5 and R13 is used in popfunc()
                + '@R14\n'
                + 'M=D\n' # M[R14] = M[LCL]
                + '@5\n'
                + 'A=D-A\n'
                + 'D=M\n' # D-register save return addr
                + '@R15\n'
                + 'M=D\n' # M[R15] = retrun addr


                + self.popfunc('argument', 0) #*ARG = pop()

                + self.getIndex('ARG', 1, True)
                + 'D=A\n' # ARG[1] in D-register
                + '@SP\n'
                + 'M=D\n' # SP = M[ARG] + 1

                + '@R14\n'
                + 'AM=M-1\n' # M[R14] = LCL-1
                + 'D=M\n' # D-register = M[LCL-1]
                + '@THAT\n'
                + 'M=D\n' # restore caller's THAT

                + '@R14\n'
                + 'AM=M-1\n' # M[R14] = LCL-2
                + 'D=M\n' # D-register = M[LCL-2]
                + '@THIS\n'
                + 'M=D\n' # restore caller's THIS

                + '@R14\n'
                + 'AM=M-1\n' # M[R14] = LCL-3
                + 'D=M\n' # D-register = M[LCL-3]
                + '@ARG\n'
                + 'M=D\n' # restore caller's ARG

                + '@R14\n'
                + 'AM=M-1\n' # M[R14] = LCL-4
                + 'D=M\n' # D-register = M[LCL-4]
                + '@LCL\n'
                + 'M=D\n' # restore caller's LCL

                + '@R15\n'
                + 'A=M\n' # A-register = return addr
                + '0;JMP\n' #goto return addr
                )
        self.output = output
    
    def writeCall(self, funcname, n, Init=False):
        pusharg = ('@SP\n'
                    + 'A=M\n'
                    + 'M=D\n'
                )
        output = (self.pushfunc('constant', f'RETURNADDR{self.nameindex}') # push return addr

                + '@LCL\n'
                + 'D=M\n'
                + pusharg
                + self.stack_pointer_inc # push *LCL

                + '@ARG\n'
                + 'D=M\n'
                + pusharg
                + self.stack_pointer_inc # push *ARG

                + self.pushfunc('pointer', '0') # push *THIS
                + self.pushfunc('pointer', '1') # push *THAT

                + '@SP\n'
                + 'D=M\n'
                + '@5\n'
                + 'D=D-A\n' # SP-5
                + f'@{n}\n'
                + 'D=D-A\n' # SP-n
                + '@ARG\n'
                + 'M=D\n' # *ARG = SP-5-n
                + '@SP\n'
                + 'D=M\n'
                + '@LCL\n'
                + 'M=D\n' # LCL = SP

                + f'@{funcname}\n'
                + '0;JMP\n' # goto funcname()
                + f'(RETURNADDR{self.nameindex})\n'
                )
        self.nameindex += 1
        if Init:
            return output
        self.output = output

# get address of segment[index] / M[segment]+index and save in A-register
    def getIndex(self, segment, index, ispointer = False):
        tmp = 'D=A\n'if not ispointer else 'D=M\n'
        output = (f'@{segment}\n'
                + tmp
                + f'@{index}\n'
                + 'A=D+A\n'
                )
        return output

    # Error happend after getIndex
    # Because getIndex() return addr in A-register and i write 'D=M/n'
    def popfunc(self, segment, index):
        output = None
        if segment == 'temp':
            output = (self.getIndex(5, index)
                    + 'D=A\n'
                    + '@R13\n'
                    + 'M=D\n' # addr of temp in @R13
                    + self.take_one_arg 
                    + 'D=M\n' # data in D-register
                    + '@R13\n'
                    + 'A=M\n' # addr of temp in A-register
                    + 'M=D\n'
            )
        elif segment == 'static':
            output = (self.take_one_arg
                    + 'D=M\n' # data in D-register
                    + f'@{self.name[-1]}.{index}\n' #addr in A-register
                    + 'M=D\n'
            )
        else: # segment == local | argument | this | that | pointer
            if(segment == 'pointer'):
                # Error because judge index like integer not string
                segment = 'THIS' if index == '0' else 'THAT'
                output = (self.getIndex(segment, 0)
                        + 'D=A\n'
                        + '@R13\n'
                        + 'M=D\n' # addr of pointer in @R13
                        + self.take_one_arg 
                        + 'D=M\n' # data in D-register
                        + '@R13\n'
                        + 'A=M\n' # addr of temp in A-register
                        + 'M=D\n'
                        )
            else:
                # Error because using 'local' 'argument' directly
                if segment == 'local':
                    segment = 'LCL'
                elif segment == 'argument':
                    segment = 'ARG'
                output = (self.getIndex(segment.upper(), index, True)
                        + 'D=A\n'
                        + '@R13\n'
                        + 'M=D\n' # addr heap in @R13
                        + self.take_one_arg 
                        + 'D=M\n' # data in D-register
                        + '@R13\n'
                        + 'A=M\n' # addr of temp in A-register
                        + 'M=D\n'
                )
        return output

    def pushfunc(self, segment, index):
        output = None
        #  push D-register to stack
        pusharg = ('@SP\n'
                    + 'A=M\n'
                    + 'M=D\n'
                )
        if segment == 'constant':
            output = (f'@{index}\n' # set constant number to D-register
                    + 'D=A\n'
                    # + pusharg
                    # + self.stack_pointer_inc
                )
        elif segment == 'temp':
            output = (self.getIndex(5, index)
                    + 'D=M\n'
                    # + pusharg
                    # + self.stack_pointer_inc
                )
        elif segment == 'static':
            output = (f'@{self.name[-1]}.{index}\n'
                    +  'D=M\n'
                    # + pusharg
                    # + self.stack_pointer_inc
                    )
        else: # segment == local | argument | this | that | pointer
            if(segment == 'pointer'):
                segment = 'THIS' if index == '0' else 'THAT'
                output = (self.getIndex(segment, 0)
                        + 'D=M\n'
                        # + pusharg
                        # + self.stack_pointer_inc
                )
            else:
                if segment == 'local':
                    segment = 'LCL'
                elif segment == 'argument':
                    segment = 'ARG'
                output = (self.getIndex(segment.upper(), index, True) # get address of statement which saved in heap
                        + 'D=M\n' # take data in stack/heap to D-register
                        # + pusharg
                        # + self.stack_pointer_inc
                        )
        output += pusharg + self.stack_pointer_inc
        return output

    def Close(self):
        self.file.close()