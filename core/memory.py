class Memory:
    _store = {}

    @classmethod
    def set(cls, key, value):
        cls._store[key] = value

    @classmethod
    def update(cls, key, value):
        if key not in cls._store:
            cls._store[key] = {}
        cls._store[key].update(value)

    @classmethod
    def get(cls, key):
        return cls._store.get(key)

    @classmethod
    def get_all(cls):
        return cls._store

    @classmethod
    def clear(cls):
        cls._store = {}
