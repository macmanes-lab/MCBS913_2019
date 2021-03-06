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
    tax_id = file_name.split('_')[-2]
    taxonomy = tax_lookup[tax_id]
    if taxonomy.split(';')[0] == 'Bacteria':
        seven_levels = [0, 2, 5, 6, 8, 10, 12, 13]
    else:
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
        print(k,score,sorted(distanceList, reverse=True))
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


def pickNode(query_seq, genome_list, curTree, out_file, taxonomy_lookup, header, blast_lookup):
    start = time.time()
    completed = 0
    for genome in genome_list:
        completed += 1
        if completed % 100 == 0:
            print("Finished BLASTING {} genomes".format(completed))
        name = genome.split('/')[-1]
        reduced_taxonomy = tax_from_file(name, taxonomy_lookup) # Determine taxonomy data

        if genome not in blast_lookup.keys():
            distance, best_hit = BLAST.blast_file(query_seq, genome)
            blast_lookup[genome] = [distance, best_hit]

            # Add data to classifying tree
            out_file.writelines(header + '\t' + genome + '\t' + ':'.join(reduced_taxonomy) + '\t' + str(distance) + '\n')
            processQuery(reduced_taxonomy, distance, curTree)
        else:
            distance, best_hit = blast_lookup[genome]

        print(str(distance)+'\t' + '|'.join(reduced_taxonomy))
    # classify sequence
    print("Time for these BLASTS", time.time() - start)
    print("\nClassifying contig using maximum values")
    winning_tax = curTree.getMaxDistPath()
    return winning_tax



def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('target', action='store', help='path to query genome to be compared to database')
    parser.add_argument('-database', '-d', action='store', help='path to genome database')
    parser.add_argument('-path_file', '-p', action='store', help='A Text file with the paths to genomes one per line')
    parser.add_argument('-num_searches', '-n', action='store', type=int, help='Number of pairwise comparisons for each level', default=100)
    parser.add_argument('-tax_lookup', '-t', action='store', help='Text file with accessions and associated taxonomy',
                        default="/home/unhTW/share/mcbs913_2019/hash_group/documents/expanded_ncbi_taxonomy.tsv")
    parser.add_argument('-divide_input', action='store_true', help='Classify each entry in FAST/Q'
                                                                   ' rather than entire file', default='store_true')
    args = parser.parse_args()
    target_genome_path = os.path.abspath(args.target)

    # Parse taxonomy lookup
    start = time.time()
    print("\nParsing taxonomy database")
    taxonomy_lookup = fillTaxonomyLookup(args.tax_lookup)
    print("Time", time.time() - start)


    # Gather list of input genomes
    print('\nGathering list of input files')
    directory_path = os.path.abspath(args.database)
    start = time.time()
    input_genomes = [directory_path+'/' +x for x in os.listdir(directory_path) if x.endswith('.gz')]  # assumes gzipped fastas
    # print("Time", time.time() - start)
    # start = time.time() # this method is slower
    # input_genomes = glob.glob(directory_path+'/'+'*.gz')  # assumes gzipped fastas
    # print("Time", time.time() - start)



    # Sketch the input directory
    start = time.time()
    print("\nSketching starting database (this may take some time... unless its been done before)")
    BLAST.sketch_database(args.database)
    print("Time", time.time() - start)


    # fill database tree
    start = time.time()
    print("\nPopulating reference tree for filling sparse tree")
    database_tree = Tree()
    file_lookup = {}  # species: filepath
    for genome_file in input_genomes:
        taxonomy_list = tax_from_file(genome_file, taxonomy_lookup)
        file_lookup[taxonomy_list[-1]] = genome_file
        processQuery(taxonomy_list, 1, database_tree)
    print("Time", time.time() - start)


    print("\n\tREFERENCE TREE\n")
    database_tree.print_tree(database_tree.getRoot())

    start = time.time()
    out_file = open('my_distances.txt', 'w')
    seq_count = 0
    if args.divide_input:
        for seq_record in SeqIO.parse(target_genome_path, "fasta"):
            total_time = time.time()
            completed_blasts = {}
            seq_count += 1
            start = time.time()
            cur_tree = Tree()
            # grab sequence information
            header = seq_record.id
            sequence = seq_record.seq

            # Create a tmp file named after the contig
            temp_file = str(seq_count) + '.fna'
            file_handle = open(temp_file, 'w')
            file_handle.writelines('>' + header + '\n' + sequence + '\n')
            file_handle.close()


            directory_path = os.path.abspath(args.database)
            # PYTHON Thread pool

            curNode = database_tree.getRoot()
            class_level = 0
            print('Selecting {} comparisons to make each iteration'.format(args.num_searches))
            while class_level < 5:# and len(completed_blasts.keys()) < len(input_genomes):
                cur_tree.print_tree(cur_tree.getRoot())
                print()
                choice = database_tree.randomPickHelper(curNode, args.num_searches)
                # retrieve all the file paths for the chosen species
                filepaths = [file_lookup[x] for x in choice.keys()]  # this assumes all the species names are unique
                # Run all the comparisons and do the work
                winningNode = pickNode(temp_file, filepaths, cur_tree, out_file, taxonomy_lookup, header, completed_blasts)
                selection = winningNode[:class_level + 1]
                print('\nWinner', selection)
                curNode = database_tree.getNodeByName(selection)
                class_level += 1

            # Run every remaining genome under the current node
            num_leafs = curNode.leafSize()
            choice = database_tree.randomPickHelper(curNode, num_leafs)
            # retrieve all the file paths for the chosen species
            filepaths = [file_lookup[x] for x in choice.keys()]  # this assumes all the species names are unique

            winningNode = pickNode(temp_file, filepaths, cur_tree, out_file, taxonomy_lookup, header, completed_blasts)
            cur_tree.print_tree(cur_tree.getRoot())
            print ('FINAL RESULTS', winningNode)
            print ('Total time to classify the sequence', time.time() - total_time)
            # Clean up temp files
            os.remove(temp_file)
    else:  # classify entire input as single query
        # as it stands this will only take the first hit of the assembly, which is usually the biggest contig.
        total_time = time.time()
        completed_blasts = {}
        seq_count += 1
        start = time.time()
        cur_tree = Tree()
        # grab sequence information
        header = seq_record.id
        sequence = seq_record.seq

        # Create a tmp file named after the contig
        temp_file = str(seq_count) + '.fna'
        file_handle = open(temp_file, 'w')
        file_handle.writelines('>' + header + '\n' + sequence + '\n')
        file_handle.close()

        directory_path = os.path.abspath(args.database)
        # PYTHON Thread pool

        curNode = database_tree.getRoot()
        class_level = 0
        print('Selecting {} comparisons to make each iteration'.format(args.num_searches))
        while class_level < 5:  # and len(completed_blasts.keys()) < len(input_genomes):
            cur_tree.print_tree(cur_tree.getRoot())
            print()
            choice = database_tree.randomPickHelper(curNode, args.num_searches)
            # retrieve all the file paths for the chosen species
            filepaths = [file_lookup[x] for x in choice.keys()]  # this assumes all the species names are unique
            # Run all the comparisons and do the work
            winningNode = pickNode(temp_file, filepaths, cur_tree, out_file, taxonomy_lookup, header, completed_blasts)
            selection = winningNode[:class_level + 1]
            print('\nWinner', selection)
            curNode = database_tree.getNodeByName(selection)
            class_level += 1

        # Run every remaining genome under the current node
        num_leafs = curNode.leafSize()
        choice = database_tree.randomPickHelper(curNode, num_leafs)
        # retrieve all the file paths for the chosen species
        filepaths = [file_lookup[x] for x in choice.keys()]  # this assumes all the species names are unique

        winningNode = pickNode(temp_file, filepaths, cur_tree, out_file, taxonomy_lookup, header, completed_blasts)
        cur_tree.print_tree(cur_tree.getRoot())
        print('FINAL RESULTS', winningNode)
        print('Total time to classify the sequence', time.time() - total_time)
        # Clean up temp files
        os.remove(temp_file)
        sys.exit()


    out_file.close()






    out_file.close()

if __name__== "__main__":
    main()