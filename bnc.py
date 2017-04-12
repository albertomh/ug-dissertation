import nltk.corpus.reader.bnc
import time
import os


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
    """
    Saves a list of sentences containing the search term 'word'. Scraped data
    is output to out/word/cat-$FILE.txt in the form:

        {x: [('stem', 'TAG'), (...)], [...]}

    A dictionary whose key 'x' is the position of the dict's value in
    the original .xml; and whose value is a list of tuples where the
    first item of the tuple is the stem form of a word and the second
    item is the TAG foundin the British National Corpus.

    >> python3 -c 'import ubnc; ubnc.search("verb")'

    """

    start_time = time.perf_counter()
    sent_counter = 0
    print("Calculating total number of sentences...")
    total_sents = len(BNC_data.sents())

    total_files_counter = 0
    num_words = 0
    print("Calculating total number of words...\n")
    total_words = len(BNC_data.words())

    match_files = []
    logfile_name = "log.txt"

    for fileid in BNC_data.fileids():
        sentences_in_file = BNC_data.tagged_sents(fileid, stem=True)  # c5=True
        total_files_counter += 1
        sent_list = []


        outfile_name = "{}.txt".format(fileid)
        outfile_name = outfile_name.replace("/", "-")
        outfile_name = outfile_name.replace(".xml", "")
        counter = 0


        with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name), "a") as outfile:
            outfile.write("{")

        for position, sentence in enumerate(sentences_in_file[0:len(sentences_in_file)]):
            for tup in sentence:
                if verb in tup:

                    with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name), "a") as outfile:
                        outfile.write("{}: {}, ".format(position, sentence))

                    counter += 1
                    sent_list.append(position)
                    num_words += len(sentence)
                    sent_counter += 1

                    match_files.append(outfile_name)

        statusmsg_filesents = "{}  \n| {} sentences saved to out/{}/{}.\n".format(sent_list, len(sent_list), verb, outfile_name)

        with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name), "a") as outfile:
            outfile.write("}")
        with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, logfile_name), "a") as logfile:
            logfile.write(statusmsg_filesents)
        if len(sent_list) == 0:
            os.remove("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name))
        print(statusmsg_filesents)


    time_taken = time.perf_counter() - start_time
    statusmsg_final = "{}\nFound '{}' in {} / {} sentences across {} / {} files.\nScraped {} words out of {}. \n\n|| That took: {:.1f} seconds. ||\n".format("-" * 75, verb, sent_counter, total_sents, len(set(match_files)), total_files_counter, num_words, total_words, time_taken)

    with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, logfile_name), "a") as logfile:
            logfile.write(statusmsg_final)
    print(statusmsg_final)
