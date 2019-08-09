import grammar as g

a = g.Symbol.new('a')
b = g.Symbol.new('b')
c = g.Symbol.new('c')
S = g.Symbol.new('S')
p1 = g.Production.from_string('S -> a S')
p2 = g.Production.from_string('S -> b c')
term = set([a, b, c])
nonterm = set([S])
ps = [p1, p2]

G = g.Grammar(term, nonterm, ps, S)
