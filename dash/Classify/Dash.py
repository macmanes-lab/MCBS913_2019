#! /usr/bin/env python3

import os
import subprocess


class Dash:

    def sketch_file(filename):
        dashing_path = '/home/unhTW/share/mcbs913_2019/hash_group/dashing/dashing'
        abs_file = os.path.abspath(filename)
        path, base_file,  = os.path.split(abs_file)
        subprocess.run('{} sketch {} -c {}'.format(dashing_path, abs_file, path), shell=True, stdout=subprocess.PIPE)
        outname = filename + '.w.31.spacing.10.hll'
        return outname

    def run_dashing(query, subject):
        dashing_path = '/home/unhTW/share/mcbs913_2019/hash_group/dashing/dashing'
        distance_lookup = {}
        out = subprocess.run('{} dist {} {} -W'.format(dashing_path, query, subject), shell=True, stdout=subprocess.PIPE)
        return out.stdout.decode('ascii')

    def sketch_database(directory):
        dashing_path = '/home/unhTW/share/mcbs913_2019/hash_group/dashing/dashing'
        threads = 24
        directory_path = os.path.abspath(directory)
        file_list = 'dashing_database_paths.txt'
        genome_list = open(file_list, 'w')
        # change this to path.join and os.scandir
        for file in [directory_path + '/' + x for x in os.listdir(directory_path) if not x.endswith('hll')]:
            genome_list.writelines(file + '\n')
        genome_list.close()
        out = subprocess.run('{} sketch -p {} -c {} -F {} '.format(dashing_path, threads, directory, file_list), shell=True, stdout=subprocess.PIPE)
        #print (out.stdout.decode('ascii'))


if __name__ == '__main__':
    sketch_database(args.database)
