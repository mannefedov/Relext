from nltk.data import load
from nltk.tokenize import word_tokenize as wt
from string import punctuation as punkt


def split_sentences(corpus='rbc.txt', newfile='rbc_se.txt'):
    t = load('tokenizers/punkt/russian.pickle')
    text = open('.\\crawler\\' + corpus, 'r', encoding='utf-8')
    new = open(newfile, 'w', encoding='utf-8')
    for line in text:
        s = t.tokenize(line.strip('\n'))
        for sent in s:
            new.write(sent + '\n')
    text.close()
    new.close()


def filter_sentences(corpus='rbc_se.txt', dic='names.txt', newfile='rbc_sent_filt_new.txt'):
    name_dict = set([x.strip('\n') for x in open('.\\preprocessing\\' + dic, encoding='utf-8')])
    text = open(corpus, encoding='utf-8')
    new_file = open(newfile, 'w', encoding='utf-8')
    for line in text:
        tokens = wt(line.strip('\n'))
        for word in tokens:
            if word in punkt:
                continue
            word = word.lower()
            if word in name_dict:
                new_file.write(line)
                break
    text.close()
    new_file.close()



