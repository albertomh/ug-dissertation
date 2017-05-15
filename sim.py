from gensim import models
import time

start_time = time.perf_counter()
print('\nLoading vectors...\n')
w = models.KeyedVectors.load_word2vec_format('/home/ubuntu/sim/CBOW|skipgram.bin', binary=True)


relations = {'': [''],
             '': [''],
             '': ['']}

original_verbs = list(relations.keys())


for verb in original_verbs:
    print('\n\n')
    for paraverb in relations[verb]:
        print('{}-{}: {:.5f}'.format(verb, paraverb, w.similarity(''.join([i for i in verb if not i.isdigit()]), paraverb)))
