#!/usr/bin/python3
import os
import itertools
import operator

import matplotlib.pyplot as plt # for plotting graphs
import numpy as np # for array maths
import pandas as pd  # for pandas dataframe creation and simplified data manipulation

import kmers  # for creating dict of all represented k-mers in a given sequence of length i-j, calculating GC content

from Bio import SeqIO  # for parsing of biological sequence data from standard file types(i.e., fastQ files)
from collections import OrderedDict
from dna2vec.multi_k_model import MultiKModel # for vectorizing sequence reads

from sklearn import svm # for creating our SVM classifier
from sklearn.model_selection import train_test_split # for splitting data into training and data sets
from sklearn.metrics import accuracy_score, confusion_matrix # for performance metrics and generation of confusion matrices
from sklearn.feature_extraction import DictVectorizer # for vectorizing k-mer frequency dictionaries
from sklearn.utils.multiclass import unique_labels # for labeling figures

from tqdm import tqdm # for monitoring progress during data processing

#Global variable declarations
species_dict =  {'ab250_4k.fq': 'A. bacterium', 'bp250_4k.fq': 'B. pumilis', 'bs250_4k.fq': 'B. subtilis',
                 'cb250_4k.fq': 'C. botulinum', 'eclo250_4k.fq': 'E.cloacae', 'ecoi250_4k.fq': 'E. coli',
                 'ef250_4k.fq': 'E. faecalis', 'fh250_4k.fq': 'F. hominis', 'gs250_4k.fq': 'G. sunshinyii',
                 'hq250_4k.fq': 'H. quentini', 'ih250_4k.fq': 'I. halophila', 'kp250_4k.fq': 'K. pseudosacchari',
                 'lf250_4k.fq': 'L. fermentum', 'lm250_4k.fq': 'L. monocytogenes', 'ml250_4k.fq': 'M. luteus',
                 'nb250_4k.fq': 'N. basaltis', 'pe250_4k.fq': 'P. equi', 'rp250_4k.fq': 'R. pickettii',
                 'sa250_4k.fq': 'S. aureus', 'se250_4k.fq': 'S. enterica', 'sepi250_4k.fq': 'S. epidermidis',
                 'va250_4k.fq': 'V. albensis', 'wc250_4k.fq': 'W. ceti', 'xb250_4k.fq': 'X. bromi',
                 'yp250_4k.fq': 'Y. pestis'}

tax_dict = {'A. bacterium': 0, 'B. pumilis': 1, 'B. subtilis': 2, 'C. botulinum': 3, 'E.cloacae': 4,
            'E. coli': 5, 'E. faecalis': 6, 'F. hominis': 7, 'G. sunshinyii': 8, 'H. quentini': 9,
            'I. halophila': 10, 'K. pseudosacchari': 11, 'L. fermentum': 12, 'L. monocytogenes': 13, 'M. luteus': 14,
            'N. basaltis': 15, 'P. equi': 16, 'R. pickettii': 17, 'S. aureus': 18 ,'S. enterica': 19,
            'S. epidermidis': 20, 'V. albensis': 21, 'W. ceti': 22, 'X. bromi': 23, 'Y. pestis': 24}

class_names = np.array(['A. bacterium','B. pumilis','B. subtilis','C. botulinum','E.cloacae','E. coli','E. faecalis','F. hominis','G. sunshinyii','H. quentini',
                        'I. halophila','K. pseudosacchari','L. fermentum','L. monocytogenes','M. luteus','N. basaltis','P. equi','R. pickettii','S. aureus',
                        'S. enterica', 'S. epidermidis', 'V. albensis', 'W. ceti','X. bromi','Y. pestis'])

gen_path = "./read_data/"

# Instantiate dictionary vectorizer object
dv = DictVectorizer()

data = []

# Import and process read data from fastQ files
i = 0
for fastq_file in os.listdir(gen_path):
    if fastq_file.endswith('.fq'):
        i += 1
        for seq_record in tqdm(SeqIO.parse(gen_path+fastq_file, 'fastq'), desc='Processing File (' + str(i)+') | ' + fastq_file, unit=' Reads processed'):
            read_id = seq_record.id
            read_seq = str(seq_record.seq)
            # Calc GC Content
            gc_content = kmers.gc_content(read_seq)
            # Perform dna2vec on read
            vectorized_read = np.zeros(100, dtype='float')
            for kmer in kmers.generate_kmers(seq_record.seq,5):
                vectorized_read = np.add(vectorized_read, kmers.generateEmbeddingFeatures(str(kmer)))
            # Calculate k-mer frequency
            total_kmerfreq = {}
            kmers.kmer_frequency(read_seq, 3, 8, total_kmerfreq)
            total_kmerfreq = OrderedDict(sorted(total_kmerfreq.items(), key=operator.itemgetter(1), reverse=True))
            total_kmerfreq = itertools.islice(total_kmerfreq.items(), 10)
            kmer_freq_extracted_features = dict()
            for iter in total_kmerfreq:
                kmer_freq_extracted_features[iter[0]] = iter[1]
            # Vectorize k-mer dictionary
            vectorized_dict = dv.fit_transform(kmer_freq_extracted_features).toarray()
            # Add taxonomic identifiers
            vectorized_read = np.append(vectorized_read, gc_content)
            vectorized_read = np.append(vectorized_read, vectorized_dict)
            species = species_dict.get(fastq_file)
            tax_id = tax_dict.get(species)
            data.append({'Vectorized Read Data':vectorized_read,'Taxonomic ID':tax_id})
df = pd.DataFrame(data) # create pandas dataframe with read and taxonomic identifier information

X = df['Vectorized Read Data'].tolist() # create list from dataframe with read data for training
Y = df['Taxonomic ID'].tolist() # create list from dataframe with taxonomic id (label) data


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0) # separate test data into training and test sets
print("Begin training SVM...")
clf = svm.SVC(gamma='scale', decision_function_shape='ovo') # create SVM classifier

y_pred = clf.fit(x_train, y_train).predict(x_test) # Train SVM

print("Accuracy score:", accuracy_score(y_test, y_pred))

#create and save confusion matrices
def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
   # fmt = '.2f' if normalize else 'd'
   # thresh = cm.max() / 2.
   # for i in range(cm.shape[0]):
   #     for j in range(cm.shape[1]):
   #         ax.text(j, i, format(cm[i, j], fmt),
   #                 ha="center", va="center",
   #                 color="white" if cm[i, j] > thresh else "black")
   # fig.tight_layout()
    return ax

np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=class_names,
                      title='Confusion matrix, without normalization')

plt.savefig('non_normalized_svm_confusion_matrix.png')

# Plot normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.savefig('normalized_svm_confusion_matrix.png')
