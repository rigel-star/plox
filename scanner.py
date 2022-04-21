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

	# one or two character tokens
	NOT = 11
	NOT_EQUAL = 12
	EQUAL = 13
	EQUAL_EQUAL = 14
	GREATER = 15
	GREATER_EQUAL = 16
	LESS = 17
	LESS_EQUAL = 18

	# literals
	IDENTIFIER = 19
	STRING = 20
	NUMBER = 21

	# keywords 
	AND = 22
	CLASS = 23
	ELSE = 24
	FALSE = 25
	FUN = 26
	FOR = 27
	IF = 28
	NUL = 29
	OR = 30
	PRINT = 31
	RETURN = 32
	SUPER = 33
	THIS = 34
	TRUE = 35
	VAR = 36
	WHILE = 37
	EOF = 38


KEYWORDS = {
	'and': TokenType.AND, 
	'or': TokenType.OR, 
	'class': TokenType.CLASS, 
	'if': TokenType.IF,
	'else': TokenType.ELSE,
	'true': TokenType.TRUE,
	'false': TokenType.FALSE,
	'var': TokenType.VAR,
	'fun': TokenType.FUN,
	'for': TokenType.FOR,
	'nul': TokenType.NUL,
	'print': TokenType.PRINT,
	'return': TokenType.RETURN,
	'super': TokenType.SUPER,
	'this': TokenType.THIS,
	'while': TokenType.WHILE
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
		elif c == "!":
			self.add_token(TokenType.NOT_EQUAL if self.match("=") else TokenType.NOT)
		elif c == "<":
			self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
		elif c == ">":
			self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
		elif c == "=":
			self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
		elif c == "/":
			if self.match("/"):
				while self.peek() != '\n' and not self.is_at_end():
					self.advance()
			elif self.match('*'):
				while self.peek() != '*' and self.peek_next() != '/':
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
				self.add_token(TokenType.NUMBER, self.source[self.start:self.current])
		elif c.isalpha() or c == "_":
			while self.peek().isalnum():
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
		result = self.source[self.current]
		self.current += 1
		return result

	def match(self, ch):
		result = not self.is_at_end() and ch == self.source[self.current]
		self.current += 1
		return result

	def peek(self):
		return '\0' if self.is_at_end() else self.source[self.current]

	def peek_next(self):
		return '\0' if (self.current + 1) > len(self.source) else self.source[self.current + 1]

	def add_token(self, token_type, literal=None):
		lexeme = self.source[self.start:self.current]
		token = Token(token_type, lexeme, literal, self.line)
		self.tokens.append(token)

	def is_at_end(self):
		return self.current >= len(self.source)
