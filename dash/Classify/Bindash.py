#! /usr/bin/env python3

import os, sys
import subprocess


class Bindash:

    def sketch_file(filename):
        bindash_path = '/home/unhTW/share/mcbs913_2019/hash_group/bindash/release/bindash'
        threads = '24'
        kmer = '31'
        abs_file = os.path.abspath(filename)
        outname = abs_file + '.sketch'
        path, base_file,  = os.path.split(abs_file)
        out = subprocess.run('{} sketch --outfname={} --nthreads={} --kmerlen={} {}'.format(bindash_path, outname, threads, kmer, abs_file), shell=True, stdout=subprocess.PIPE)
        return outname

    def run_bindash(query, subject):
        bindash_path = '/home/unhTW/share/mcbs913_2019/hash_group/bindash/release/bindash'
        distance_lookup = {}
        threads = '24'
        out = subprocess.run('{} dist {} {} --nthreads={}'.format(bindash_path, query, subject, threads), shell=True, stdout=subprocess.PIPE)
        return out.stdout.decode('ascii')

    def sketch_database(directory):
        bindash_path = '/home/unhTW/share/mcbs913_2019/hash_group/bindash/release/bindash'
        threads = 24
        directory_path = os.path.abspath(directory)
        skecthed = 0
        already_sketched = 0
        # change this to path.join and os.scandir
        for file in [directory_path + '/' + x for x in os.listdir(directory_path)]:
            if not file +'.sketch' in [directory_path + '/' + x for x in os.listdir(directory_path)]:
                if 'sketch' not in file:
                    if not file.endswith('.hll'):
                        sketched += 1
                        print('sketching', file)
                        threads = '24'
                        kmer = '31'
                        abs_file = os.path.abspath(file)
                        outname = abs_file + '.sketch'
                        path, base_file, = os.path.split(abs_file)
                        out = subprocess.run('{} sketch --outfname={} --nthreads={} --kmerlen={} {}'.format(bindash_path, outname,
                                                                                                           threads, kmer, abs_file), shell=True, stdout=subprocess.PIPE)
        print ('Sketched', skecthed, 'files')

if __name__ == '__main__':
    print ('Start')
    Bindash.sketch_database(sys.argv[2])
    out = Bindash.sketch_file(sys.argv[1])
    print (out)
    for file in [sys.argv[2] + '/' + x for x in os.listdir(sys.argv[2]) if x.endswith('.sketch')]:
        out = Bindash.run_bindash(sys.argv[1] +'.sketch', file)
        print (out)