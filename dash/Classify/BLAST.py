#! /usr/bin/env python3

import os, sys, glob
import subprocess


class BLAST:

    def sketch_file(filename): # makes a blast database for a file
        return False

    def blast_file(query, database):
        min_length = 500
        min_identity = 0
        threads = '48'

        return_best = "| head -n 1"#""| awk -F'\t' '$4 > {}' | sort -k1,1 -k12,12nr -k11,11n | sort -u -k1,1 --merge | head -n 1".format(min_length)

        out = subprocess.run('blastn -query {} -db {} -num_threads {} -outfmt 6 -max_target_seqs 1 {}'.format(query, database, threads, return_best), shell=True, stdout=subprocess.PIPE)
        # determine best hit and return only a score and taxid, return False if no scores or too low
        score = 0
        out_line = out.stdout.decode('ascii').rstrip()
        if out_line:
            length = out_line.split('\t')[3]
            if int(length) > min_length:
                score = float(out_line.split('\t')[11]) # 11 = bitscore
        return score, out_line.split('\t')

    def sketch_database(directory):  # makes a blast database for all files, skips ones done
        directory_path = os.path.abspath(directory)
        sketched = 0
        already_sketched = 0
        # change this to path.join and os.scandir

        completed_genomes = []
        for file in [directory_path + '/' + x for x in os.listdir(directory_path)]:
            if file.endswith('.nhr'):
                if file.endswith('00.nhr'):
                    completed_genomes.append(file[:-7])
                else:
                    completed_genomes.append(file[:-4])
        for file in [directory_path + '/' + x for x in os.listdir(directory_path) if x.endswith('fna.gz')]:
            if not file in completed_genomes:
                sketched += 1
                print('Making BLAST db', file)
                abs_file = os.path.abspath(file)
                path, base_file, = os.path.split(abs_file)
                out = subprocess.run('gunzip -c {} | makeblastdb -in - -dbtype nucl -out {} -title {}'.format(abs_file, abs_file, file), shell=True, stdout=subprocess.PIPE)
        print ('Sketched', sketched, 'files')

if __name__ == '__main__':
    BLAST.sketch_database(sys.argv[2])
    for file in [sys.argv[2] + x for x in os.listdir(sys.argv[2]) if x.endswith('fna.gz')]:
        score = BLAST.blast_file(sys.argv[1], file)
        print (file, score)