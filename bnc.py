import nltk.corpus.reader.bnc
import time


# ==========================================================================================================
"""
Read BNC data. Target specific folders (aca, dem, fic, news) with regex in
fileids parameter.

"""
start_time = time.perf_counter()
BNC_data = nltk.corpus.reader.bnc.BNCCorpusReader(root='/home/ubuntu/ug-d/bncbaby/',
                                                  fileids=r'aca/\w*\.xml',  # r'aca/\w*\.xml', # r'[a-z]{3}/\w*\.xml')
                                                  lazy=False)  # found here: https://github.com/nltk/nltk/issues/781 talk about how much more efficient it is
time_taken = time.perf_counter() - start_time
print('\n|| Successfully loaded the British National Corpus in {:.1f}'.format(time_taken), 'seconds. ||\n')


# ==========================================================================================================
def listall():
    """
    Prints a list of all files in the dataset and
    the number of sentences in each file.

    >> python3 -c 'import ubnc; ubnc.listall()'

    """

    start_time = time.perf_counter()

    sent_counter = 0
    file_counter = len(BNC_data.fileids())

    for fileid in BNC_data.fileids():
        number_of_sents = len(BNC_data.sents(fileid))
        sent_counter += number_of_sents
        print(fileid, number_of_sents)

    time_taken = time.perf_counter() - start_time
    print('\n || {} sentences across {} files. ||\n'.format(sent_counter, file_counter), '|| That took: {:.1f}'.format(time_taken), 'seconds. ||\n')


# ==========================================================================================================
def search(verb):

    start_time = time.perf_counter()
    sent_counter = 0
