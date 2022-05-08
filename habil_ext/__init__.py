class Overloadable:
    @classmethod
    def overload(cls, *args, **kwargs) -> 'Overloadable':
        return cls(*args, **kwargs)