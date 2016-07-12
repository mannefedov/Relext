from lxml import etree
from pymystem3 import Mystem


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
        print(len(result_full), ' разобралось')
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
    lmtze('all_per_org_pairs.txt')