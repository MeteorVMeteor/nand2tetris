class Parser:
    arithmetic = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    def __init__(self, addr):
        file = open(addr, 'r')
        self.doc = []
        for line in file:
            line = line.strip('\n')
            self.doc += [line]
        file.close()
        self.index = -1
        self.command = None
        self.type = None

    def hasMoreCommands(self):
        return self.index < len(self.doc)-1

    def advance(self):
        self.index += 1
        self.command = self.doc[self.index].split(' ')
        self.__confirmtype__(self.command[0])
    
    def __confirmtype__(self, firstcommand):
        for i in self.arithmetic:
            if i == firstcommand:
                self.type = 'C_ARITHMETIC'                
        if firstcommand == 'pop':
            self.type = 'C_POP'
        elif firstcommand == 'push':
            self.type = 'C_PUSH'
        elif firstcommand == 'label':
            self.type = 'C_LABEL'
        elif firstcommand == 'goto':
            self.type = 'C_GOTO'
        elif firstcommand == 'if-goto':
            self.type = 'C_IF'
        elif firstcommand == 'function':
            self.type = 'C_FUNCTION'
        elif firstcommand == 'call':
            self.type = 'C_CALL'
        elif firstcommand == 'return':
            self.type = 'C_RETURN'

    def commandType(self):
        return self.type

    def arg1(self):
        assert not self.type == 'C_RETURN'
        if self.type == 'C_ARITHMETIC':
            return self.command[0]
        return self.command[1]

    def arg2(self):
        assert self.type == 'C_PUSH' or self.type == 'C_POP' or self.type == 'C_FUNCTION' or self.type == 'C_CALL'
        return self.command[2]
    