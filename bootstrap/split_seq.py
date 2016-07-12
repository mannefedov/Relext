from lxml import etree


def main():
    """Принимает лемматизированные последовательности, в которых
       встречаются нужные пары тэгов.
       Разбивает их на последовательности вида <BEF><TAG1><BET><TAG2>,<AFT>
       т.е. оставляет только 2 различных тега. Последовательности с 
       большим количеством тегэв разбиваются несколько с 2 тэгами.

    """
    text = open('corpus.txt', encoding='utf-8').readlines()
    result = []
    for line in text:
        a = line[:]
        try:
            line = line.strip('\n')
            line = etree.fromstring(line)
            e = [x.tag for x in line.xpath('*')]
            entities = line.xpath('*')
            seq = line.xpath('text()')
            good_pairs = [(i, e[i], e[i+1]) for i in range(len(e)-1) if e[i] != e[i+1]]
            for pair in good_pairs:
              i = pair[0]
              tup = [seq[i:i+1],
                     '<' + entities[i].tag + '>' + entities[i].text + '</' + entities[i].tag + '>',
                     seq[i+1:i+2],
                     '<' + entities[i+1].tag + '>' + entities[i+1].text + '</' + entities[i+1].tag + '>',
                     seq[i+2:i+3]]
              result.append(tup)
        except TypeError:
            continue
    with open('all_2_pairs_lem.txt', 'w', encoding='utf-8') as text:
        for x in result:
            text.write('<sent>')
            text.write(''.join(['<BEF>', ''.join(x[0]), '</BEF>']))
            text.write(''.join(x[1]))
            text.write(''.join(['<BET>', ''.join(x[2]), '</BET>']))
            text.write(''.join(x[3]))
            text.write(''.join(['<AFT>', ''.join(x[4]), '</AFT>']))
            text.write('</sent>\n')

if __name__ == '__main__':
    main()

