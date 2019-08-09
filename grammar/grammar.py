import argparse
import json
import re
from symbol import EmptySymbol, Symbol


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    return parser.parse_args()


class Grammar:
    def __init__(self, terminals, nonterminals, productions, axiom):
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.alphabet = terminals | nonterminals
        self.productions = productions
        self.axiom = axiom
        self.verify()

    def __repr__(self):
        return 'Grammar<T={term}, N={nonterm}, P={prod}, S={ax}>'.format(
            term=repr(self.terminals),
            nonterm=repr(self.nonterminals),
            prod=repr(self.productions),
            ax=repr(self.axiom))

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as f:
            spec = json.load(f)
        terms = spec.get('T')
        nonterms = spec.get('N')
        prods = spec.get('P')
        axiom = spec.get('S')
        if None in [terms, nonterms, prods, axiom]:
            raise ValueError('Incompatible specification')
        terms = set(map(Symbol.new, terms))
        nonterms = set(map(Symbol.new, nonterms))
        prods = list(map(Production.from_string, prods))
        axiom = Symbol.new(axiom)
        return cls(terms, nonterms, prods, axiom)

    def verify(self):
        assert not self.terminals.intersection(self.nonterminals), \
            'Terminals and nonterminals must not intersect'
        assert self.axiom in self.nonterminals, 'Axiom must be a nonterminal'
        for production in self.productions:
            assert set(production.source.sequence +
                       production.product.sequence).issubset(self.alphabet), \
                'Unknown symbol in production {}'.format(production)

    def pretty_print(self):
        lines = []
        lines.append('Terminals:')
        terms = ', '.join(list(map(str, self.terminals)))
        lines.append(' ' * 2 + '{}'.format(terms))
        nonterms = map(str, self.nonterminals)
        nonterms = map(lambda x: x + '(Ax)' if x == self.axiom else x,
                       nonterms)
        nonterms = ', '.join(list(nonterms))
        lines.append('Non-terminals:')
        lines.append(' ' * 2 + '{}'.format(nonterms))
        lines.append('Productions:')
        for production in self.productions:
            lines.append(' ' * 2 + str(production))
        return '\n'.join(lines)


class Production:
    DELIM = '->'
    __slots__ = ('source', 'product')

    def __init__(self, source, product):
        self.source = source
        self.product = product

    def __str__(self):
        return '{source} -> {product}'.format(source=self.source,
                                              product=self.product)

    def __repr__(self):
        return 'Production<{}>'.format(str(self))

    @classmethod
    def from_string(cls, string):
        if cls.DELIM not in string:
            raise SyntaxError('Invalid production syntax')
        left, right = string.split(cls.DELIM, 1)
        source = Word.from_string(left)
        product = Word.from_string(right)
        return cls(source, product)


class Word:
    __slots__ = ('sequence', 'value')

    def __init__(self, symbols):
        self.sequence = symbols
        self.value = ''.join(list(map(str, symbols)))

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'Word<{}>'.format(', '.join(list(map(repr, self.sequence))))

    def __getitem__(self, val):
        if isinstance(val, int):
            return self.sequence[val]
        return Word.new(self.sequence[val])

    @classmethod
    def new(cls, symbols):
        if list(filter(lambda x: not isinstance(x, Symbol), symbols)):
            raise TypeError('Word can be built only from Symbols')
        symbols = list(
            filter(lambda x: not isinstance(x, EmptySymbol), symbols))
        if not symbols:
            return EmptyWord()
        return cls(symbols)

    @classmethod
    def from_string(cls, string):
        return cls.new(list(map(Symbol.new, string.split())))


class EmptyWord(Word):
    def __init__(self):
        super().__init__([])


if __name__ == "__main__":
    args = parse_args()
    G = Grammar.from_json(args.path)
