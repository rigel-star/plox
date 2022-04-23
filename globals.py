from callable import PloxCallable
from math import sqrt
from typing import List

class Sqrt(PloxCallable):
    def call(self, interp, args: List[object]):
        return sqrt(args[0])

    def arity(self):
        return 1
