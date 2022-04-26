from typing import List, Dict, Tuple
from enum import Enum

had_error: bool = False

class TokenType(Enum):
	# single character tokens
	LEFT_PAREN = 0
	RIGHT_PAREN = 1
	LEFT_BRACE = 2
	RIGHT_BRACE = 3
	COMMA = 4
	DOT = 5
	MINUS = 6
	PLUS = 7
	SEMICOLON = 8
	SLASH = 9
	STAR = 10
	NEGATE = 11
	BIT_AND = 12
	BIT_OR = 13
	BIT_NEGATE = 14
	BIT_XOR = 15

	# TODO: % operator

	# one or two character tokens
	NOT = 16
	NOT_EQUAL = 17
	EQUAL = 18
	EQUAL_EQUAL = 19
	GREATER = 20
	GREATER_EQUAL = 21
	BIT_SHIFT_RIGHT = 24
	LESS = 22
	LESS_EQUAL = 23
	BIT_SHIFT_LEFT = 25

	# literals
	IDENTIFIER = 26
	STRING = 27
	NUMBER = 28

	# keywords
	AND = 29
	OBJECT = 30
	ELSE = 31
	FALSE = 32
	FUN = 33
	FOR = 34
	IF = 35
	NIL = 36
	OR = 37
	PRINT = 38
	RETURN = 39
	SUPER = 40
	THIS = 41
	TRUE = 42
	VAR = 43
	WHILE = 44
	EOF = 45
	ENUM = 46


KEYWORDS = {
	'and': TokenType.AND,
	'or': TokenType.OR,
	'object': TokenType.OBJECT,
	'if': TokenType.IF,
	'else': TokenType.ELSE,
	'true': TokenType.TRUE,
	'false': TokenType.FALSE,
	'var': TokenType.VAR,
	'fun': TokenType.FUN,
	'for': TokenType.FOR,
	'nil': TokenType.NIL,
	'print': TokenType.PRINT,
	'return': TokenType.RETURN,
	'super': TokenType.SUPER,
	'this': TokenType.THIS,
	'while': TokenType.WHILE,
	'enum': TokenType.ENUM
}


class Token:
	def __init__(self, tok_type: TokenType, lexeme: str, literal: object, line: int):
		self.token_type = tok_type
		self.lexeme = lexeme
		self.literal = literal
		self.line = line

	def __str__(self):
		return f"{self.token_type} {self.lexeme} {self.literal}"


class Scanner:
	def __init__(self, source: str):
		self.source: str = source
		self.tokens: List[Token] = list()
		self.current = 0
		self.start = 0
		self.line = 1

	def scan_tokens(self):
		while not self.is_at_end():
			self.start = self.current
			self.scan_token()

		_eof = Token(TokenType.EOF, "", None, self.line)
		self.tokens.append(_eof)
		return self.tokens

	def scan_token(self):
		c = self.advance()

		if c == "(":
			self.add_token(TokenType.LEFT_PAREN)

		elif c == ")":
			self.add_token(TokenType.RIGHT_PAREN)

		elif c == "{":
			self.add_token(TokenType.LEFT_BRACE)

		elif c == "}":
			self.add_token(TokenType.RIGHT_BRACE)

		elif c == ",":
			self.add_token(TokenType.COMMA)

		elif c == ".":
			self.add_token(TokenType.DOT)

		elif c == "-":
			self.add_token(TokenType.MINUS)

		elif c == "+":
			self.add_token(TokenType.PLUS)

		elif c == ";":
			self.add_token(TokenType.SEMICOLON)

		elif c == "*":
			self.add_token(TokenType.STAR)

		elif c == "&":
			self.add_token(TokenType.BIT_AND)

		elif c == "|":
			self.add_token(TokenType.BIT_OR)

		elif c == "^":
			self.add_token(TokenType.BIT_XOR)

		elif c == "~":
			self.add_token(TokenType.BIT_NEGATE)

		elif c == "!":
			if self.match("="):
				self.add_token(TokenType.NOT_EQUAL)
				self.advance()
			else:
				self.add_token(TokenType.NOT)

		elif c == "<":
			if self.match("="):
				self.add_token(TokenType.LESS_EQUAL)
				self.advance()
			elif self.match("<"):
				self.add_token(TokenType.BIT_SHIFT_LEFT)
				self.advance()
			else:
				self.add_token(TokenType.LESS)

		elif c == ">":
			if self.match("="):
				self.add_token(TokenType.GREATER_EQUAL)
				self.advance()
			elif self.match(">"):
				self.add_token(TokenType.BIT_SHIFT_RIGHT)
				self.advance()
			else:
				self.add_token(TokenType.GREATER)

		elif c == "=":
			if self.match("="):
				self.add_token(TokenType.EQUAL_EQUAL)
				self.advance()
			else:
				self.add_token(TokenType.EQUAL)

		elif c == "/":
			if self.match("*"):
				self.advance()
				while self.peek() != '*' and self.peek_next() != '/' and not self.is_at_end():
					if self.peek() == '\n':
						self.line += 1
					self.advance()

				if self.is_at_end():
					print(f'[line {self.line}]: Error: Unterminated multiline comment')

				self.advance() # for *
				self.advance() # for /
			elif self.match("/"):
				self.advance()
				while self.peek() != '\n' and not self.is_at_end():
					self.advance()
			else:
				self.add_token(TokenType.SLASH)

		elif c == '\n':
			self.line += 1

		elif c == '"':
			while self.peek() != '"' and not self.is_at_end():
				if self.peek() == '\n':
					self.line += 1
				self.advance()

			if self.is_at_end():
				print(f"[line {self.line}]: Error: Unterminated string")
				return

			self.advance() # advancing the closing "
			self.add_token(TokenType.STRING, self.source[self.start + 1: self.current - 1])

		elif c.isdigit():
				while self.peek().isdigit():
					self.advance()
				if self.peek() == '.' and self.peek_next().isdigit():
					self.advance()
					while self.peek().isdigit():
						self.advance()
					self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
				else:
					self.add_token(TokenType.NUMBER, int(self.source[self.start:self.current]))

		elif c.isalpha() or c == "_":
			while self.peek().isalnum() or self.peek() == "_":
				self.advance()
			text = self.source[self.start:self.current]
			typ = KEYWORDS.get(text)
			if typ is None:
				typ = TokenType.IDENTIFIER
			self.add_token(typ)

		else:
			if c == ' ' or '\r' or '\t':
				return
			else:
				print(f"[line: {self.line}]: Error: Unexpected character")


	def advance(self):
		result = self.source[self.current] if self.current < len(self.source) else '\0'
		self.current += 1
		return result


	def match(self, ch):
		return not self.is_at_end() and ch == self.source[self.current]


	def peek(self):
		return '\0' if self.is_at_end() else self.source[self.current]


	def peek_next(self):
		return self.source[self.current + 1] if (self.current + 1) < len(self.source) else '\0'


	def add_token(self, token_type, literal=None):
		lexeme = self.source[self.start:self.current]
		token = Token(token_type, lexeme, literal, self.line)
		self.tokens.append(token)


	def is_at_end(self):
		return self.current >= len(self.source)
