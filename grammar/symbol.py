import re


class Symbol:
    __slots__ = ('value')

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'Symbol<{}>'.format(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            raise ValueError

    @classmethod
    def new(cls, value):
        if not isinstance(value, str):
            raise TypeError('Only strings can be assigned to a Sybmol')
        if not re.fullmatch(r'\w*', value):
            raise ValueError('Unsupported charecters in token')
        if not value:
            return EmptySymbol()
        return cls(value)


class EmptySymbol(Symbol):
    def __init__(self):
        super().__init__('')
