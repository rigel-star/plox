from interpreter import Interpreter
from environment import Environment
from typing import List
import sys


class ReturnException(Exception):
    def __init__(self, value):
        super().__init__("")
        self.value = value


# callable interface
class PloxCallable:
    def call(self, interp: Interpreter, args: List[object]):
        pass

    def arity(self):
        pass


class PloxFunction(PloxCallable):
    def __init__(self, declare):
        self.declaration = declare

    def call(self, interp: Interpreter, args: List[object]):
        if len(args) != self.arity():
            print(f'Expected {self.arity()} arguments but got {len(args)}');
            sys.exit(10)

        env = Environment(enclosing=interp.globals)

        for i, arg in enumerate(args):
            env.declare(self.declaration.parameters[i].lexeme, arg)

        try:
            interp.execute_block(self.declaration.body, env)
        except ReturnException as e:
            return e.value

        return None


    def arity(self):
        return len(self.declaration.parameters)
