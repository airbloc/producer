
class Identity:

    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self) -> str:
        return 'Identity(type={}, name={})'.format(self.type, self.name)

