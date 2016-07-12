from lxml import etree
import requests
import re
from random import choice
from multiprocessing import Pool
from itertools import islice
from time import time
from collections import Counter

def get_all(corp='corpus.txt'):
    corpus = open(corp, encoding='utf-8')
    new_file = open('all_relations.txt', 'w', encoding='utf-8')

    for line in corpus:
        line = etree.fromstring(line)
        new_file.write('{},{}\n'.format(line.xpath('//PER/text()')[0], line.xpath('//ORG/text()')[0]))

    corpus.close()
    new_file.close()


def get_true(relation):
    r_with_pmi = None
    lenta = "https://lenta.ru/search/process?&query="
    rbc = "http://rbc.ru/search/ajax/?project=rbcnews&limit=1&query="
    site = choice([lenta, rbc])
    per, org, d1, d2, d3 = relation.strip('\n').split(',')
    try:
        # r_per = requests.get(site + per.replace(' ', '+'))
        r_tog = requests.get(site + per.replace(' ', '+') + '+' + org.replace(' ', '+'))
        d1_ = requests.get(site + per.replace(' ', '+') + '+' + org.replace(' ', '+'))
        d2_ = requests.get(site + per.replace(' ', '+') + '+' + org.replace(' ', '+'))
        d3_ = requests.get(site + per.replace(' ', '+') + '+' + org.replace(' ', '+'))
    except Exception:
        raise
    n_tog = re.search('"total_found": ([0-9]*),|"counts":\{"_total":"([0-9]*)",', r_tog.text)
    d1 = re.search('"total_found": ([0-9]*),|"counts":\{"_total":"([0-9]*)",', d1_.text)
    d2 = re.search('"total_found": ([0-9]*),|"counts":\{"_total":"([0-9]*)",', d2_.text)
    d3 = re.search('"total_found": ([0-9]*),|"counts":\{"_total":"([0-9]*)",', d3_.text)

    if d1 is not None and n_tog is not None \
        and d2 is not None and d3 is not None:
        if site == rbc:
            d1 = d1.group(2)
            d2 = d2.group(2)
            d3 = d3.group(2)
            n_tog = n_tog.group(2)
        else:
            d1 = d1.group(1)
            d2 = d2.group(1)
            d3 = d3.group(1)
            n_tog = n_tog.group(1)
        try:
            pmi = max([int(x)/int(n_tog) for x in [d1, d2, d3]])
        except ZeroDivisionError:
            pmi = 0
    if pmi > 0.5:    
        return (per, org)
    else:
        return None

def unfound(relation):
    desc = open('filt_desc.txt', encoding='utf-8').readlines()
    rbc = "http://rbc.ru/search/ajax/?project=rbcnews&limit=1&query="
    per, org = relation.strip('\n').split(',')
    c = Counter()
    n_per = 0
    for i in range(10):
        rbc = "http://rbc.ru/search/ajax/?project=rbcnews&offset={}&limit=10&query=".format(i*10)
        r_tog = requests.get(rbc + per.replace(' ', '+') + '+' + org.replace(' ', '+'))
        n_per = re.search('"counts":\{"_total":"([0-9]*)",', r_tog.text).group(1)
        for d in desc:
            d = d.strip('\n')
            f = r_tog.text.find(d)
            if f != -1:
                c.update([d])
    if int(n_per) < 3:
        if c and c.most_common(1)[0][1] > 2:
            return (per, org)
        else:
            return None
    if int(n_per) < 10:
        if c and c.most_common(1)[0][1] > 5:
            return (per, org)
        else:
            return None
    
    if c and c.most_common(1)[0][1] > 10:
        return (per, org)
    else:
        return None


if __name__ == '__main__':
    f = open('true_relations.txt', 'w', encoding='utf-8')
    # f = open('pmi_rel.txt', 'r', encoding='utf-8')
    r = open('relations_with_desc.txt', encoding='utf-8').readlines()
    # relations = []
    # for x in f:
    #     x = x.strip('\n').split(',')
    #     if float(x[0]) > 0.5:
    #         relations.append((x[1], x[2]))
    # for x in relations:
    #     r.write(','.join(x) + '\n')
    a = time()
    with Pool(processes=25) as pool:
        try:
            for x in pool.map(get_true, r):
                if x is not None:

                    f.write(','.join(x) + '\n')
        except Exception:
            raise
    print('time taken ', time()-a)
    f.close()