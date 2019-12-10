#!/usr/bin/env python 3

import os,sys
import argparse
import pandas as pd

# This script takes the output of abricate and outputs a binary presence/absence matrix in tab-delimited format

# setup argparser to display help if no arguments
class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# determine command line arguments and get path
parser = ArgParser(description='Convert the results of Abricate to binary presence/absence')
parser.add_argument('tsv', type=str, help="Abricate summary file (tab delimited)")
parser.add_argument('-o', metavar='output', type=str, help="Output directory - defaults to working directory")

args = parser.parse_args()

# get current working dir if output is empty
try:
    out = os.path.abspath(args.o)
except (AttributeError, TypeError) as err:
    out = os.getcwd()

# Ssoptions.display.max_rows = 10
pd.options.display.max_columns = 5

# get max identity for each entry, if any
def identity(val):
    # convert to str
    val = list(map(str, val))
    for i in range(0,len(val)):
      vals = val[i].split(";")

      # if AR gene absent, set to 0
      if len(vals) == 1 and vals[0] == ".":
          val[i] = 0

      # if AR gene(s) present, get max value
      else:
          vals = list(map(float, vals))
          val[i] = max(vals)
    return val

def binary(val):
    for i in range(0,len(val)):
      if val[i] == 0:
          val[i] = 0
      # if AR gene present, set to 1
      else:
          val[i] = 1
    return val

# get path to abricate tsv file
tsvfile = os.path.abspath(args.tsv)

# get abricate tsv file handle
tsvhandle = os.path.basename(tsvfile).split(".")[0] + "_binary.tsv"

# read abricate tsv file to df
tsv = pd.read_csv(tsvfile, sep="\t", header=0)

# set path to output file
binaytsv = os.path.join(out,tsvhandle)

# get identity of each entry in the df
for i in range(2,len(tsv.columns)):
 tsv.iloc[0:len(tsv.index),i] = identity(list(tsv.iloc[0:len(tsv.index), i]))

# convert df to binary
bin_tsv = tsv
for i in range(2,len(bin_tsv.columns)):
    bin_tsv.iloc[0:len(bin_tsv.index),i] = binary(list(bin_tsv.iloc[0:len(bin_tsv.index), i]))

# write binary df to file
bin_tsv.to_csv(binaytsv, sep='\t', encoding='utf-8')
