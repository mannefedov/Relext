from collections import Counter
import os
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

class Dict():
    def __init__(self):
        dictionary = open('dict\\descriptors.txt', encoding='utf-8')
        self.dictionary = set([x.strip('\n') for x in dictionary])

    def get_dict(self):
        return self.dictionary

    def lookup(self, word):
        if word in self.dictionary:
            return True
        else:
            return None


def main():
    d = Dict()
    files = [x for x in os.listdir('.\\texts\\') if x.endswith('.txt')]
    who = []
    hypo = []
    # word_bag_a = Counter()
    # word_bag_b = Counter()
    for f in files:
        f = open('texts\\' + f, encoding='utf-8').read()
        index = f.lower().find('дмитрий медведев')
        bef = f[index-150:index].lower()
        bef = bef.split()
        
        for i in range(len(bef)):
            lemma = morph.parse(bef[i])[0].normal_form
            # tag = morph.parse(word)[0].tag.case
            if d.lookup(lemma):
                # print('found lemma ', lemma)

                who.append(lemma)
                who += bef[i+1:]
                # print('left: ', bef[i+1:])
                hypo.append(' '.join(who))
                who = []
                # print('hypo now', hypo)
                break
            # if who and tag == 'gent':
            #   who.append(word)

        #     word_bag_b.update([word])
        # for word in aft:
        #     word = morph.parse(word)[0].normal_form
        #     word_bag_a.update([word])
    c = open('test.txt','w',encoding='utf-8')
    for x in hypo:
        c.write(x + '\n')
    c.close()
if __name__ == '__main__':
    main()