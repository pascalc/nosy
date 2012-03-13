class OpenStruct(object):
    def __init__(self, data=None, **kwargs):
        # Merge with kwargs if supplied
        self.__dict__.update(kwargs)
        # On created callback
        self._on_created(data, **kwargs)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __delattr__(self, name):
        del self.__dict__[name]

    def _on_created(self, data, **kwargs):
        pass

    def to_dict(self):
        return self.__dict__
