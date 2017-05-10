from gensim import models
import time

start_time = time.perf_counter()
print('\nLoading vectors...\n')
w = models.KeyedVectors.load_word2vec_format('/home/ubuntu/sim/CBOW|skipgram.bin', binary=True)


relations = {'': [''],
             '': [''],
             '': ['']}

original_verbs = list(relations.keys())
