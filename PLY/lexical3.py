import ply.lex as lex
import sqlite3
import argparse
import csv

parser = argparse.ArgumentParser(description='generate dataset for learn-fixes')
parser.add_argument('-d', '--dataset', default='./dataset.db', type=str)
args = parser.parse_args()

dataset = args.dataset

cor_code = []
err_code = []
code_list = []

with sqlite3.connect( dataset ) as conn:
    cursor = conn.cursor()

    pre_code_id     = None
    pre_user_id     = None
    pre_prob_id     = None
    pre_code        = None
    pre_errorcount  = 0

    for row in cursor.execute( "SELECT DISTINCT code_id, user_id, problem_id, code, errorcount FROM Code ORDER BY user_id ASC, problem_id ASC, code_id ASC;" ):
        if row[ 0 ] and row[ 1 ] and row[ 2 ] and row[ 3 ]:
            code_id     = str( row[ 0 ] )
            user_id     = str( row[ 1 ] )
            prob_id     = str( row[ 2 ] )
            code        = str( row[ 3 ] )
            errorcount  = int( row[ 4 ] )

            if pre_user_id == user_id and pre_prob_id == prob_id and pre_errorcount > 0 and errorcount == 0:
                cor_code.append( ( code_id, code ) )
                err_code.append( ( pre_code_id, pre_code ) )

            pre_code_id     = code_id
            pre_user_id     = user_id
            pre_prob_id     = prob_id
            pre_code        = code
            pre_errorcount  = errorcount

    cursor.close()

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
    "FLOAT",
    "OPERATOR",
    "LPAREN",
    "RPAREN",
    "COMMA",
    "SEMICOLON",
    "INCLUDE",
    "DEFINE",
    "HEADER",
    "COMMENT",
    "CHAR"
] + list( reserved.values() )

# Regular expression rules for simple tokens
t_OPERATOR  = r'[\+\-\*/\=&%!|:]'
t_LPAREN    = r'[\(\{\[<]'
t_RPAREN    = r'[\)\}\]>]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_INT       = r'\d+'
t_FLOAT     = r'\d+\.\d+'
t_STRING    = r'\".*\"'
t_CHAR      = r'\'.*\''
t_INCLUDE   = r'\#include'
t_DEFINE    = r'\#define'
t_HEADER    = r'<.+\.h\s*>'
t_COMMENT   = r'/\*[\s\S]*?\*/|//.*'

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

me_lis, va_lis, st_lis, ch_lis, in_lis, fl_lis, ty_lis = [], [], [], [], [], [], []

def lex_tokenize( data ):
    # Build the lexer
    lexer = lex.lex()

    # Give the lexer some input
    lexer.input( data )

    # Tokenize
    tokenized = ""
    global m_lis, v_lis, s_lis, c_lis, i_lis, f_lis, ty_lis
    while True:
        tok = lexer.token()
        if not tok: # No more input
            break
        kind = tok.type
        code = tok.value
        if kind == "METHOD":
            if code not in me_lis:
                me_lis.append( code )
            tokenized += "METHOD_" + str( me_lis.index( code ) + 1 )
        elif kind == "VAR":
            if code not in va_lis:
                va_lis.append( code )
            tokenized += "VAR_" + str( va_lis.index( code ) + 1 )
        elif kind == "STRING":
            if code not in st_lis:
                st_lis.append( code )
            tokenized += "STRING_" + str( st_lis.index( code ) + 1 )
        elif kind == "CHAR":
            if code not in ch_lis:
                ch_lis.append( code )
            tokenized += "CHAR_" + str( ch_lis.index( code ) + 1 )
        elif kind == "INT":
            if code not in in_lis:
                in_lis.append( code )
            tokenized += "INT_" + str( in_lis.index( code ) + 1 )
        elif kind == "FLOAT":
            if code not in fl_lis:
                fl_lis.append( code )
            tokenized += "FLOAT_" + str( fl_lis.index( code ) + 1 )
        elif kind == "TYPE":
            if code not in ty_lis:
                ty_lis.append( code )
            tokenized += "TYPE_" + str( ty_lis.index( code ) + 1 )
        elif kind == "COMMENT":
            tokenized += "COMMENT"
        else:
            tokenized += str( tok.value )
        tokenized += " "

    return tokenized

cor_tokenized_list = []
err_tokenized_list = []

for raw_code_id, raw_code in cor_code:
    cor_tokenized_code = lex_tokenize( raw_code )
    cor_tokenized_list.append( ( raw_code_id, cor_tokenized_code ) )

for raw_code_id, raw_code in err_code:
    err_tokenized_code = lex_tokenize( raw_code )
    err_tokenized_list.append( ( raw_code_id, err_tokenized_code ) )

with open( "./fixed.txt", "w" ) as f:
    for raw_code_id, cor_tokenized_code in cor_tokenized_list:
        f.write( str( cor_tokenized_code ) + "\n" )

with open( "./buggy.txt", "w" ) as f:
    for raw_code_id, err_tokenized_code in err_tokenized_list:
        f.write( str( err_tokenized_code ) + "\n" )

# i = 0
# with open( "./lex_result_raw.txt", "w" ) as f:
#     for raw_code_id, raw_code in code_list:
#         f.write( str( i ) + str( raw_code ) + "\n" )
#         i += 1
