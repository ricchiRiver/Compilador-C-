import lex as lex
import re
import sys

reservadas = {
   'else' : 'ELSE',
   'if' : 'IF',
   'return' : 'RETURN',
   'while' : 'WHILE',
   'int' : 'INT',
   'void' : 'VOID'
}

tokens = [ 
    'ID', 'NUM',
    'RELOP',
    'SOMA', 'SUB', 'MULT', 'DIVIS',
    'VIRG', 'PVIRG', 
    'LPAREN', 'RPAREN',                            
    'LCOLCH', 'RCOLCH',             
    'LCHAVE', 'RCHAVE',               
    'COMEN'
] + list(reservadas.values())

TS = {
}

erros = [
]

t_VIRG      = r'\,'
t_PVIRG     = r'\;'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCOLCH    = r'\['
t_RCOLCH    = r'\]'
t_LCHAVE    = r'\{'
t_RCHAVE    = r'\}'
t_SOMA      = r'\+'
t_SUB       = r'\-'
t_MULT      = r'\*'
t_DIVIS     = r'\/'

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z]+'
    t.type = reservadas.get(t.value,'ID')
    if(t.type == "ID"):
        if t.value not in TS:
            TS[t.value] = "placeholder"
        t.value = (t.value, TS.get(t.value))
    return t
    
def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_RELOP(t):
    r'\<\=|\<|\>\=|\>|\=|\=\=|\!\='
    if (t.value == '<'):
        t.value = (t.value, 'LT')
    if (t.value == '>'):
        t.value = (t.value, 'GT')
    if (t.value == '='):
        t.value = (t.value, 'EQ')
    if (t.value == '<='):
        t.value = (t.value, 'LE')
    if (t.value == '>='):
        t.value = (t.value, 'GE')
    if (t.value == '=='):
        t.value = (t.value, 'EE')
    if (t.value == '!='):
        t.value = (t.value, 'NE')
    return t

def t_COMEN(t):
    r'/\*(.*?)(?s)\*/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    erros.append((str(t.value[0]), str(t.lexer.lineno)))
    t.lexer.skip(1)

def t_EOF(t):
    r'/\*.*(?s)'
    print("EOF: Comentario nao fechado na linha " + str(t.lexer.lineno))
    t.lexer.skip(1)

def main():
    lexer = lex.lex()

    print("Insira o codigo. Ao terminar, tecle enter, CTRL+Z (Windows) ou CTRL+D (Linux), e enter mais uma vez")
    entrada = sys.stdin.read()
    lexer.input(entrada)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    
    if erros:
        print(str(len(erros)) + " erros achados.")
        for e in erros:
            print("Caractere invalido " + str(e[0]) + " achado na linha " + str(e[1]))

main()