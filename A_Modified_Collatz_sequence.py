class Frac(object):
    def __init__(self, a, b, c):
        self.a = 1
        self.b = 0
        self.c = 1

    def _parse(self, char):
        self.c *= 3
        if char == 'U':
            self.a *= 4
            self.b = 4 * self.b + 2 * self.c
        elif char == 'd':
            self.a *= 2
            self.b = 2 * self.b - self.c

    def parse(self, string):
        for char in string:
            self._parse(char)
        print(self.a, self.b, self.c)
