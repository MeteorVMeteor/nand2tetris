class CodeWriter:
    #use in add, sub, and, or operation
    take_two_arg = ('@SP\n' 
                    + 'AM=M-1\n' #first operator(M[M[SP]-1]) and stackpointer -= 1
                    + 'D=M\n' #take first operator in D
                    + 'A=A-1\n' #second operator(M[A]) and stackpointer nochange
                    )
    #use in neg, not, pop operation
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
        self.judge_name = 0
    
    def setFileName(self, name):
        self.name = name
        filename = f'{self.addr}\{name}.asm'
        self.file = open(filename, 'w')

    def apply(self, cmdtype, arg1, arg2):
        if cmdtype == 'C_ARITHMETIC':
            self.writeArithmetic(arg1)
        elif cmdtype == 'C_PUSH' or cmdtype == 'C_POP':
            self.writePushPop(cmdtype, arg1, arg2)
        self.file.write(self.output)

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
                + f'@STATEMENT{self.judge_name}\n'
                + f'D;{c_command}\n'
                
                + '@SP\n' #if false
                + 'A=M-1\n'
                + 'M=0\n'
                + f'@CONTINUE{self.judge_name}\n'
                + '0;JMP\n'

                + f'(STATEMENT{self.judge_name})\n' #if true
                + '@SP\n'
                + 'A=M-1\n'
                + 'M=-1\n'

                + f'(CONTINUE{self.judge_name})\n'
                )
        self.judge_name += 1
        return output

    def writePushPop(self, command, segment, index):
        if command == 'C_PUSH':
            self.output = self.pushfunc(segment, index)
        elif command == 'C_POP':
            self.output = self.popfunc(segment, index)

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
                    + f'@{self.name}.{index}\n' #addr in A-register
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
            output = (f'@{self.name}.{index}\n'
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