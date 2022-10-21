import Parser
def symbol_iter(doc):
    cnt = 0
    codesum = 0
    symtable = {}
    while Parser.hasMoreCommands(cnt, doc):
        text = Parser.advance(cnt, doc)
        type = Parser.commandType(text)
        if not type == 'L':
            codesum += 1
        else: 
            text = text[1:len(text)-1]
            symtable[text] = codesum
        cnt += 1
    return symtable

def symbol(text, symtable, index):
    text = text[1:] #delete '@'
    res = ''
    if text in symtable:
        res = str(bin(symtable[text]))[2:]
    elif text.isdigit():
        res = str(bin(int(text)))[2:]
    else:
        symtable[text] = index + 16
        res = str(bin(index + 16))[2:]
        index += 1
    while len(res) < 16:
        res = '0' + res
    return res, symtable, index