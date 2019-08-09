from typing import Any, Callable, List

from runtime.types import FutureBool, FutureInt, FutureString


class Node:
    '''Represents a node in specification tree.'''

    @property
    def childs(self) -> List['Node']:
        raise NotImplementedError

    _attrs: List = []

    @classmethod
    def attrs(cls):
        return cls._attrs

    @property
    def type(self):
        return self.__class__.__name__

    def __str__(self):
        return '<{}>'.format(self.type)

    def __repr__(self):
        return '<{type} {attrs}>'.format(
            type=self.__class__.__name__,
            attrs=', '.join(['{}={}'.format(attr, str(getattr(self, attr)))
                             for attr in self.attrs()]))

    def traverse(self, callback: Callable[['Node'], Any]):
        for child in self.childs:
            callback(child)
            child.traverse(callback)

    def to_json(self):
        def _to_json(node):
            return {
                'type': node.type,
                'attrs': {attr: str(getattr(node, attr))
                          for attr in node.attrs()},
                'childs': [_to_json(child) for child in node.childs]
            }

        return _to_json(self)


class Value(Node):
    '''Represents raw byte sequence.

    Refers to words (terminal sequences).
    '''

    _attrs = ['length', 'endianness']

    def __init__(self, length: FutureInt, endianness: FutureString = 'big'):
        self.length = length
        self.endianness = endianness

    @property
    def childs(self):
        return []


class Type(Node):
    '''Represents structured type.

    Refers to nonterminal symbol.
    '''

    _attrs = ['name']

    def __init__(self, name: str, struct: List[Node]):
        self.name = name
        self.struct = struct

    @property
    def childs(self):
        return self.struct


class OptionalType(Type):

    _attrs = ['name', 'condition']

    def __init__(self, name: str, struct: List[Node], condition: FutureBool):
        super().__init__(name, struct)
        self.condition = condition


class Select(Node):
    def __init__(self, variants: List[Node]):
        self.variants = variants

    @property
    def childs(self):
        return self.variants


class Repeat(Node):
    '''Represents repeated structure.

    Refers to recursion in grammar.
    '''

    def __init__(self, body: Node):
        self.body = body

    @property
    def childs(self):
        return [self.body]


class RepeatCount(Repeat):
    '''Represents structure, repeated specified times.'''

    _attrs = ['count']

    def __init__(self, body: Node, count: FutureInt):
        super().__init__(body)
        self.count = count


class RepeatUntil(Repeat):
    _attrs = ['delimiter']

    def __init__(self, body: Node, delimiter: Value):
        super().__init__(body)
        self.delimiter = delimiter


if __name__ == "__main__":
    import json

    t1 = Type('mytype', [Value(FutureInt('1')), Value(FutureInt('3'))])
    t2 = RepeatCount(t1, FutureInt('3'))

    t3 = OptionalType('opttype', [Value(FutureInt('4'))], FutureBool('true'))
    t4 = Select([t3, t1])

    t5 = Type('magic', [Value(FutureInt('2'))])

    t5 = Type('big', [t5, t2, t4])

    print(
        json.dumps(t5.to_json(), indent=4)
    )
