

system = set()
system2 =set()
for x in open('new.txt', encoding='utf-8'):
	try:
		a = (x.strip('\n').split(',')[0], x.strip('\n').split(',')[1]) if float(x.strip('\n').split(',')[2]) > 0.93 else None
		if a is not None:
			b = (a[1], a[0])
		else:
			continue
	except Exception:
		print(x)
		raise
	system.add(a)
	system2.add(b)



g = set([tuple(x.strip('\n').split(',')) for x in open('not_found_true.txt', encoding='utf-8')])
bd = set([tuple(x.strip('\n').split(',')) for x in open('ceos.txt', encoding='utf-8')])
system = system | system2
b = system & bd
a = g & system
a = a - b
c = g & bd
c = c - b

p = (len(a)+len(b))/len(system)
rec = (len(a)+len(b))/(len(a)+len(b)+len(c)+len(g))
f1 = (2*p*rec)/(p+rec)

print(p*100, '% -precision')
print(rec*100, '% -recal')
print(f1*100, '% 1-measure')

# s = open('found.txt', encoding='utf-8')
# new = open('new.txt', 'w', encoding='utf-8')
# for l in s:
#     r = l.strip('\n').split(' ')[:1:-1]
#     if float(r[0]) > 0.6:
#     	new.write(l)