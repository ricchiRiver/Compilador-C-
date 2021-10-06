import lex as lex
import re

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
    'MENIG', 'MEN', 'MAI', 'MAIIG', 'IGIG', 'DIF', 'IG',
    'SOMA', 'SUB', 'MULT', 'DIVIS',
    'VIRG', 'PVIRG', 
    'LPAREN', 'RPAREN',                            
    'LCOLCH', 'RCOLCH',             
    'LCHAVE', 'RCHAVE',               
    'COMEN'
] + list(reservadas.values())

TS = {

}

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
    if t.value not in TS:
        TS[t.value] = int(t.value)
    t.value = (t.value, TS.get(t.value))
    return t

t_ignore = ' \t\n'

def t_COMEN(t):
    r'/\*(.*?)\*/(?s)'
    pass

def t_LINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def coluna(input, token):
    start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - start) + 1

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

t_MENIG     = r'\<\='
t_MEN       = r'\<'
t_MAI       = r'\>'
t_MAIIG     = r'\>\='
t_IGIG      = r'\=\='
t_DIF       = r'\!\='
t_IG        = r'\='

def main():
    lexer = lex.lex()

    data = '''
    
    /* Um programa para ordenação por seleção de
   uma matriz com dez elementos. */

int x[10];

int minloc( int a[], int low, int high ) {
	int i; 
	int x; 
	int k;
	k = low;
	x = a[low];
	i = low + 1;
	while (i < high) {	
		if (a[i] < x) {
			x = a[i];
			k= i;
		}
	i = i + 1;
	}
return k;
}

void sort( int a[], int low, int high ) {
	int i; int k;
	i = low;
	while (i < high-1){
		int t;
		k = minloc(a, i, high);
		t = a[k];
		a[k] = a[i];
		a[i] = t;
		i = i + 1;
	}
}

void main(void){
	int i;
	i = 0;
	while (i < 10){
		x[i] = input();
		i = i + 1;
	}
	sort(x,0,10);
	i= 0;
	while (1 < 10){
		output (x[i]);
		i = i + 1;
	}
}

'''
    lexer.input(data)
    while True:
        tok = lexer.token()
        for tok in lexer:
            print(tok)

main()