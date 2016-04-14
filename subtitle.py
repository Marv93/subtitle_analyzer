#!/usr/bin/python
#! coding: utf-8

import pysrt
import string
import sys
import time

class CountingSet(object):
    def __init__(self):
        self.content = {}
        
    def add(self, something):
        if something not in self.content.keys():
            self.content[something] = 1
        else:
            self.content[something] += 1
            
    def add_many(self, liste):
        for thing in liste:
            self.add(thing)
        
    def get_content(self):
        tmp_list = []
        for key in self.content.keys():
            tmp_list.append((key, self.content[key]))
        return_list = sorted(tmp_list, key=lambda tupel: tupel[1], reverse=True)
        return return_list

def generate_ngrams(wort):
    return_list = []
    ngram_len = 4
    word_len = len(wort)
    while word_len >= ngram_len:
        for i in xrange(0, word_len-ngram_len+1):
            return_list.append(wort[i:i+ngram_len])
        ngram_len += 1
    return return_list

def compare_ngrams(ngram_list):
    new_ngram_list = []
    for i in xrange(0,len(ngram_list)):
        found = False
        for j in xrange(i+1, len(ngram_list)):
            if ngram_list[i][1] > ngram_list[j][1]:
                break
            else:
                if ngram_list[i][0] in ngram_list[j][0]:
                    found = True
                    break
                    
        for j in xrange(i-1, 0, -1):
            if ngram_list[i][1] > ngram_list[j][1]:
                break
            else:
                if ngram_list[i][0] in ngram_list[j][0]:
                    found = True
                    break
                    
        if found == False:
            new_ngram_list.append(ngram_list[i])
    return new_ngram_list

sonderzeichen = ["'","-",".",",","+","!","?",":","(",")","</i>","<i>","</b>","<b>","</u>","<u>"]

word_set = CountingSet()
ngram_set = CountingSet()

out_filename = ""

start = time.time()

for arg_num in xrange(1, len(sys.argv)):
    filename_ex = sys.argv[arg_num]
    dot_index = filename_ex.index(".")
    extension = filename_ex[dot_index:]
    filename = filename_ex[:dot_index]
    out_filename += "_" + filename

    # subs is a list of pysrt.srtitem.SupRipItem objects
    try:
        subs = pysrt.open(filename_ex)
    except UnicodeDecodeError:
        subs = pysrt.open(filename_ex, encoding="iso-8859-1")

    for sub in subs:
        worte = string.split(sub.text)
        for wort in worte:
            wort_kopie = wort.lower()
            for zeichen in sonderzeichen:
                wort_kopie = wort_kopie.replace(zeichen, "")
            if len(wort_kopie) > 0:
                word_set.add(wort_kopie)
                if len(wort_kopie) >= 4:
                    ngrams = generate_ngrams(wort_kopie)
                    ngram_set.add_many(ngrams)

wortliste = word_set.get_content()
ngramliste = compare_ngrams(ngram_set.get_content())

if len(sys.argv) > 1:
    FH = open("wortliste"+out_filename,"w")
    for tupel in wortliste:
        FH.write(tupel[0].encode('utf-8') + "\t" + str(tupel[1]) + "\n")
    FH.close()

    FH = open("ngramliste"+out_filename,"w")
    for tupel in ngramliste:
        FH.write(tupel[0].encode('utf-8') + "\t" + str(tupel[1]) + "\n")
    FH.close()

end = time.time()

print len(wortliste), "Worte"
print len(ngramliste), "N-Gramme"
print end-start, "Sekunden"
