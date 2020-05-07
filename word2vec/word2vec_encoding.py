#!/usr/bin/env python
# coding: utf-8

import re
import numpy as np
import pandas as pd
from Bio import SeqIO
import gensim
import os
import json



# read fasta as dict
def read_fasta(fasta_name):
    r = {}
    for record in SeqIO.parse(fasta_name, 'fasta'):
        idtag = str(record.id)
        seq = str(record.seq)
        r[idtag] = seq
    return r

# sequence padding (token:'X')
def padding_seq(r,length=200,pad_value='X'):
    data={}
    for key, value in r.items():
        if len(r[key]) > length:
            print('squence length over padding length ')
            break
        elif len(r[key]) <= length:
            r[key] = [r[key]+pad_value*(length-len(r[key]))]

        data[key] = r[key]
    return data


# word2vec
def word2vec_encode_table():
    root=os.path.dirname(__file__)
    path=root+'/../model/word2vec.model'
    model = gensim.models.Word2Vec.load(path)
    alphabet = 'ACDEFGHIKLMNPQRSTVWY'
    table = {}
    for key in alphabet:
        table[key] = list(model.wv[key].astype('float64'))
    table['X'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return table


# encoding
def encoding(data):
    #method = integer or onehot
    dat={}
    for  key in data.keys():
        integer_encoded = []
        for amino in list(data[key][0]):
            integer_encoded.append(word2vec_encode_table()[amino])
        dat[key]=integer_encoded
    return dat


# word2vec encoding (input: fasta)
def word2vec_encoding(fasta_name, length=200):
    r = read_fasta(fasta_name)
    data = padding_seq(r, length)
    dat = encoding(data)
    return dat
 