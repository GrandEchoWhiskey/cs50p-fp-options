import sys

DEFAULT_PREFIX = '-'

default_set = set()

class opt:

    def __init__(self, long: str, *short, oset: set = default_set) -> None:
        self.__long: str = long
        self.__shorts: list = short
        oset.add(self)

    def __str__(self) -> str: return self.__long

    def __hash__(self) -> int: return hash(self.__long)

    def __iter__(self): return iter(self.__shorts)

    def __next__(self): return next(self.__shorts)


class translation:

    def __init__(self, args: list = sys.argv, prefix: str = DEFAULT_PREFIX, oset: set = default_set) -> None:
        self.__p_args: list = [] # Args after "python"
        self.__d_args: dict = {} # Args after a decorated option "-x" for example
        self.__set: set = oset
        self.__prefix: str = prefix
        self._translate(args)
        self._replace_to_long(self.__d_args)

    def _translate(self, __args: list) -> None:
        __last_key: str | None = None
        for __i in __args:
            if __i.startswith(self.__prefix):
                __last_key = __i
                if __i not in self.__d_args.keys():
                    self.__d_args[__i] = []
            elif __last_key:
                self.__d_args[__last_key].append(__i)
            else:
                self.__p_args.append(__i)

    def _replace_to_long(self, __d_args: dict) -> None:
        __cpy = list(__d_args.keys()).copy()
        for __key in __cpy:
            if __key.startswith(2*self.__prefix): continue
            if not __key.startswith(self.__prefix): continue
            for __item in self.__set:
                for __short in __item:
                    if __short == __key[1:]:
                        __d_args[2*self.__prefix + str(__item)] = __d_args.pop(__key)

    def update(self): self._replace_to_long(self.__d_args)

    def _pref(self, key: str) -> str: return 2*self.__prefix + key

    def isset(self, key: str) -> bool: return self._pref(key) in self.__d_args.keys()

    def len(self, key: str) -> int: return len(self.__d_args[self._pref(key)]) if self.isset(key) else -1

    def values(self, key: str) -> list:
        if self.len(key) < 0: return None
        return self.__d_args[self._pref(key)]

    @property
    def p_args(self) -> list: return self.__p_args

    @property
    def d_args(self) -> dict: return self.__d_args

    @property
    def oset(self) -> set: return self.__set

default_translation = translation()

def option(long: str, *shorts, tsl: translation = default_translation):

    opt(long, *shorts, oset=tsl.oset)
    tsl.update()

    def decorator(func):

        def wrapper(*args, **kwargs):

            if tsl.values(long) is None:
                return False

            def modifier(*args, **kwargs):
                result = func(*args, **kwargs)
                return True if result is None else result

            nargs = list(args) + tsl.values(long)
            return modifier(*nargs, **kwargs)

        return wrapper

    return decorator

class var:

    def __init__(self, value):
        self.__call__(value)

    def __invert__(self):
        return self.__value

    def __call__(self, value):
        self.__value = value

opt('alpha', 'a')
opt('bravo', 'b')

@option('alpha')
def test(some_x, some_y, some_z=1):
    print(some_x, some_y, some_z)
    return int(some_x)*int(some_y)*int(some_z)

@option('bravo')
def test2(x, y):
    print(x, y)

if x := test(10, 10):
    test2(x)

c = var(100)
b = c
b(10)
print(~c)