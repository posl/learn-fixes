import argparse
import os

parser = argparse.ArgumentParser(description='make dic from dataset for learn-fixes')
parser.add_argument('-i', '--in_dir', default='./', type=str)
parser.add_argument('-o', '--out_dir', default='./', type=str)
args = parser.parse_args()

in_dir = args.in_dir
out_dir = args.out_dir

buggy_dic = {}
with open( in_dir + "/buggy.txt" ) as f:
    s_list = f.readlines()
    for s in s_list:
        words = s.split()
        for w in words:
            try:
                buggy_dic[ w ] += 1
            except KeyError:
                buggy_dic[ w ] = 1

fixed_dic = {}
with open( in_dir + "/fixed.txt" ) as f:
    s_list = f.readlines()
    for s in s_list:
        words = s.split()
        for w in words:
            try:
                fixed_dic[ w ] += 1
            except KeyError:
                fixed_dic[ w ] = 1

if not os.path.exists( out_dir ):
    os.makedirs( out_dir )

with open( out_dir + "/vocab.buggy.txt", "w" ) as f:
    for k,v in sorted(buggy_dic.items(), key=lambda x: -x[1]):
        # print( str( w ) + "\t" + str( buggy_dic[ w ] ) )
        f.write( str( k ) + "\t" + str( v ) + "\n" )

with open( out_dir + "/vocab.fixed.txt", "w" ) as f:
    for k,v in sorted(fixed_dic.items(), key=lambda x: -x[1]):
        # print( str( w ) + "\t" + str( fixed_dic[ w ] ) )
        f.write( str( k ) + "\t" + str( v ) + "\n" )
