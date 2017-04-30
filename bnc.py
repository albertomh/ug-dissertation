import nltk.corpus.reader.bnc
import time
import os
import ast


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

        """
        - The outfile_name is in the form: {cat}_{file}.txt where cat(egory)
          can be aca, dem, fic, news and file is the name of the source .xml.

        - A counter is created which will later be used to print how many
          sentences have been saved per file.

        - A summary of the scraped data is written to word/log.txt

        """

        outfile_name = "{}.txt".format(fileid)
        outfile_name = outfile_name.replace("/", "-")
        outfile_name = outfile_name.replace(".xml", "")
        counter = 0


        # Look through sentences for instances of 'word'.
        with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name), "a") as outfile:
            outfile.write("{")

        for position, sentence in enumerate(sentences_in_file[0:len(sentences_in_file)]):
            for tup in sentence:
                if verb in tup:

                    # If a match is found, write tagged data to outfile.
                    with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name), "a") as outfile:
                        outfile.write("{}: {}, ".format(position, sentence))

                    # Update values and print message for each file.
                    counter += 1
                    sent_list.append(position)
                    num_words += len(sentence)
                    sent_counter += 1

                    match_files.append(outfile_name)

        statusmsg_filesents = "{}  \n| {} sentences saved to out/{}/{}.\n".format(sent_list, len(sent_list), verb, outfile_name)

        # Write to logfile and print status for each file. Remove outfile if empty.
        with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name), "a") as outfile:
            outfile.write("}")
        with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, logfile_name), "a") as logfile:
            logfile.write(statusmsg_filesents)
        if len(sent_list) == 0:
            os.remove("/home/ubuntu/ug-d/out/{}/{}".format(verb, outfile_name))
        print(statusmsg_filesents)


    # Closing message printed to console and added to log.
    time_taken = time.perf_counter() - start_time
    statusmsg_final = "{}\nFound '{}' in {} / {} sentences across {} / {} files.\nScraped {} words out of {}. \n\n|| That took: {:.1f} seconds. ||\n".format("-" * 75, verb, sent_counter, total_sents, len(set(match_files)), total_files_counter, num_words, total_words, time_taken)

    with open("/home/ubuntu/ug-d/out/{}/{}".format(verb, logfile_name), "a") as logfile:
            logfile.write(statusmsg_final)
    print(statusmsg_final)


# ==========================================================================================================
def getVV(verb, cat):
    """
    Merges the files created by search(word) and flattentuple(word), saving
    only instances of ("word", V), ("?", V).

    First load all files corresponding to a single category into /out/{word}/
    by running search("{word}") with a suitable regex.

    Then run getVV for each of the four categories.

    >> python3 -c 'import ubnc; ubnc.getVV("word", "cat")'   | "begin", "aca"

    """

    start_time = time.perf_counter()
    total_files = 0
    total_sents = 0

    directory = "/home/ubuntu/ug-d/out/{}/{}/".format(verb, cat)
    merge_dir = "/home/ubuntu/ug-d/out-merge/{}/".format(verb)
    print(directory)


    with open("{}{}VV.txt".format(merge_dir, cat), "a") as mergefile:
        mergefile.write("{")

    for file in os.listdir(directory):
        if not file.endswith("log.txt"):
            total_files += 1
            filetag = file.replace(".txt", "").replace("-", "")
            filetag = filetag.replace(cat, "")

            with open("{}{}".format(directory, file), "r") as oldfile:
                oldfile = ast.literal_eval(oldfile.read())
                all_keys = list(oldfile.keys())


            with open("{}{}VV.txt".format(merge_dir, cat), "a") as mergefile:

                for key in all_keys:
                    for x, y in zip(oldfile[key], oldfile[key][1:]):
                        if x[0] == verb and x[1] == "VERB" and y[1] == "VERB":
                            total_sents += 1
                            print("\n{}  Sentence found in: {}  {}".format("-" * 15, file, "-" * 15))
                            mergefile.write("'{}-{}': {}, ".format(filetag, key, oldfile[key]))
                            print("{}\n".format(oldfile[key]))


    with open("{}{}VV.txt".format(merge_dir, cat), "a") as mergefile:
        mergefile.write("}")

    time_taken = time.perf_counter() - start_time
    print("\n{}\nProcessed {} sentences across {} files.\n|| That took: {:.1f} seconds. ||\n".format("-" * 75, total_sents, total_files, time_taken))


# ==========================================================================================================
def getVNP(verb, cat):
    """
    Merges the files created by search(verb) and flattentuple(verb), saving
    only instances of ("verb", V), ("the", ART).

    First load all files corresponding to a single category into /out/{verb}/
    by running search("{verb}") with a suitable regex.

    Then run getVNP for each of the four categories.

    >> python3 -c 'import ubnc; ubnc.getVNP("verb", "cat")'   | "begin", "aca"

    """

    start_time = time.perf_counter()
    total_files = 0
    total_sents = 0

    directory = "/home/ubuntu/ug-d/out/{}/{}/".format(verb, cat)
    merge_dir = "/home/ubuntu/ug-d/out-merge/{}/".format(verb)

    with open("{}{}VNP.txt".format(merge_dir, cat), "a") as mergefile:
        mergefile.write("{")

    for file in os.listdir(directory):
        if not file.endswith("log.txt"):
            total_files += 1
            filetag = file.replace(".txt", "").replace("-", "")
            filetag = filetag.replace(cat, "")

            with open("{}{}".format(directory, file), "r") as oldfile:
                oldfile = ast.literal_eval(oldfile.read())
                all_keys = list(oldfile.keys())


            with open("{}{}VNP.txt".format(merge_dir, cat), "a") as mergefile:

                for key in all_keys:
                    for x, y in zip(oldfile[key], oldfile[key][1:]):
                        if x[0] == verb and x[1] == "VERB" and y[0] == "the" and y[1] == "ART":
                            total_sents += 1
                            print("\n{}  Sentence found in: {}  {}".format("-" * 15, file, "-" * 15))
                            mergefile.write("'{}-{}': {}, ".format(filetag, key, oldfile[key]))
                            print("{}\n".format(oldfile[key]))


    with open("{}{}VNP.txt".format(merge_dir, cat), "a") as mergefile:
        mergefile.write("}")

    time_taken = time.perf_counter() - start_time
    print("\n{}\nProcessed {} sentences across {} files.\n|| That took: {:.1f} seconds. ||\n".format("-" * 75, total_sents, total_files, time_taken))


# ==========================================================================================================
def targetVNP(verb):
    """
    Uses the tuples created by getVV(verb), getVNP(verb) which were
    subsequently stored in /out-merge/verb/{CAT}-{VV|VNP}.txt.

    Then trims sentences to get target NPs, storing snippets as
    a list at /out-merge/{verb}/catVNP-snippets.
    e.g. [ [('begin', 'VERB'), ('the', 'ART'), ('research', 'SUBST')], [...] ]

    >> python3 -c 'import ubnc; ubnc.targetVNP("verb")' |  "begin"

    """

    start_time = time.perf_counter()
    total_files = 0
    total_sents = 0

    directory = "/home/ubuntu/ug-d/out-merge/{}/".format(verb)


    for file in os.listdir(directory):
        if not file.endswith("log.txt") and file.endswith("VNP.txt"):
            print("\n{}  FILE BEING PROCESSED: {}  {}".format("-" * 15, file, "-" * 15))
            total_files += 1

            with open("{}{}".format(directory, file), "r") as oldfile:
                oldfile = ast.literal_eval(oldfile.read())
                all_keys = list(oldfile.keys())
                num_sentences = len(all_keys)
                total_sents += num_sentences

            file = file.replace(".txt", "")

            with open("{}/{}-snippets.txt".format(directory, file), "a") as newfile:
                newfile.write("[")


            for key in all_keys:

                snippet_index = [x for x, y in enumerate(oldfile[key]) if y[0] == verb]
                snippet_index = snippet_index[0]  # snippet_index is an integer.
                snippet = oldfile[key][snippet_index:]

                end_index = [x for x, y in enumerate(snippet) if y[1] == 'SUBST']
                end_index = end_index[0] + 1

                snippet = snippet[:end_index]

                with open("{}/{}-snippets.txt".format(directory, file), "a") as newfile:
                    newfile.write("{}, ".format(snippet))

            with open("{}/{}-snippets.txt".format(directory, file), "a") as newfile:
                newfile.write("]")

    time_taken = time.perf_counter() - start_time
    print("\n{}\nProcessed {} sentences across {} files.\n|| That took: {:.1f} seconds. ||\n".format("-" * 75, total_sents, total_files, time_taken))


# ==========================================================================================================
def retrosearch(verb, cat):

	start_time = time.perf_counter()
    sent_counter = 0
    print("Calculating total number of sentences...")
    total_sents = len(BNC_data.sents())

    total_files_counter = 0
    num_words = 0
    print("Calculating total number of words...\n")
    total_words = len(BNC_data.words())


	# Generate list of nouns that have appeared alongside 'verb'.
    nouns = []
    with open("/home/ubuntu/ug-d/out-merge/{}/{}VNP-snippets.txt".format(verb, cat)) as snippet_file:
        snippet_list = ast.literal_eval(snippet_file.read())

        for snippet in snippet_list:
            nouns.append([tup[0] for tup in snippet if tup[1] == 'SUBST'][0])

 	match_files = []
    paraverb_sents = []

    for fileid in BNC_data.fileids():
        sentences_in_file = BNC_data.tagged_sents(fileid, stem=False)  # c5=True
        total_files_counter += 1

    	#  Sentences that contain a verb which could potentially
        #  paraphrase the original verb.
        for noun in nouns:
            for sentence in sentences_in_file:
                for tup in sentence:
                    if tup[0] == noun and tup[1] == 'SUBST':

                    	sentence = [x[0] for x in sentence]
                        sentence = " ".join(sentence)

                        paraverb_sents.append(sentence)
                        num_words += len(sentence)
                        sent_counter += 1
                        match_files.append(fileid)
