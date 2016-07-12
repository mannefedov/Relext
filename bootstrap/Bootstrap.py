# coding= utf-8
from gensim.models import Word2Vec as w2v
from lxml import etree
from scipy.spatial.distance import cosine as cos

class Instance():
    """Принимает последовательность, возвращает кортеж 
       (bet,tag1,bet,tag2,aft)
    """

    def __init__(self, sent):
        sent = etree.fromstring(sent)
        self.before = ''.join(sent.xpath('..//BEF/text()'))
        self.between = ''.join(sent.xpath('..//BET/text()'))
        self.after = ''.join(sent.xpath('..//AFT/text()'))
        entity_sequence = [x.tag for x in sent.xpath('..//ORG|PER')]
        self.tag1 = ''.join(sent.xpath('.//' + entity_sequence[0] + '/text()'))
        self.tag2 = ''.join(sent.xpath('.//' + entity_sequence[1] + '/text()'))

    def __eq__(self, other):
        if isinstance(other, tuple):
            try:
                if self.tag1 == other[0].decode('utf-8') and \
                   self.tag2 == other[1].decode('utf-8'):
                    return True
                elif self.tag1 == other[1].decode('utf-8') and \
                   self.tag2 == other[0].decode('utf-8'):
                    return True
                else:
                    return False
            except UnicodeEncodeError:
                if self.tag1 == other[0] and \
                   self.tag2 == other[1]:
                    return True
                if self.tag1 == other[1] and \
                   self.tag2 == other[0]:
                    return True
                else:
                    return False
        else:
            if self.tag1 == other.tag1 and \
               self.tag2 == other.tag2:
                return True
            else:
                return False
    def conf(self, seed):
        for s in seed:
            try:
                if self.tag1 == s[0].decode('utf-8') or \
                    self.tag2 == s[1].decode('utf-8'):
                    return True
                elif self.tag1 == s[1].decode('utf-8') or \
                    self.tag2 == s[0].decode('utf-8'):
                    return True
            except UnicodeEncodeError:
                if self.tag1 == s[0] or \
                    self.tag2 == s[1]:
                    return True
                elif self.tag1 == s[1] or \
                    self.tag2 == s[0]:
                    return True  
        else:
            return False

    def get_tuple(self):
        return (self.before, self.tag1, self.between, self.tag2, self.after)

    def get_pair(self):
        return (self.tag1, self.tag2)


class Pattern():

    def __init__(self, inst, model):
        self.model = model
        self.tag1 = inst.tag1
        self.tag2 = inst.tag2
        vec_bef = []
        for x in inst.before.split()[:4:-1]:
            if x.endswith('_S') or x.endswith('_V'):
                try:
                    v = self.model[x]
                    vec_bef.append(x)
                except KeyError:
                    continue
            
        self.vec_bef = vec_bef if vec_bef else None
        # print vec_bef
        vec_bet = []
        for x in inst.between.split():
            if x.endswith('_S') or x.endswith('_V'):
                try:
                    v = self.model[x]
                    vec_bet.append(x)
                except Exception:
                    continue
        self.vec_bet = vec_bet if vec_bet else None
        # print vec_bet
        vec_aft = []
        for x in inst.after.split()[:4]:
            if x.endswith('_S') or x.endswith('_V'):
                try:
                    v = self.model[x]
                    vec_aft.append(x)
                except KeyError:
                    continue
        self.vec_aft = vec_aft if vec_aft else None
        # print vec_aft
        # self.raw_tuple = (bef, bet, aft)
    def sim(self, other):
        a = 0
        if self.vec_bef is not None and other.vec_bef is not None:
            a = self.model.n_similarity(self.vec_bef, other.vec_bef)
        b = 0
        if self.vec_bet is not None and other.vec_bet is not None:
            b = self.model.n_similarity(self.vec_bet, other.vec_bet)
        c = 0
        if self.vec_aft is not None and other.vec_aft is not None:
            c = self.model.n_similarity(self.vec_aft, other.vec_aft)
        return 0.4*a + 0.4*b + 0.2*c

class Pattern_Generator():

    def __init__(self, corpus):
        self.sequence = []
        self.all_found = set()
        self.entities = dict()
        self.corpus = corpus
        self.seed = set()
        self.model = w2v.load_word2vec_format('news_vectors.bin', binary=True)
        self.candidate_patterns = []
    def update_seed(self, new_seed):
        self.sequence = []
        self.seed.update(new_seed)
        for inst in self.corpus:
            for x in self.seed:
                if inst == x:
                    self.sequence.append(inst)

    def vectorize(self):
        self.patterns = []
        for inst in self.sequence:
            self.patterns.append(Pattern(inst, self.model))

    def clusterize(self, alpha):
        new_patterns = [[self.patterns[0]]]
        for i in self.patterns[1:]:
            # print new_patterns
            for j in new_patterns:
                maxsim = 0
                for x in j:
                    s = i.sim(x)
                    if s > maxsim:
                        maxsim = s
                
                if maxsim > alpha:
                    new_patterns[new_patterns.index(j)].append(i)
                    break
            else:
                new_patterns = [[i]] + new_patterns
        print 'got {} clusters'.format(len(new_patterns))
        stack = []
        if self.candidate_patterns:
            for cl_new in new_patterns:
                maxsim = 0
                best_cl = None
                for i in cl_new:
                    for cl_old in self.candidate_patterns:
                        for j in cl_old[0]:
                            s = i.sim(j)
                            if s > maxsim:
                                maxsim = s
                                best_cl = cl_old
                if maxsim > alpha:
                    self.candidate_patterns[self.candidate_patterns.index(best_cl)][0] += cl_new
                else:
                    stack.append([cl_new,0,0,0])
            if stack:
                self.candidate_patterns += stack 
        else:
            self.candidate_patterns += [[x,0,0,0] for x in new_patterns]


    def find_pairs(self, sim_alpha=0.5):
        import codecs
        good = []
        for inst in self.corpus:
            pattern = Pattern(inst, self.model)
            simbest = 0
            pbest = 0
            for cluster in self.candidate_patterns:
                maxsim = 0
                for i in cluster[0]:
                    n = pattern.sim(i) 
                    if n > maxsim:
                        maxsim = n
                
                if maxsim > sim_alpha:
                    if inst.get_pair() in self.seed:
                        self.candidate_patterns[self.candidate_patterns.index(cluster)][1] += 1
                    elif inst.conf(self.seed):
                        self.candidate_patterns[self.candidate_patterns.index(cluster)][2] += 1
                    else:
                        self.candidate_patterns[self.candidate_patterns.index(cluster)][3] += 1
                    if maxsim > simbest:
                        simbest = maxsim
                        pbest = self.candidate_patterns.index(cluster)
                    if self.entities.get(inst.get_pair()) is not None:
                        self.entities[inst.get_pair()].append((self.candidate_patterns[pbest], simbest))
                    else:
                        self.entities[inst.get_pair()] = [(self.candidate_patterns[pbest], simbest)]
        # print 'found {0} self.entities  :\n{1}'.format(len(self.entities), self.entities.keys())
        # a = codecs.open('found_all.txt', 'w', encoding='utf-8')
        # print 'writing test result'
        # for i in self.entities:
        #     try:
        #         a.write(i[0].decode('utf-8') + ' ' + i[1].decode('utf-8') + '\n')
        #     except UnicodeEncodeError:
        #         a.write(i[0] + ' ' + i[1] + '\n')
        # a.close()    
               
        for e in self.entities:
            confidence = 1
            for x in self.entities[e]:
                p_conf = (x[0][1] / (x[0][1] + (2 * x[0][2]) + (0.1*x[0][3]))) if x[0][1] > 0 else 1

                # print 'p_conf - {}'.format(p_conf)
                sim_c = x[1]
                # print 'sim_c - {}'.format(sim_c)
                confidence *= (1 - (p_conf*sim_c))
            confidence = 1 - confidence
            print 'confidence = {}'.format(confidence)
            if confidence > 0.3:
                good.append(e)
                self.all_found.add((e, str(confidence)))
        a = codecs.open('found.txt', 'w', encoding='utf-8')
        print 'writing result'
        for i in self.all_found:
            try:
                a.write(i[0][0].decode('utf-8') + ' ' + i[0][1].decode('utf-8') + i[1].decode('utf-8') + '\n')
            except UnicodeEncodeError:
                a.write(i[0][0] + ' ' + i[0][1] + i[1] + '\n')
        a.close()
                # print 'another good one'

        print 'found {} good entities'.format(len(good))

        return good

def main():
    import codecs
    text = codecs.open('corpus.txt', encoding='utf-8').readlines()
    instance_seq = []
    seed = set([('павел дуров', 'telegram'), ('алексей венедиктов', "эхо москва"), ('герман греф', 'сбербанк')])
    print 'loading instances ...'
    for line in text:
        instance_seq.append(Instance(line))
    print 'generating patterns ...'
    p = Pattern_Generator(instance_seq)
    print 'starting iteration...'
    
    for i in range(3):
        print 'Iteration {0}'.format(i) 
        p.update_seed(seed)
        p.vectorize()
        print 'clustering...'
        p.clusterize(0.5)
        print 'extracting pairs'
        seed.update(p.find_pairs())

    # a = codecs.open('found.txt', 'w', encoding='utf-8')
    # print 'writing result'
    # for i in p.all_found:
    #     try:
    #         a.write(i[0][0].decode('utf-8') + ' ' + i[0]][1].decode('utf-8') + i[1].decode('utf-8') + '\n')
    #     except UnicodeEncodeError:
    #         a.write(i[0][0] + ' ' + i[0][1] + i[1] + '\n')
    # a.close()

if __name__ == '__main__':
    main()
