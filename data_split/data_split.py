import sqlite3
import argparse
import random
import os

parser = argparse.ArgumentParser(description='split the dataset into train, eval and test')
parser.add_argument('-d', '--dataset', default='./dataset.db', type=str)
parser.add_argument('-e', '--eval_rate', default=0.10, type=float)
parser.add_argument('-t', '--test_rate', default=0.10, type=float)
parser.add_argument('-o', '--out_dir', default='', type=str)
args = parser.parse_args()

dataset = args.dataset
eval_rate = args.eval_rate
test_rate = args.test_rate
out_dir = args.out_dir

def save_database( which, user_list, out ):
    if not os.path.exists( out+ "/" + which ):
        os.makedirs( out + "/" + which )

    new_db = out + "/" + which + "/" + "dataset.db"

    with sqlite3.connect( new_db ) as new_conn:
        new_cursor = new_conn.cursor()
        new_cursor.execute( 'CREATE TABLE "Code" ( "code_id" TEXT,"user_id" TEXT, "problem_id" TEXT, "code" TEXT, "error" TEXT, "errorcount" INTEGER, PRIMARY KEY("code_id"))' )

        with sqlite3.connect( dataset ) as conn:
            cursor = conn.cursor()

            for user in user_list:
                for line in cursor.execute( 'SELECT * FROM Code WHERE user_id="' + user + '"' ):
                    code_id     = str( line[ 0 ] )
                    user_id     = str( line[ 1 ] )
                    prob_id     = str( line[ 2 ] )
                    code        = str( line[ 3 ] )
                    error       = str( line[ 4 ] )
                    errorcount  = str( line[ 5 ] )

                    # print( code_id, user_id, prob_id, code, error, errorcount )

                    sql_insert = 'INSERT INTO Code( code_id, user_id, problem_id, code, error, errorcount ) values( ?, ?, ?, ?, ?, ? )'
                    new_cursor.execute( sql_insert, [ code_id, user_id, prob_id, code, error, errorcount ] )

            cursor.close()

        new_cursor.close()


with sqlite3.connect( dataset ) as conn:
    cursor = conn.cursor()

    user_list = []
    for line in cursor.execute( "SELECT DISTINCT user_id FROM Code" ):
        user_id = str( line[ 0 ] )
        user_list.append( user_id )

    random.shuffle( user_list )
    datasize = len( user_list )
    index_e = int( datasize * eval_rate )
    index_t = index_e + int( datasize * test_rate )
    eval_list = user_list[ : index_e ]
    test_list = user_list[ index_e : index_t ]
    train_list = user_list[ index_t : ]

    cursor.close()

if not os.path.exists( out_dir ):
    os.makedirs( out_dir )
save_database( "train", train_list, "./" + out_dir )
save_database( "eval", eval_list, "./" + out_dir )
save_database( "test", test_list, "./" + out_dir )