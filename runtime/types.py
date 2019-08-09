class Expression:
    def __init__(self, rawexp: str):
        self.rawexp = rawexp
        self.parse()

    def __repr__(self):
        return '<{type} \'{expr}\'>'.format(
            type=self.__class__.__name__,
            expr=self.rawexp)

    def parse(self):
        pass

    def evaluate(self):
        pass


class FutureInt(Expression, int):
    pass


class FutureString(Expression, str):
    pass


class FutureBool(Expression):
    pass
