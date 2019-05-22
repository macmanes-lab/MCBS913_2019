from dna2vec.multi_k_model import MultiKModel # for converting short-read DNA sequences into vectorized reads

filepath = '../../pretrained/dna2vec-20161219-0153-k3to8-100d-10c-29320Mbp-sliding-Xat.w2v' #path to file with vectorized k-mer representations
mk_model = MultiKModel(filepath) # instantiating model for fetching vectorized k-mer representations

def kmer_frequency(sequence, start, end, data):
    """
	Calculate kmer frequency for k-mers of length i-j

	Keyword arguments:
	sequence -- DNA record sequence (string)
	start -- min k-mer length (int)
	end -- max k-mer length (int)
	data -- empty dictionary to populate with k-mer frequency data (dict)
    """
    for counter in range(start, end + 1):
        for kmer in generate_kmers(sequence, counter):
            # print(kmer)
            if kmer in data:
                data[kmer] = data[kmer] + 1
            else:
                data[kmer] = 1
    return data


def generate_kmers(sequence, length):
    """ Generate k-mers of length i-j"""
    for kmer in range(0, len(sequence) - length):
         yield sequence[kmer:kmer + length]


def gc_content(dna_seq):
    """Calculate GC Content of a DNA sequence"""
    g_content = dna_seq.upper().count('G')
    c_content = dna_seq.upper().count('C')
    return (g_content + c_content) / len(dna_seq)


def generateEmbeddingFeatures(kmer):
    """Return vectorized kmer"""
    return mk_model.vector(kmer)
