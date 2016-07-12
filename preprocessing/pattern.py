import os, re
from collections import Counter
from pprint import pprint
# import subprocess
from pymystem3 import Mystem
from lxml import etree

def entity_finder(name_of_person):
    found = []
    files = [x for x in os.listdir('.\\testset\\') if x.endswith('txt')]
    for f in files:
        try:
            text = open('.\\testset\\' + f, encoding='utf-8').read().lower()
            if text.find(name_of_person) is not -1:
                found.append(f.strip('txt'))
        except Exception as e:
            print(f, e)
    return found, name_of_person


def coentities(files, name_of_person):
    co_enitites = Counter()
    for f in files:
        plain_text = open('.\\testset\\' + f + 'txt', encoding='utf-8').read().lower()
        marked = open('.\\testset\\' + f + 'task1', encoding='utf-8').readlines()
        for entity in marked:
            tag, b, l = entity.split(' ')
            b = int(b)
            l = int(l)
            ent = plain_text[b:b+l]
            if ent != name_of_person and 'ORG' in tag:
                co_enitites.update([(ent)])
    return co_enitites.most_common(10)

def context(files, nop):
    cont = Counter()
    for f in files:
        text = open('.\\testset\\' + f + 'txt', encoding='utf-8').read().lower().split('\n')
        text = [x.split('. ') for x in text]
        for line in text:
            for sent in line:
                if nop in sent:
                    for s in sent.split():
                        s = s.strip(',').strip('.')
                        if len(s) > 3 and s not in nop:
                            cont.update([s])
    return cont.most_common(10)


def get_pairs():
    found = []
    files = sorted([int(x.strip('.txt')) for x in os.listdir('.\\texts\\') if x.endswith('txt')])
    for f in files:
        print('reading: ', f)
        try:
            text = open('.\\texts\\' + str(f) + '.txt', encoding='utf-8').read().lower()
            marked = open('.\\right\\' + str(f) + '.task1', encoding='utf-8').readlines()
        except Exception:
            continue
        ner = sorted([(int(x.split(' ')[1]), x.split(' ')[0], int(x.split(' ')[2])) for x in marked])
        
        i = 0
        for ne in ner:
            if 'LOC' in ne[1]:
                continue
            text = ''.join([text[:ne[0]+i],  # text before
                            '<', ne[1][:3], '>',  # tag opening
                            text[ne[0]+i:ne[0]+ne[2]+i],   # entity
                            '</', ne[1][:3], '>',  # tag closing
                            text[ne[0]+ne[2]+i:]])  # rest of the text
            i += 11
        text = text.split('\n')
        for sent in text:
            if 'PER' in sent and 'ORG' in sent:
                found.append(''.join(['<sent>', sent, '</sent>']))
    return found

def lmtze(textfile):
    m = Mystem()
    text = open(textfile, encoding='utf-8').readlines()
    newfile = open(textfile.replace('txt', 'lem.txt'), 'w', encoding='utf-8')
    result_full = []
    for line in text:
        try:
            element = etree.fromstring(line.strip('\n'))
            text_ = element.xpath('text()')
            entities = element.xpath('*')
            result = ['<sent>']
            while text_:
                l = text_.pop(0)
                # open('temp.txt', 'w', encoding='utf-8').write(l)
                # subprocess.call(['C:\\Mystem\\mystem', 'i'])
                l = m.analyze(l)
                # print(l)
                for x in l:
                    if x.get('analysis') is not None:
                        if x.get('analysis') == []:
                            result.append(x['text'])
                        else:
                            result.append(x['analysis'][0]['lex'] + '_' + x['analysis'][0]['gr'].split(',')[0].split('=')[0])
                    else:
                        continue

                if text_:
                    e = entities.pop(0)
                    e_ = m.analyze(e.text)
                    result.append('<' + e.tag + '>')
                    for x in e_:
                        if x.get('analysis') is not None:
                            if x.get('analysis') == []:
                                result.append(x['text'])
                            else:
                                result.append(x['analysis'][0]['lex'])
                        else:
                            continue
                    result.append('</' + e.tag + '>')
        except Exception:
            continue
        result.append('</sent>')
        result_full.append(result)
        result = []
        print(len(text) - len(result_full), ' осталось разобрать')
    for sent in result_full:
        prev = ''
        for x in sent:
            if '<' in x and '/' not in x:
                newfile.write(prev + x)
                prev = ''
            elif '_' in x or x.isalpha():
                newfile.write(prev + x)
                prev = ' '
            else:
                newfile.write(x)
        newfile.write('\n')



if __name__ == '__main__':
    # files, nop = entity_finder('алексей венедиктов')
    # print('----- ', nop, '-------\n', file=open('report.txt', 'a', encoding='utf-8'))
    # pprint(coentities(files, nop), stream=open('report.txt', 'a', encoding='utf-8'))
    f = open('all_per_org_pairs.txt', 'w', encoding='utf-8')
    # f.write('<DOC>' + '\n')
    for x in get_pairs():
        x = x.replace('<ORG></PER></ORG>', '</PER>')
        x = x.replace('<<ORG>/PER></ORG>', '/PER>')

        x = x.replace('<PER></ORG></PER>', '</ORG>')
        x = x.replace('<<PER>/ORG></PER>', '</ORG>')
        if re.match(r'</(PER|ORG)></(PER|ORG)>', x) or re.match(r'<(PER|ORG)>[A-Za-zА-Яа-яЁё]{0,10}</(PER|ORG)></(PER|ORG)>', x):
            continue
        else:
            f.write(x + '\n')
    # f.write('</DOC>')
    f.close()


