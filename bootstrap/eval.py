# coding=utf-8
from gensim.models import Word2Vec as w2v
from codecs import open

model = w2v.load_word2vec_format('news_vectors.bin', binary=True)
rel = open('all_relations.txt', 'r', encoding='utf-8').readlines()
desc = open('filt_desc.txt', 'r', encoding='utf-8').readlines()
new = open('relations_with_desc.txt', 'w', encoding='utf-8')
not_f = open('not_found.txt', 'w', encoding='utf-8')
sim = []
not_found = []
for r in rel:
    per, _ = r.strip('\n').split(',')
    per = per.split(' ')
    if len(per) > 1:
        per = per[1] + '_S'
    else:
        per = per[0] + '_S'
    s = []
    for d in desc:
        d = d.strip('\n') + '_S'
        try:
            g = ((model.similarity(per, d), d))
            s.append(g)
        except KeyError:
            not_found.append(r)
            break
    else:
        s = sorted(s, reverse=True)
        try:
            sim.append((r.strip('\n').rstrip(','), ','.join([s[0][1], s[1][1], s[2][1]])))
        except Exception:
            print s
            print per, len(not_found)
            raise
for s in sim:
    new.write(','.join(s) + '\n')
for n in not_found:
    not_f.write(n)
not_f.close()
new.close()
# for line in desc:
#     line = line.strip('\n').split('  ')
#     if len(line) > 1:
#         try:
#             _ = model[l[0] + '_A']
#             _ = model[l[1] + '_S']
#             new.write(' '.join(line) + '\n')
#         except KeyError:
#             continue
#     else:
#         try:
#             _ = model[line[0] + '_S']
#             new.write(line[0] + '\n')
#         except KeyError:
#             continue