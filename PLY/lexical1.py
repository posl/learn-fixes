import ply.lex as lex

reserved = {
    "main"      : "MAIN",
    "return"    : "RETURN",
    "break"     : "BREAK",
    "case"      : "CASE",
    "continue"  : "CONTINUE",
    "default"   : "DEFAULT",
    "do"        : "DO",
    "else"      : "ELSE",
    "for"       : "FOR",
    "if"        : "IF",
    "switch"    : "SWITCH",
    "while"     : "WHILE"
}

# List of token names. This is always required
tokens = [
    "STRING",
    "VAR",
    "TYPE",
    "METHOD",
    "INT",
    "OPERATOR",
    "LPAREN",
    "RPAREN",
    "COMMA",
    "SEMICOLON",
    "INCLUDE",
    "HEADER",
    "COMMENT",
    "CHAR"
] + list( reserved.values() )

# Regular expression rules for simple tokens
t_OPERATOR  = r'[\+\-\*/\=&%]'
t_LPAREN    = r'[\(\{\[<]'
t_RPAREN    = r'[\)\}\]>]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_INT       = r'\d+'
t_STRING    = r'\".*\"'
t_CHAR      = r'\'.*\''
t_INCLUDE   = r'\#include'
t_HEADER    = r'<.+\.h\s*>'
t_COMMENT   = r'/\*.*\*/|//.*\n'

# A regular expression rule with some action code
def t_TYPE( t ):
    r'char|short|int|long|float|double|const|unsigned|void'
    return t

def t_METHOD( t ):
    r'fclose|fgets|fopen|fprintf|fputs|fscanf|getc|getchar|gets|printf|putc|putchar|puts|scanf'
    return t

def t_VAR( t ):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get( t.value, 'VAR' )    # 予約語のチェック
    return t

# Define a rule so we can track line numbers
def t_newline( t ):
    r'\n+'
    t.lexer.lineno += len( t.value )

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error( t ):
    print( "Illegal character '%s'" % t.value[ 0 ] )
    t.lexer.skip( 1 )
    # ほんとはスキップしたらまずいけど

# Build the lexer
lexer = lex.lex()

# Test it out
data = r'''

>>20171025231942-61280

#include <stdio.h>
int main(int argc, const char * argc[])
{
  int a;
  a = 'A';
  printf("%c\n" , a);
  return 0;}


>>20171026094919-74102

#include <stdio.h>
int main(int argc, const char * argv[])
{
 int a;

 a = A;
 printf("%d", &a);

 return 0;
 }


>>20171102090729-114189

#include <stdio.h>
int main(int argc, const char * argv[])
{
  int a;

  a ='A';
  printf("%c\n", a);

  return 0;
}


>>20171020160358-58669

#include <stdio.h>
int main(int argc, const char * argv[])
{
     char a;

     a = 'A';
     printf("%c \n", a);

     return 0;
}


>>20171102101625-127779

#include<stdio.h>
int main()
{
  char a;
  a='A';
  printf("%c\n",a);

  return 0;
}






>>20171102091711-116733

#include <stdio.h>
int main(int argc, const char * argv[])
{
  int a,A;
  a=A
    printf("%d/n",A);
  return 0;


>>20171030013531-57428

#include <stdio.h>

int main(int argc, const char * argv[])
{
  char a;

  printf("好きな文字を入力してください：");
  scanf("%c",&a);
  printf("あなたが入力した文字は：%c\n", a);

  return 0;

}


>>20171019095744-117955

#include <stdio.h>
int main(int argc, const char * argv[])
{
  char a;

  a = 'A';
  printf("%c\n", a);
  return 0;
}


>>20171020153256-56112

#include <stdio.h>
int main(int argc, const char * argv[])
{
  char a;

  a = 'A'
    printf("%c\n", a);

  return 0;



>>20171026100909-79123

#include <stdio.h>
int main(int argc, const char * argv[])
{
  char a;

  a='A'
    printf("%c" , a );

  return 0;
}

'''

# Give the lexer some input
lexer.input( data )

# Tokenize
tokenized = ""
m_lis, v_lis, s_lis, c_lis, i_lis, f_lis, t_lis = [], [], [], [], [], [], []
while True:
    tok = lexer.token()
    if not tok: # No more input
        break
    kind = tok.type
    code = tok.value
    if kind == "METHOD":
        if code not in m_lis:
            m_lis.append( code )
        tokenized += "METHOD_" + str( m_lis.index( code ) + 1 )
    elif kind == "VAR":
        if code not in v_lis:
            v_lis.append( code )
        tokenized += "VAR_" + str( v_lis.index( code ) + 1 )
    elif kind == "STRING":
        if code not in s_lis:
            s_lis.append( code )
        tokenized += "STRING_" + str( s_lis.index( code ) + 1 )
    elif kind == "CHAR":
        if code not in c_lis:
            c_lis.append( code )
        tokenized += "CHAR_" + str( c_lis.index( code ) + 1 )
    elif kind == "INT":
        if code not in i_lis:
            i_lis.append( code )
        tokenized += "INT_" + str( i_lis.index( code ) + 1 )
    elif kind == "FLOAT":
        if code not in f_lis:
            f_lis.append( code )
        tokenized += "FLOAT_" + str( f_lis.index( code ) + 1 )
    elif kind == "TYPE":
        if code not in t_lis:
            t_lis.append( code )
        tokenized += "TYPE_" + str( t_lis.index( code ) + 1 )
    elif kind == "COMMENT":
        tokenized += "COMMENT"
    else:
        tokenized += str( tok.value )
    tokenized += " "

print( tokenized )
