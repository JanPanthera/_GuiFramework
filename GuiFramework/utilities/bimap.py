# GuiFramework/utilities/bimap.py


class BiMap:
    def __init__(self):
        self.forward = {}
        self.reverse = {}

    def get(self, key, default=None):
        return self.forward.get(key, default)

    def reverse_get(self, key, default=None):
        return self.reverse.get(key, default)

    def keys(self):
        return self.forward.keys()

    def values(self):
        return self.forward.values()

    def items(self):
        return self.forward.items()

    def inverse(self):
        return self.reverse

    def __contains__(self, item):
        return item in self.forward or item in self.reverse

    def __setitem__(self, key, value):
        self.forward[key] = value
        self.reverse[value] = key

    def __getitem__(self, key):
        return self.forward.get(key)

    def __delitem__(self, key):
        value = self.forward.get(key)
        if value is not None:
            del self.forward[key]
            del self.reverse[value]

    def __iter__(self):
        return iter(self.forward)

    def __len__(self):
        return len(self.forward)
