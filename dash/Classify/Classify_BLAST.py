#! python3
import sys, os, glob
import statistics
import argparse
import time
from Bio import SeqIO
from Tree import Tree
from Node import Node
from Dash import Dash
from BLAST import BLAST
#from progress.bar import Bar

#tree = Tree()


full_start = time.time()


# function to retrieve taxonomy information from file names, may change depending on database structure
def tax_from_file(file_name, tax_lookup):
    tax_id = file_name.split('_')[2]
    taxonomy = tax_lookup[tax_id]
    seven_levels = [0, 1, 2, 5, 8, 10, 12, 13]
    seven_levels_taxonomy = [taxonomy.split(';')[x] for x in seven_levels]
    return seven_levels_taxonomy


def fillTaxonomyLookup(tax_path):
    # expected input is, Accession\tKingdom;Phylum;Class;etc
    taxonomy_lookup = {}
    for line in open(tax_path):
        id, taxonomy = line.rstrip().split('\t')
        taxonomy_lookup[id] = taxonomy
    return taxonomy_lookup


def processQuery(query, distance, cur_tree):
    cur_tree.add(query, distance)


# total classify sequence
def classify_sequence(totalNodes):
    totalNodes.pop("_root")
    taxon = ''
    top_score = 0.0
    #k is name in string type, v is node instance
    for k,v in totalNodes.items():
        distanceList = v.getDistance()
        score = max([float(x) for x in distanceList])
        score = statistics.median([float(x) for x in distanceList])
        print(k,score,sorted(distanceList,reverse=True))
        if score > top_score:
            top_score = score
            taxon = k

    return taxon


def classify_sequenceByName(name):
    distanceList = tree.getDistanceByName(name)
    taxon = ''
    top_score = 0.0
    score = max([float(x) for x in distanceList])
    score = statistics.median([float(x) for x in distanceList])
    print(k,score,sorted(distanceList,reverse=True))


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('target', action='store', help='path to query genome to be compared to database')
    parser.add_argument('-database', '-d', action='store', help='path to genome database')
    parser.add_argument('-path_file', '-p', action='store', help='A Text file with the paths to genomes one per line')
    parser.add_argument('-tax_lookup', '-t', action='store', help='Text file with accessions and associated taxonomy',
                        default="/home/unhTW/share/mcbs913_2019/hash_group/documents/expanded_ncbi_taxonomy.tsv")
    parser.add_argument('-divide_input', action='store_true', help='Classify each entry in FAST/Q'
                                                                   ' rather than entire file')
    args = parser.parse_args()
    target_genome_path = os.path.abspath(args.target)

    # Parse taxonomy lookup
    start = time.time()
    print("\nParsing taxonomy database")
    taxonomy_lookup = fillTaxonomyLookup(args.tax_lookup)
    print("Time", time.time() - start)


    # Gather list of input genomes
    directory_path = os.path.abspath(args.database)
    print ('gathering list of input files')
    start = time.time()
    input_genomes = [x for x in os.listdir(directory_path) if x.endswith('.gz')]  # assumes gzipped fastas
    print (len(input_genomes))
    print (input_genomes[0])
    print("Time", time.time() - start)
    start = time.time()
    input_genomes = glob.glob(directory_path+'/'+'*.gz')  # assumes gzipped fastas
    print (len(input_genomes))
    print (input_genomes[0])
    print("Time", time.time() - start)



    # Sketch the input directory
    start = time.time()
    print("\nSketching starting database (this may take some time... unless its been done before)")
    BLAST.sketch_database(args.database)
    print("Time", time.time() - start)


    total_references = len(input_genomes)

    # fill database tree
    start = time.time()
    print("\nPopulating reference tree for filling sparse tree")
    database_tree = Tree()
    for genome_file in input_genomes:
        taxonomy_list = tax_from_file(genome_file, taxonomy_lookup)
        processQuery(taxonomy_list, 1, database_tree)
    print("Time", time.time() - start)

    start = time.time()
    out_file = open('my_distances.txt', 'w')
    if args.divide_input:
        for seq_record in SeqIO.parse(target_genome_path, "fasta"):
            start = time.time()
            cur_tree = Tree()
            # grab sequence information
            header = seq_record.id
            sequence = seq_record.seq

            # Create a tmp file named after the contig
            temp_file = header.split('_')[1] + '.fna'
            file_handle = open(temp_file, 'w')
            file_handle.writelines('>' + header + '\n' + sequence + '\n')
            file_handle.close()

            # iterate through the database and calculate distance with dashing
            print("\nBLASTING contig {} against database with {} total genomes".format(header, total_references))
            directory_path = os.path.abspath(args.database)
            # PYTHON Thread pool



            # Multithread
            completed = 0
            for genome in [directory_path + '/' + x for x in os.listdir(directory_path) if x.endswith('.gz')]:
                completed += 1
                if completed % 100 == 0:
                    print ("Finished BLASTING {} genomes".format(completed))
                name = genome.split('/')[-1]
                distance, best_hit = BLAST.blast_file(temp_file, genome)
                # print (temp_file, genome)
                # print (dist_t)

                # Determine taxonomy data
                reduced_taxonomy = tax_from_file(name, taxonomy_lookup)

                # Add data to classifying tree
                #print (reduced_taxonomy, distance)
                out_file.writelines(header + '\t' + genome + '\t' + ':'.join(reduced_taxonomy) + '\t' + str(distance) + '\n')
                processQuery(reduced_taxonomy, distance, cur_tree)
                # output.writelines((temp_file + ',' + name + ',' + dist + '\n'))
            print("Time", time.time() - start)

            # classify sequence
            print("\nClassifying contig using maximum values")
            cur_tree.getMaxDistPath()

            # Clean up temp files
            os.remove(temp_file)
    else:  # classify entire input as single query
        # as it stands this will only take the first hit of the assembly, which is usually the biggest contig.
        cur_tree = Tree()
        for genome in [directory_path + '/' + x for x in os.listdir(directory_path) if x.endswith('.gz')]:
            name = genome.split('/')[-1]
            distance, best_hit = BLAST.blast_file(target_genome_path, genome)

            # Determine taxonomy data
            reduced_taxonomy = tax_from_file(name)

            # Write data to output
            out_file.writelines(target_genome_path + '\t' + genome + '\t' + ':'.join(reduced_taxonomy) + '\t' + str(distance) + '\n')

            # fill tree
            processQuery(reduced_taxonomy, distance, cur_tree)

        print("Time", time.time() - start)

        # classify sequence
        start = time.time()
        print("\nClassifying contig using maximum values")
        cur_tree.getMaxDistPath()
        print("Time", time.time() - start)

    out_file.close()






    out_file.close()

if __name__== "__main__":
    main()