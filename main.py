import yacc as yacc
import lex as lex
import re
import sys
from termcolor import colored

#-------------------------------------- Lexer

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
    'SOMA', 'MULT',
    'VIRG', 'PVIRG', 
    'LPAREN', 'RPAREN',                            
    'LCOLCH', 'RCOLCH',             
    'LCHAVE', 'RCHAVE',               
    'COMEN', 'EQ'
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
t_EQ        = r'\='

t_ignore = ' \t'

def t_COMEN(t):
    r'/\*(.*?)(?s)\*/'
    pass

def t_EOF(t):
    r'/\*.*(?s)'
    print("EOF: Comentario nao fechado na linha " + str(t.lexer.lineno))
    t.lexer.skip(1)

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

def t_SOMA(t):
    r'\+|-'
    if (t.value == '-'):
        t.value = (t.value, 'SB')
    if (t.value == '+'):
        t.value = (t.value, 'SM')
    return t

def t_MULT(t):
    r'\*|\/'
    if (t.value == '*'):
        t.value = (t.value, 'MT')
    if (t.value == '/'):
        t.value = (t.value, 'DV')
    return t

def t_RELOP(t):
    r'\<\=|\<|\>\=|\>|\=\=|\!\='
    if (t.value == '<'):
        t.value = (t.value, 'LT')
    if (t.value == '>'):
        t.value = (t.value, 'GT')
    if (t.value == '<='):
        t.value = (t.value, 'LE')
    if (t.value == '>='):
        t.value = (t.value, 'GE')
    if (t.value == '=='):
        t.value = (t.value, 'EE')
    if (t.value == '!='):
        t.value = (t.value, 'NE')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    erros.append((str(t.value[0]), str(t.lexer.lineno)))
    t.lexer.skip(1)

#------------------------------------- Parser

class No:
    def __init__(self, tipo, desc = None, filhos = None):
        self.tipo = tipo
        self.desc = desc
        if filhos:
            self.filhos = filhos
        else:
            self.filhos = []

def p_programa(p):
    'programa : declaracaolista'
    p[0] = No("Programa")
    p[0].filhos = p[1]

def p_declaracaolista(p):
    '''declaracaolista : declaracaolista declaracao
                       | declaracao'''
    p[0] = []
    if (len(p) == 3):
        p[1].append(p[2])
        p[0].extend(p[1])
    else:
        p[0].append(p[1])

def p_declaracao(p):
    '''declaracao : vardeclaracao
                  | fundeclaracao'''
    p[0] = p[1]

def p_vardeclaracao_simples(p):
    'vardeclaracao : tipo ID PVIRG'
    TS[(p[2])[0]] = p[1]
    #Substitui valor do lexeme ID na TS para 'tipo'

    p[0] = No("vardec", (p[2])[0])
    #Cria no e coloca na arvore

def p_vardeclaracao_matriz(p):
    'vardeclaracao : tipo ID LCOLCH NUM RCOLCH PVIRG'
    TS[(p[2])[0]] = (p[1], p[4])
    #Substitui valor do lexeme ID na TS para ( 'tipo', 'numero' )

    p[0] = No("matdec", (p[2])[0] + '[' + str(p[4]) + ']')
    #Cria no e coloca na arvore

def p_tipo(p):
    '''tipo : INT
            | VOID'''
    p[0] = p[1]

def p_fundeclaracao(p):
    'fundeclaracao : tipo ID LPAREN params RPAREN compostodecl'
    TS[(p[2])[0]] = p[1]

    p[0] = No("fundec", p[1] + ' ' + (p[2])[0] + "()")
    if p[4]:
        p[0].filhos.append(p[4])
    p[0].filhos.append(p[6])

def p_params_lista(p):
    'params : paramlista'
    p[0] = No("params", filhos = p[1])

def p_params_void(p):
    'params : VOID'
    p[0] = No("params")
    temp = No("VOID")
    p[0].filhos.append(temp)

def p_paramlista(p):
    '''paramlista : paramlista VIRG param
                  | param'''
    p[0] = []
    if (len(p) == 4):
        p[1].append(p[3])
        p[0].extend(p[1])
    else:
        p[0].append(p[1])

def p_param(p):
    '''param : tipo ID
             | tipo ID LCOLCH RCOLCH'''
    if (len(p) == 3):
        TS[(p[2])[0]] = p[1]
        p[0] = No("vardec", (p[2])[0])
    else:
        TS[(p[2])[0]] = (p[1], 0)
        p[0] = No("matdec", (p[2])[0] + "[]")

def p_compostodecl(p):
    'compostodecl : LCHAVE localdeclaracoes statementlista RCHAVE'
    p[0] = No("compostodecl")
    if len(p[2]) != 0:
        temp = No("localdec", filhos = p[2])
        p[0].filhos.append(temp)
    if len(p[3]) != 0:
        temp = No("statements", filhos = p[3])
        p[0].filhos.append(temp)

def p_localdeclaracoes_lista(p):
    'localdeclaracoes : localdeclaracoes vardeclaracao'
    p[1].append(p[2])
    p[0] = p[1]

def p_localdeclaracoes_vazio(p):
    'localdeclaracoes : empty'
    p[0] = []

def p_statementlista_lista(p):
    'statementlista : statementlista statement'
    p[1].append(p[2])
    p[0] = p[1]

def p_statementlista_vazio(p):
    'statementlista : empty'
    p[0] = []

def p_statement(p):
    '''statement : expressaodecl
                 | compostodecl
                 | selecaodecl
                 | iteracaodecl
                 | retornodecl'''
    p[0] = p[1]

def p_expressaodecl(p):
    '''expressaodecl : expressao PVIRG
                     | PVIRG'''
    if (len(p) == 3):
        p[0] = p[1]

def p_selecaodecl(p):
    '''selecaodecl : IF LPAREN expressao RPAREN statement
                   | IF LPAREN expressao RPAREN statement ELSE statement'''
    p[0] = No("IF")
    p[0].filhos.append(p[3])
    p[0].filhos.append(p[5])
    if (len(p) == 8):
        p[0].filhos.append(p[7])

def p_iteracaodecl(p):
    'iteracaodecl : WHILE LPAREN expressao RPAREN statement'
    p[0] = No("WHILE")
    p[0].filhos.append(p[3])
    p[0].filhos.append(p[5])

def p_retornodecl(p):
    '''retornodecl : RETURN PVIRG
                   | RETURN expressao PVIRG'''
    p[0] = No("RETURN")
    if (len(p) == 4):
        p[0].filhos.append(p[2])

def p_expressao(p):
    '''expressao : var EQ expressao
                 | simplesexpressao'''
    if (len(p) == 4):
        p[0] = No("=")
        p[0].filhos.append(p[1])
        p[0].filhos.append(p[3])
    else:
        p[0] = p[1]

def p_var(p):
    '''var : ID
           | ID LCOLCH expressao RCOLCH'''
    if (len(p) == 2):
        p[0] = No("var", (p[1])[0])
    else:
        p[0] = No("mat", (p[1])[0])
        p[0].filhos.append(No("["))
        p[0].filhos.append(p[3])
        p[0].filhos.append(No("]"))

def p_simplesexpressao(p):
    '''simplesexpressao : somaexpressao RELOP somaexpressao
                        | somaexpressao'''
    if (len(p) == 4):
        p[0] = No((p[2])[0])
        p[0].filhos.append(p[1])
        p[0].filhos.append(p[3])
    else:
        p[0] = p[1]

def p_somaexpressao(p):
    '''somaexpressao : somaexpressao SOMA termo
                     | termo'''
    if (len(p) == 4):
        p[0] = No((p[2])[0])
        p[0].filhos.append(p[1])
        p[0].filhos.append(p[3])
    else:
        p[0] = p[1]

def p_termo(p):
    '''termo : termo MULT fator
             | fator'''
    if (len(p) == 4):
        p[0] = No((p[2])[0])
        p[0].filhos.append(p[1])
        p[0].filhos.append(p[3])
    else:
        p[0] = p[1]

def p_fator_nt(p):
    '''fator : LPAREN expressao RPAREN
             | var
             | ativacao'''
    if (len(p) == 4):
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_fator_num(p):
    'fator : NUM'
    p[0] = No(str(p[1]))

def p_ativacao(p):
    'ativacao : ID LPAREN args RPAREN'
    p[0] = No("fun", TS[(p[1])[0]] + " " + (p[1])[0])
    if p[3]:
        p[0].filhos.append(No("("))
        for a in p[3]:
            p[0].filhos.append(a)
        p[0].filhos.append(No(")"))

def p_args_lista(p):
    'args : arglista'
    p[0] = p[1]

def p_args_vazio(p):
    'args : empty'
    p[0] = None

def p_arglista(p):
    '''arglista : arglista VIRG expressao
                | expressao'''
    p[0] = []
    if (len(p) == 4):
        p[1].append(p[3])
        p[0].extend(p[1])
    else:
        p[0].append(p[1])

def p_vazio(p):
    'empty :'
    pass

def p_error(p):
    if not p:
        print("EOF")
        return
    print(colored("Erro de sintaxe na linha: " + str(p.lineno), 'red'))
    l = []
    x = ""
    while True:
        tok = parser.token()
        if not tok: break
        if type(tok.value) == tuple:
            l.append(str(tok.value[0]))
        else:
            l.append(str(tok.value))
        if tok.type == "PVIRG": break
    for t in l:
        x = x + " " + t
    print(colored(x, 'red'))
    parser.errok()
    return tok

#-------------------------------------EXEC

def VisNo(no, ger = 0):
    if no == None:
        return
    if no.desc:
        print((colored("|", 'green') + "    ") * ger + no.tipo + ", " + no.desc)
    else:
        print((colored("|", 'green') + "    ") * ger + no.tipo)
    if no.filhos:
        for f in no.filhos:
            VisNo(f, ger + 1)

lexer = lex.lex()
TS["input"] = "int"
TS["output"] = "void"
parser = yacc.yacc(errorlog=yacc.NullLogger())

print("Insira o codigo. Ao terminar, tecle enter, CTRL+Z (Windows) ou CTRL+D (Linux), e enter mais uma vez")
entrada = sys.stdin.read()
lexer.input(entrada)

#while True:
#    tok = lexer.token()
#    if not tok:
#        break
#    print(tok)

#if erros:
#    print(str(len(erros)) + " erros achados.")
#    for e in erros:
#        print("Caractere invalido " + str(e[0]) + " achado na linha " + str(e[1]))

result = parser.parse(entrada)
VisNo(result)