def comp(text):
    dir = { '0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
                'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
                '-A':'0110011', 'D+1':'0011111', 'A+1':'0110111', 'D-1':'0001110', 
                'A-1':'0110010', 'D+A':'0000010', 'D-A':'0010011', 'A-D':'0000111', 
                'D&A':'0000000', 'D|A':'0010101', 'M':'1110000',  '!M':'1110001', 
                '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010', 'D+M':'1000010', 
                'D-M':'1010011', 'M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101' }
    key = get_slice(text, 0)
    return '111' + dir[key]

def dest(text):
    dir = { 'null':'000', 'M':'001', 'D':'010', 'MD':'011',
                'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}
    key = get_slice(text, 1)
    return dir[key]

def jump(text):
    dir = { 'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
    key = get_slice(text, 2)
    return dir[key]

def get_slice(text, num):
    type = -1
    tmp = []
    if '=' in text:
        type = 0
        tmp = text.split('=')
    elif ';' in text:
        type = 1
        tmp = text.split(';')
    if num == 0:
        if type == 0:
            return tmp[1]
        elif type == 1:
            return tmp[0]
    elif num == 1:
        if type == 0:
            return tmp[0]
        elif type == 1:
            return 'null'
    else:
        if type == 0:
            return 'null'
        elif type == 1:
            return tmp[1]