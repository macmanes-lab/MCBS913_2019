
# Taxonomic Classification of DNA Sequences using Support Vector Machines
**Author:** William Rivera  
**Course:** MCBS 913 | Applied Bioinformatics  
**Professors:** Matthew MacManes, Anthony Westbrook  
**Group:** Machine Learning  
**Date:** May 21, 2019

## Overview
This is a first foray for this investigator into using support vector machines (SVMs). The primary goal of this project was to investigate a potential computational method for classifying short (100-250bp) next-gen sequencing (NGS)  reads based on their sequence data alone. Given the challenges in generating features about the sequences beyond characteristics such as GC content and k-mer frequency distributions, utilizing a machine learning (ML) algorithm to classify the sequences seemed a viable option. Out of the candidate ML algorithms considered, I decided to explore support vector machines as there was not a lot of literature that appeared to explore the use of SVMs on biological sequence data. As this project represents a proof of concept and not a finished product, recommendations for future improvements are made throughout.

### Brief Support Vector Machine Theory

Support vector machines are a class of machine learning algorithm frequently used in classification tasks, particularly those that lend themselves to linear and logistic regression analysis. 

The central idea behind SVMs is that they are capable of performing classification tasks by separating classes along their features (i.e., data points or feature mappings) by creating a decision boundary or hyperplane that separates clusters of data points representative of the different classes. What an SVM is generally attempting to do is find the optimal hyperplane which creates the largest possible margins between the extreme cases of each opposing class. The extreme values represent the 'support vectors' in SVMs, where a support vector can be understood as a line or plane traced through one of the boundary data points parallel to the hyperplane. [1, 7, 8] In the figure below, visual examples of a hyperplane dividing a set of data points in two- and three-dimensional feature spaces are provided. While we will avoid a detailed discussion on the mathematical theories that underlie SVMs, we cannot ignore the major parameters that can be tuned and strategies used to optimize the performance of an SVM.



![hyperplane.png](attachment:hyperplane.png)
<center> Figure 1. Hyperplanes in 2D and 3D feature space [1]</center>


#### SVM Kernels and Hyper-parameters

##### Kernels
In Figure 1, the boundaries separating the classes are quite clear cut. While these images serve as good intuitive representations of how SVMs create hyperplanes, they are not representative of the noisy data sets frequently encountered. They also are datasets that can be represented in low dimensional feature spaces. When dealing with high-dimensional data, determining a hyperplane becomes an increasingly difficult task. Kernel functions, sometimes referred to as using the 'kernel trick', map high-dimensional feature spaces to lower-dimensional to make the creation of a decision boundary that accurately separates classes--while minimizing misclassifications--simpler. (This is done doing a little bit of linear algebra that we won't delve into.) The use of kernel function make the use of SVMs computationaly tractable in many cases when high-dimensional data is being used. Some of the more common kernel functions are: radial-based function (rbf), linear, polynomial, and sigmoid. Rbf kernels are well suited to working high-dimensional data or when dealing with non-linear problems. Linear kernels are used when working with data that is easily linearly separable, such as in the case of two-dimensional data sets. Polynomial kernels are also used for determining hyperplanes in non-linearly separable data sets. [7] 

SVM models will have different hyper-parameters that can be tuned based on the kernel function they use to establish the boundaries between support vectors. Here are some that will be adjusted during the training process.

##### The Regularization paramater, C {rbf}
SVMs use **hinge loss** as the loss function for maximizing the margin between classes. Contained with the hinge loss function is a parameter known as the *regularization* parameter, denoted by C. At its most basic level, C represents the level of tolerance or importance given to misclassifications by the model. The larger C is, the fewer misclassifications are allowed by the model while, conversely, the smaller it is, the more misclassifications are permitted by the model. Optimizing the classification capacity of the model depends on finding the balance between low training error and low testing error to improve the model's ability to generalize and prevent overfitting. [1, 7]

##### Gamma ($\gamma$) {rbf}
The $\gamma$ parameter refers to the influence or importance of a single training example. The lower $\gamma$ is, the broader or less selective the decision boundary is where as a high $\gamma$ reflects a more selective boundary tightly coupled around data points. [7]

#### Degree (d) {polynomial}
The degree of a polynomial kernel function determines how flexible the decision boundary created is in terms of its curvature (graphically speaking). [7]


**For additional background on support vector machines, I would encourage you to check out the following resources:**  

[Support Vector Machine (SVM) - Fun and Easy Machine Learning](https://www.youtube.com/watch?v=Y6RRHw9uN9o)  
[Support Vector Machine — Introduction to Machine Learning Algorithms](https://towardsdatascience.com/support-vector-machine-introduction-to-machine-learning-algorithms-934a444fca47)  
[Support Vector Machine Lecture Notes (by Andrew Ng of Stanford)](http://cs229.stanford.edu/notes/cs229-notes3.pdf)  

### Data Preparation and Feature Extraction
#### Data Acquistion
Genomic data (in the form of .fna files) for analysis was downloaded from the NCBI FTP Server at ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/ using `wget`.

#### Read Simulation
Since the goal of this project is to analyze short NGS reads, the genomic [FastA](https://en.wikipedia.org/wiki/FASTA_format) files will need to be broken down into appropriate length reads. This was achieved using the command line program [ART](https://www.niehs.nih.gov/research/resources/software/biostatistics/art/index.cfm), an NGS read simulator. ART was run on our genomes to simulate Illumina reads of 100, 150, 200, and 250 nucleotides in length.


#### Read Sequence Pre-Processing
A salient challenge in most computational problems and approaches to modeling is that of representation. Genomic data, though voluminous, favorably lends itself to text-based encoding as the nucleotides central to life; <span style="color:blue"> adenosine (A)</span>,<span style="color:orange"> cytosine (C)</span>,<span style="color:red"> guanine (G)</span>, and <span style="color:green"> thymine (T)</span>, are easily represented using single characters. While encoding nucleotides as alphabetic characters make it possible to store  and interact with genomic data for many computational analyses, machine learning algorithms require that data be stored in a numerical representation so that the model can process them. One common method of representating encoding label data is the use of one-hot encoding. A one-hot encoded vector (i.e., 1-dimensional array with preserved order) would be a vector comprising all 0's with the exception of a single 1 used to uniquely identify that label. In the case of nucleotides, this could manifest as:


|  Nucleotide       | One-hot encoding |      
| -------------:|:-------------|
| A      | [1 0 0 0]
| C      | [0 1 0 0]    
| G | [0 0 1 0]
| T | [0 0 0 1]

One-hot encoding, at least in our particular use case, is vulnerable to the 'curse of dimensionality' and the similarity difference between one-hot encoded vectors ends up being equidistant. These notions are touched on greater detail in [dna2vec:Consistent vector representations of variable-length k-mers](https://arxiv.org/pdf/1701.06279.pdf) which is also where a work around to these issues can be found. In the Natural Language Processing (NLP) space within machine learning, researchers developed a series of models for creating word embeddings or vectors of real numbers that encode both semantic and linguistic information of words. One of the, if not, the most popular word-embedding package is **word2vec**. Patrick Ng, a researcher at Cornell University, leveraged the **word2vec** library and trained the embeddings on k-mers instead of words derived from human language, and made some interesting findings. The most relevant contributions from his paper were that variable-length k-mers could be modeled using word-embedding techniques, addition of dna2vec vectors can be treated as analagous to nucleotide concatentation, and that there is a relationship between Needleman-Wunsch alignment and cosine similarity scores. 

In brief, using **dna2vec** will allow for the generation of consistent and unique sequence representations that can be fed into this, or other, machine learning models.

#### k-mer frequency data extraction
In bioinformatics, the term **k-mer** is ubiqituous. It simply refers to a string with a length of k , where k is a positive integer denoting the number of nucleotides, amino acid residues, etc. in the sequence. K-mers in isolation are of limited value, but when all k-mers of a particular sequence or perhaps a genome are considered, they can provide information that is useful in sequence alignment and assembly. As other read sequence features are not readily identifiable, at least to this investigator, k-mer frequency distributions were also passed to our model as potentially meaningful features. While the k-mer frequency distributions or histograms can be saved as Python dictionaries, this is another unfavorable data type for MLA processing, so these dictionaries will also need to be converted into vectors. This can be achieved using the **DictVectorizer** module from sci-kit learn. If you'd like to learn more about k-mers, here is a link to the [Wikipedia article](https://en.wikipedia.org/wiki/K-mer).

#### GC content calculation
While a trivial calculation to perform, GC content has revealed itself to be a diagnostic criterion in the analysis of genetic sequences and genomes. For this reason, it was included as the final feature sequence passed to our model.


## Getting Started
Now that we've touched on most of the relevant background information and general process, let's move onto actual machine learning! These instructions will walk you through the installation and deployment process for training and running an SVM Classifier using the sci-kit learn library.

### Requirements

The majority of packages and modules used are available for installation via `pip` or `conda`. These are listed in [requirements.txt](../requirements.txt).

One package not available by the above means is **dna2vec**. To install this open-source library, please visit Patrick Ng's [Github repository](https://github.com/pnpnpn/dna2vec). *Note*: installing dependencies using conda package manager instead of pip made for a much cleaner install due to issues with dependency versioning. Also, to avoid needing to these scripts in the same directory where dna2vec is unpacked, installing it as a Python module using the `python setup.py install` command in the module's root directory.

**DISCLAIMER:** As [pipreqs](https://github.com/bndr/pipreqs) was run on the UNH Ron Server in a **conda** environment, the requirements list may be incomplete relative to your personal computer if you are not a user with access to Ron.

### Read Simulation with ART_Illumina

First, reference genomes must be downloaded for simulation. For example, to download the genome for *Bacillus subtilis* one would run the following shell command:
```
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/Bacillus_subtilis/reference/GCF_000009045.1_ASM904v1/GCF_000009045.1_ASM904v1_genomic.fna.gz
```
Then to break down the genomes into simulated reads, the following command with these required flags must run. 
```
art_illumina [options] -sam -i <seq_ref_file> -l <read_length> -f <fold_coverage> -ss <sequencing_system> -o <outfile_prefix>
```

For our testing purposes, we simulated single-end reads from our reference genomes with 10X fold coverage at the aforementioned read lengths using multiple sequencing systems (HS20 at 100bp, HS25 at 150bp, MSv1 at 200bp and 250bp). Again, using *B. subtilis* as an example, here would be the command to simulate its genome using ART_Illumina with reads 100bp long:

```
art_illumina --ss HS25 -sam -i GCF_000009045.1_ASM904v1_genomic.fna -l 100 -f 10 -o single_dat_bs.fq
```
This command will produce a [FastQ](https://en.wikipedia.org/wiki/FASTQ_format) file containing all of the simulated reads and a [SAM](https://en.wikipedia.org/wiki/SAM_(file_format)) file with our sequence alignment data.

`input:` bacterial genome (.fna)  
`output:` bacterial genome spliced into reads (.fq) + sequence alignment file (.sam)

#### Training k-mer Embeddings

As the pre-trained **dna2vec** embeddings included with the package are trained using the human genome, we opted to train the embeddings on our set of bacterial genomes.

|Species| 
|:---:|
|A. bacterium|
|B. pumilis|
|B. subtilis|
|C. botulinum|
|E.cloacae|
|E. coli|
|E. faecalis|
|F. hominis|
|G. sunshinyii|
|H. quentini|
|I. halophila|
|K. pseudosacchari|
|L. fermentum|
|L. monocytogenes|
|M. luteus|
|N. basaltis|
|P. equi|
|R. pickettii|
|S. aureus|
|S. enterica|
|S. epidermidis|
|V. albensis|
|W. ceti|
|X. bromi|
|Y. pestis|

The process is explained in the [**dna2vec**](https://github.com/pnpnpn/dna2vec) README file and is essentially the same with the only difference being that .yml specifying what chromosomal data to train on was modified as below.

sample.yml
```
inputs: inputs/bac_chroms/*.fna
k-low: 3
k-high: 100
vec-dim: 100
epoch: 10
context: 10
out-dir: results/
```

### Subsampling from Simulated Read Files for SVM Training & Testing Data Sets

As the training time of an SVM scales quadratically with the number of samples in your data set, computational resources and time available for experimentation are non-trivial considerations. To keep training times reasonable (~1 hr) it is recommended that you limit the overall number of sequences passed into the model at or under 100,000. To quickly do this on a POSIX OS (which these instructions presume you are operating on) you can use either the `head` or `tail` command using the `-n` flag to specify how many lines of the file you want to grab. Below is an example of how to grab 250 sequences and their related metadata from a FastQ file.

```
head -n 1000 bacterial_genome_file.fq >> new_reads_file.fq
```

Once you have curated a satisfactory collection of reads, it is time to process them.


### Data Preparation Script | data_prep.py 

`data_prep.py` iterates over all read_sequences in the FastQ files in the directory and creates a **pandas** dataframe file containing an array comprising: 1) the vectorized read sequence, 2) its GC content (as a float), and 3) a k-mer dictionary of all kmers up to a user-determined length. The dataframe is pickled and saved as a .pkl file until it is later unpacked by a model.

**Current Usage:** `tax_svm.py`  
**Future Usage:** `data_prep.py /path/to/read_and_tax_data_directory`


>At present, paths to directories containing reads for processing are hard-coded. (With the next update to this code base, the plan will be to make a more interactive command-line tool through the use of `argparse`. Instead of making calls to local variables, users will provide a directory with FastQ files and .csv files containing taxonomic information for processing.) Because of this, all data preparation is actually occuring in tax_svm.py and no pickled dataframe is being created at the moment.

### SVM Training Scripts | tax_svm.py, grid_svm.py 

`tax_svm.py` trains an SVM on the sequence feature data and the taxonomic rank data and generates confusion matrices to provide simple visuals for assessing model performance. 

**Current Usage:** `tax_svm.py`  
`input:` feature data (**pandas** dataframe), taxonomic info (Python dictionary)  
`output:` normalized and non-normalized confusion matrices of prediction accuracies(.png)  

>**Future Usage:** `tax_svm.py dataframe.pkl tax_rank.csv`  
`input:` pickled dataframe (.pkl), taxonomic info (.csv with columns: domain, kingdom, phylum, class, order, family, genus, species)  
`output:` normalized and non-normalized confusion matrices of prediction accuracies(.png)


`grid_search.py` performs an exhaustive search over user-specified parameter value ranges to determine optimal hyperparameters for SVM performance


**Current Usage:** `grid_search.py`  
`input:` feature data (**pandas** dataframe), taxonomic info(Python dictionary)  
`output:` dict of optimal SVM hyperparameters and other miscellaneous training statistics

>**Future Usage:** `grid_search.py dataframe.pkl tax_rank.csv`  
`input:` pickled dataframe (.pkl), taxonomic info (.csv with columns: domain, kingdom, phylum, class, order, family, genus, species)  
`output:` dict of optimal SVM hyperparameters and other miscellaneous training statistics (.txt)  

### Results

Although not overwhelmingly impressive, the model does a reasonable job of classifying the sequences with a classification accuracy of 60.4% using the baseline parameters for the sci-kit SVM classifer (i.e., rbf kernal with scaled gamma). Performance dropped when using a polynomial kernal to 55.1% and was even worse when a sigmoid kernel function was used (37.8%).

## Reflections and Recommendations

Due to time constraints, a full grid-search exploring the optimal SVM parameters using rbf and linear kernel functions was not realized. The code to perform a grid search has been included for the sake of seeing if performance can be improved upon with hyper-parameter tuning. These parameters would need to be specified in the function call for SVM classifier in `tax_svm.py` to recreate this specific model and generate data visualizations. 

While better than random or chance-based success was seen in using SVMs, the need for optimal feature selection and engineering does make unguided supervised learning a more difficult task.  

Deep learning techniques likely would have produced the best results as they have historically done better with sequence data and offer significant performance benefits when dealing with training sets comprising large numbers of samples but limited feature data. [2] As we were able to achieve reasonable classification results using an SVM, exploring how a neural network would perform on the same task feels like a reasonable extension of this work, which could prove quite helpful in metagenomic analysis as it would remove the need to rely on more specific stretches of genetic material such as 16S rRNA.

 ## Acknowledgements
 + I would like to thank my fellow ML group members, Pooja Oza and Amanda Tellier, for their assistance in code reviews, statistical theory discussion, and general support throughout our work on this project.
 + Thanks are also in order to professors Matt MacManes and Toni Westbrook, for their guidance and inspiring conversations while tackling some of the challenges associated with this project.

## References
1. Gandhi, R., & Gandhi, R. (2018, June 07). Support Vector Machine - Introduction to Machine Learning Algorithms. Retrieved from https://towardsdatascience.com/support-vector-machine-introduction-to-machine-learning-algorithms-934a444fca47 
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning. Cambridge (EE. UU.): MIT Press.
3. Guillaume, & Carl. (2011, January 07). Fast, lock-free approach for efficient parallel counting of occurrences of k -mers. Retrieved from https://academic.oup.com/bioinformatics/article/27/6/764/234905
4. Huang, W., Li, L., Myers, J. R., & Marth, G. T. (2012, February 15). ART: A next-generation sequencing read simulator. Retrieved from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3278762/
5. Mikolov, Tomas, Chen, Kai, Corrado, Greg, . . . Jeffrey. (2013, September 07). Efficient Estimation of Word Representations in Vector Space. Retrieved from https://arxiv.org/abs/1301.3781
6. Ng, P. (2017, January 23). Dna2vec: Consistent vector representations of variable-length k-mers. Retrieved from https://arxiv.org/abs/1701.06279
7. Sci-kit learn. (n.d.). 1.4. Support Vector Machines. Retrieved from https://scikit-learn.org/stable/modules/svm.html
8. Stanford University, Ng, A. (n.d.). CS229 Lecture Notes. Lecture. In Part V Support Vector Machines(pp. 1-25).
