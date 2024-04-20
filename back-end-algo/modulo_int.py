from modulo import modulo


class MD:
    modulus: int = 2

    def __init__(self, value: int):
        self.value = value % MD.modulus

    def __str__(self):
        return str(self.value)

    def __create2ModObjects(self, other: 'MD'):
        return modulo(self.value, MD.modulus), modulo(other.value, MD.modulus)

    def __add__(self, other: 'MD') -> 'MD':
        _this, _other = MD.__create2ModObjects(self, other)
        return MD(int(_this + _other))

    def __sub__(self, other: 'MD') -> 'MD':
        _this, _other = MD.__create2ModObjects(self, other)
        return MD(int(_this - _other))

    def __mul__(self, other: 'MD') -> 'MD':
        _this, _other = MD.__create2ModObjects(self, other)
        return MD(int(_this * _other))

    def __floordiv__(self, other: 'MD') -> 'MD':
        if other.value == 0:
            raise ZeroDivisionError("_other value equal to 0")
        _this, _other = MD.__create2ModObjects(self, other)
        return MD(int(_this // _other))

    def __truediv__(self, other: 'MD') -> 'MD':
        return MD.__floordiv__(self, other)
