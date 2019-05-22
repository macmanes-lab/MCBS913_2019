# Created by poojaoza

import os.path
import csv
import operator
import itertools

import constants

import numpy as np
import pandas as pd

from collections import OrderedDict

from Bio import SeqIO
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA

from dna2vec.dna2vec.multi_k_model import MultiKModel
from Model.randomForestClassifier import randomForest
from Model.randomForestClassifier import predictRandomForest


dir_path = os.path.dirname(os.path.realpath(__file__))
par_path = os.path.abspath(os.path.join(dir_path, os.pardir))
filepath = par_path+'/dna2vec/pretrained/dna2vec-20161219-0153-k3to8-100d-10c-29320Mbp-sliding-Xat.w2v'
mk_model = MultiKModel(filepath)


def readtaxonomy():
    with open(par_path+'/tax_encoding.csv') as coding_csv:
        coding_csv_reader = csv.reader(coding_csv, delimiter=',')
        next(coding_csv_reader)
        counter = 1
        taxonomy_code = {}
        for row in coding_csv_reader:
            print(row[14])
            taxonomy_code[counter] = row[14]
            counter += 1
    return taxonomy_code


def generatekmers(sequence, length):
    for kmer in range(0, len(sequence)-length):
        yield str(sequence[kmer:kmer+length])


def generateEmbeddingFeatures(kmer):
    return mk_model.vector(kmer)


def predictResponse(x_train_1, x_test_1, y_train_1, y_test_1):
    randomForest(x_train_1, x_test_1, y_train_1, y_test_1)


def calc_gc_content(dna_seq):
    g_content = dna_seq.upper().count('G')
    c_content = dna_seq.upper().count('C')
    return (g_content + c_content)/ len(dna_seq)


# the kmers are generated based on the length given
# For example, if the sequence is AAACCCC and the given length is 3 then the kmers generated are
# AAA, AAC, ACC, CCC
def existingKmerFrequency(sequence, start, end, data):
    for counter in range(start, end + 1):
        for kmer in generatekmers(sequence, counter):
            #print(kmer)
            if kmer in data:
                data[kmer] = data[kmer] + 1

    return data


def kmerFrequency(sequence, start, end, data):
    for counter in range(start, end + 1):
        for kmer in generatekmers(sequence, counter):
            #print(kmer)
            if kmer in data:
                data[kmer] = data[kmer] + 1
            else:
                data[kmer] = 1

    return data


def readinputfile(input_file, train_model):
    #The method reads the input fq files, generates features, and call randomForest

    tax_code = readtaxonomy()
    print(tax_code)

    v = DictVectorizer()
    final_feature_vector = []

    total_kmerfreq = {}
    number_of_features = 0
    print("constants.KMER_LEN_START : ", constants.KMER_LEN_START)
    for in_file in input_file:
        with open(in_file, "rU") as input_handle:
            print("Processing file : ", in_file)
            counter = 0
            for record in SeqIO.parse(input_handle, "fastq"):
                # Retrieve all the kmers of the given length from all the species
                total_kmerfreq = kmerFrequency(record.seq, constants.KMER_LEN_START, constants.KMER_LEN_END, total_kmerfreq)
                counter = counter + 1
                # print(counter)
            print(counter)

    print(len(total_kmerfreq))
    total_kmerfreq = OrderedDict(sorted(total_kmerfreq.items(), key=operator.itemgetter(1), reverse=True))
    total_kmerfreq = itertools.islice(total_kmerfreq.items(), 20) #Select only top 20 most frequently occuring kmers in all species
    kmer_freq_extracted_features = dict()
    kmer_freq_extracted_features_counter = 1

    #Implementation of sliding window
    for iter in total_kmerfreq:
        if kmer_freq_extracted_features_counter >= 11:
            kmer_freq_extracted_features[iter[0]] = 0
        kmer_freq_extracted_features_counter += 1

    print(type(total_kmerfreq))

    for file in input_file:
        print("Processing file : ", file)
        species_str = file.split('/')[-1].split('_')[-1].split('.')[0][:2]

        with open(file, "rU") as handle:
            line_counter = 1
            for record in SeqIO.parse(handle, "fastq"):

                kmerfreq = dict.fromkeys(kmer_freq_extracted_features.keys(), 0)

                dna2vec_feature = np.zeros(100, dtype='float')

                #generate kmers of the given read sequence
                kmerfreq = existingKmerFrequency(record.seq, constants.KMER_LEN_START, constants.KMER_LEN_END, kmerfreq)

                #get the dna2vec values for the 5-length kmers
                for kmer_5 in generatekmers(record.seq, 5):
                    dna2vec_feature = np.add(dna2vec_feature, generateEmbeddingFeatures(kmer_5))

                #convert the dictionary of freuently occuring kmers to np array
                feature_vector = v.fit_transform(kmerfreq).toarray()
                feature_vector_data = feature_vector.data

                for f in dna2vec_feature:
                    feature_vector = np.append(feature_vector, f)

                category_class = constants.TAX_SPECIES_MAP[species_str]

                gc_content = calc_gc_content(record.seq)
                feature_vector = np.append(feature_vector, gc_content)

                feature_vector = np.append(feature_vector, category_class) # the response y

                final_feature_vector.append(feature_vector.tolist())
                line_counter += 1

        print("After finishing the kmer frequency : ", len(final_feature_vector))
        number_of_features = len(feature_vector)

    df = pd.DataFrame(final_feature_vector)
    if df.isnull().values.any():
        print("Null present in df")

    #create dataframes of features and response
    train_x1 = df.iloc[:, 0:number_of_features-2]
    train_y1 = df.iloc[:, number_of_features - 1]
    print("number of features : ", number_of_features)

    if np.isnan(train_x1).any().any():
        print("Null present in the training features")
        exit(-1)
    if np.isnan(train_y1).any().any():
        print("Null present in the training response")
        exit(-1)

    # if the train_model is true then a random forest model will be trained on train data and validated on test data
    # the trained model is saved in "random_forest.sav" file
    # if the train model is not true then the data will given to the model given in user input and the scores will be
    # predicted on the entire data set

    if train_model:
        x_train, x_test, y_train, y_test = train_test_split(train_x1, train_y1, test_size=0.3, random_state=0)
        print("starting random forest:")
        predictResponse(x_train, x_test, y_train, y_test)
    else:
        print("load rf model file : ", constants.RF_MODEL_FILE)
        predictRandomForest(train_x1, train_y1, constants.RF_MODEL_FILE)



