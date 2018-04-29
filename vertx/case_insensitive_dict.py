from collections import MutableMapping


class CaseInsensitiveDict(MutableMapping):

    def __init__(self, data=None, **kwargs):
        self._data = {}
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        self._data[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._data[key.lower()][1]

    def __delitem__(self, key):
        del self._data[key.lower()]

    def __iter__(self):
        return (key for key, value in self._data.values())

    def __len__(self):
        return len(self._data)

    def __eq__(self, data):
        if isinstance(data, self.__class__):
            return self.to_normalized_dict() == data.to_normalized_dict()
        else:
            return self.to_dict() == data

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return dict(self._data.values())

    def to_normalized_dict(self):
        return {key.lower(): self[key] for key in self}
