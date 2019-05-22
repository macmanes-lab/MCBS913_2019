# Created by poojaoza

import argparse

import constants
from IO import IOFile


# nargs - list of the fastq files
# k - kmerlength for which the top most frequently occuring kmers are calculate
# model - provide a model file to be used for the prediction on data set
# featnum - the number of features to be used in the model

def main():
    print("In main")
    parser = argparse.ArgumentParser()
    parser.add_argument('--nargs', nargs='+', help="<Required> enter the space separated fastaq file names")
    parser.add_argument("-k", "--kmerlen", help="kmer length")
    parser.add_argument("-model", "--modelfile", help="saved model file path")
    parser.add_argument("-featnum", "--featuresnum", help="Number of features")
    args = parser.parse_args()

    print(args.kmerlen)
    print(args.nargs)
    print(args.modelfile)

    print("*********************")
    if args.kmerlen:
        constants.KMER_LEN_START = int(args.kmerlen)
        constants.KMER_LEN_END = int(args.kmerlen)

    if args.modelfile:
        constants.RF_MODEL_FILE = args.modelfile
        IOFile.readinputfile(args.nargs, False)
    else:
        IOFile.readinputfile(args.nargs, True)
    # for _, value in parser.parse_args()._get_kwargs():
    #     if value is not None:
    #         print(value)
    #         print("================")
    #         IOFile.readinputfile(value)


if __name__ == '__main__':
    main()
