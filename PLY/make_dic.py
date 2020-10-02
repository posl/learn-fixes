s = """

TYPE_1 main ( ) { TYPE_1 VAR_1 , VAR_2 , VAR_3 , VAR_4 ; METHOD_1 ( STRING_1 ) ; METHOD_2 ( STRING_2 , & VAR_4 ) ; for ( VAR_1 = INT_3 ; VAR_1 < = VAR_4 ; VAR_1 + + ) { for ( VAR_2 = INT_3 ; VAR_2 < = VAR_1 ; VAR_2 + + ) { METHOD_1 ( STRING_3 ) ; } return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_5 , VAR_6 , VAR_7 ; METHOD_1 ( STRING_4 ) ; METHOD_2 ( STRING_2 , & VAR_5 ) ; for ( VAR_7 = INT_3 ; VAR_7 < INT_6 ; VAR_7 + + ) { for ( VAR_6 = INT_3 ; VAR_6 < = VAR_7 ; VAR_6 + + ) { METHOD_1 ( STRING_5 ) ; } METHOD_1 ( STRING_6 ) ; } return INT_3 ; }
TYPE_1 main ( TYPE_1 VAR_8 , TYPE_2 TYPE_3 * VAR_9 [ ] ) { TYPE_1 VAR_1 , VAR_2 , VAR_3 , VAR_4 ; METHOD_1 ( STRING_1 ) ; METHOD_2 ( STRING_2 , & VAR_4 ) ; for ( VAR_1 = INT_3 ; VAR_1 < = VAR_4 ; VAR_1 + + ) { for ( VAR_2 = INT_3 ; VAR_2 < = VAR_1 ; VAR_2 + + ) { METHOD_1 ( STRING_7 ) ; } return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_10 ; TYPE_1 VAR_11 ; TYPE_1 VAR_4 ; TYPE_3 VAR_12 = STRING_8 ; TYPE_1 VAR_13 ; METHOD_1 ( STRING_9 ) ; METHOD_2 ( STRING_2 , & VAR_4 ) ; VAR_13 = VAR_4 ; for ( VAR_11 = INT_3 ; VAR_11 < VAR_13 ; VAR_11 + + ) { for ( VAR_10 = INT_3 ; VAR_10 < VAR_4 ; VAR_10 + + ) { METHOD_1 ( STRING_10 , VAR_12 ) ; } METHOD_1 ( STRING_6 ) ; VAR_4 - = INT_11 ; } return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_10 , VAR_14 , VAR_1 ; METHOD_2 ( STRING_2 , & VAR_1 ) ; for ( VAR_10 = INT_11 ; VAR_10 < = VAR_1 ; VAR_10 + + ) { for ( VAR_14 = INT_11 ; VAR_14 < = VAR_10 ; VAR_14 + + ) { METHOD_1 ( STRING_5 ) ; } METHOD_1 ( STRING_6 ) ; } return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_6 , VAR_7 ; for ( VAR_7 = INT_3 ; VAR_7 < INT_6 ; VAR_7 + + ) { for ( VAR_6 = INT_3 ; VAR_6 < = VAR_7 ; VAR_6 + + ) { METHOD_1 ( STRING_11 ) ; } METHOD_1 ( STRING_6 ) ; } return INT_3 ; }
TYPE_1 main ( TYPE_1 VAR_8 , TYPE_2 TYPE_3 * VAR_9 [ ] ) { TYPE_1 VAR_1 , VAR_2 , VAR_3 , VAR_4 ; METHOD_1 ( STRING_1 ) ; METHOD_2 ( STRING_2 , & VAR_4 ) ; for ( VAR_1 = INT_3 ; VAR_1 < = VAR_4 ; VAR_1 + + ) { for ( VAR_2 = INT_3 ; VAR_2 < = VAR_1 ; VAR_2 + + ) { METHOD_1 ( STRING_7 ) ; } return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_10 , VAR_14 ; TYPE_3 & ; METHOD_2 ( STRING_12 ) ; for ( VAR_14 = INT_11 ; VAR_14 < = VAR_10 ; VAR_14 + + ) { METHOD_1 ( STRING_13 , & = VAR_14 ) ; } return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_5 , VAR_10 , VAR_14 ; for ( VAR_10 = INT_11 ; VAR_10 < = VAR_5 ; VAR_10 + + ) { for ( VAR_14 = INT_11 ; VAR_14 < = VAR_10 ; VAR_14 + + ) { METHOD_1 ( STRING_14 ) ; } METHOD_1 ( STRING_6 ) ; } METHOD_2 ( STRING_15 ) ; return INT_3 ; }
TYPE_1 main ( ) { TYPE_1 VAR_12 ; TYPE_1 VAR_4 ; METHOD_1 ( STRING_16 ) ; METHOD_2 ( STRING_2 , & VAR_4 ) ; for ( VAR_12 = INT_3 ; VAR_12 < = VAR_4 ; VAR_12 + + ) { METHOD_1 ( STRING_17 , VAR_12 ) ; } return INT_3 ; }
"""

words = s.split()
dic = {}
for w in words:
    try:
        dic[ w ] += 1
    except KeyError:
        dic[ w ] = 1

for w in dic.keys():
    print( str( w ) + "\t" + str( dic[ w ] ) )