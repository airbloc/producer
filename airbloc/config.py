import json

class Config(dict):

    def __init__(self, path):
        with open(path, 'r') as f:
            super(Config, self).__init__(json.load(f))

    def __getattr__(self, attr):
        return self.get(attr)
