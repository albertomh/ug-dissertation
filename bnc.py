import nltk.corpus.reader.bnc
import time


start_time = time.perf_counter()
BNC_data = nltk.corpus.reader.bnc.BNCCorpusReader(root='/home/ubuntu/ug-d/bncbaby/',
                                            fileids=r'aca/\w*\.xml', # r'aca/\w*\.xml', # r'[a-z]{3}/\w*\.xml')
                                            lazy=False)  # found here: https://github.com/nltk/nltk/issues/781 talk about how much more efficient it is
time_taken = time.perf_counter() - start_time
print('\n|| Successfully loaded the British National Corpus in {:.1f}'.format(time_taken), 'seconds. ||\n')