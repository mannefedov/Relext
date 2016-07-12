import os

files = [x.strip('.txt') for x in os.listdir('.\\texts\\') if x.endswith('txt')]

for f in files:
    a = open('.\\texts\\' + f + '.txt', encoding='utf-8')
    b = open('.\\clean\\' + f + '.task1', encoding='utf-8')
    b = [x.strip('\n') for x in b]
    ner = [[x.split(' ')[0], int(x.split(' ')[1]), x.split(' ')[2]] for x in b]
    

    index = 0
    for line in a:
        index += len(line)
        for x in ner:
            if x[1] > index:
                x[1] -= 1
    with open('.\\right\\' + f + '.task1', 'w', encoding='utf-8') as new:
        for x in ner:
            new.write(' '.join([str(x[0]), str(x[1]), str(x[2])]) + '\n')
