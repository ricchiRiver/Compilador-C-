import lex as lexer
import re

tokens = (
    'ELSE', 'IF', 'RETURN', 'WHILE', 'INT', 'VOID', 
    'ID', 'NUM',
    'RELOP',                #atributos <=, <, >, >=, ==, !=
    'SOMA',                 #atributos +, -
    'MULT',                 #atributos *, /
    'VIRG', 'PVIRG', 
    'LPAREN', 'RPAREN',                            
    'LCOLCH', 'RCOLCH',             
    'LCHAVE', 'RCHAVE',               
    'COMEN' 
)

reservados = {
   'else' : 'ELSE',
   'if' : 'IF',
   'return' : 'RETURN',
   'while' : 'WHILE',
   'int' : 'INT',
   'void' : 'VOID'
}

TS = {

}

def t_ID(t):
    r'[a-zA-Z]+'
    t.type = reservados.get(t.value,'ID')
    t.value = (t.value, symbol_lookup(t.value))
    return t
    
def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_RELOP(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SOMA(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_MULT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMEN(t):
    r'\d+'
    t.value = int(t.value)  
    return t

t_VIRG      = r','
t_PVIRG     = r';'
t_LPAREN    = r'('
t_RPAREN    = r')'
t_LCOLCH    = r'['
t_RCOLCH    = r']'
t_LCHAVE    = r'{'
t_RCHAVE    = r'}'

def main():
    while True:
        tok = lexer.token()
        for tok in lexer:
            print(tok)

TS["x"] = ("x", "ID")
print(TS.get("x")[0])