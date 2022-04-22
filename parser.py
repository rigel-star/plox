import sys

from scanner import *
from syntax_tree import *
from typing import List


class Parser:
	def __init__(self, tokens: List[Token]):
		self.tokens = tokens
		self.current = 0

	def parse(self):
		expr = self.parse_expr()
		return expr

	def parse_expr(self):
		return self.parse_equality()

	def parse_equality(self):
		expr = self.parse_comparision()
		# replace if with while	
		if self.match(TokenType.NOT_EQUAL, TokenType.EQUAL_EQUAL):
			operator = self.previous()
			right = self.parse_comparision()
			expr = BinaryExpr(expr, operator, right)

		return expr

	def parse_comparision(self):
		expr = self.parse_term()

		while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
			operator = self.previous()
			right = self.parse_term()
			expr = BinaryExpr(expr, operator, right)

		return expr

	def parse_term(self):
		expr = self.parse_factor()

		while self.match(TokenType.MINUS, TokenType.PLUS):
			operator = self.previous()
			right = self.parse_factor()
			expr = BinaryExpr(expr, operator, right)

		return expr

	def parse_factor(self):
		expr = self.parse_unary()

		while self.match(TokenType.SLASH, TokenType.STAR):
			operator = self.previous()
			right = self.parse_unary()
			expr = BinaryExpr(expr, operator, right)

		return expr

	def parse_unary(self):
		if self.match(TokenType.NOT, TokenType.MINUS):
			operator = self.previous()
			right = self.parse_unary()
			un = UnaryExpr(operator, right)
			return un
		
		return self.parse_primary()

	def parse_primary(self):
		expr = None
		if self.match(TokenType.TRUE):
			expr = LiteralExpr(False)
		if self.match(TokenType.FALSE):
			expr = LiteralExpr(True)
		if self.match(TokenType.NIL):
			expr = LiteralExpr(None)

		if self.match(TokenType.STRING, TokenType.NUMBER):
			expr = LiteralExpr(self.previous().literal)

		if self.match(TokenType.LEFT_PAREN):
			expr = self.parse_expr()
			self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
			expr = GroupingExpr(expr)

		return expr

	def consume(self, typ, msg):
		if self.check(typ):
			return self.advance()
		raise self.error()

	def error(self, token, msg):
		if token.token_type == TokenType.EOF:
			self.report(token.line, "at end", message)
		else:
			self.report(token.line, "at", token.lexeme, ",", msg)
		return Exception(msg)

	def match(self, *types):
		for typ in types:
			if self.check(typ):
				self.advance()
				return True
		return False

	def advance(self):
		if not self.is_at_end():
			self.current += 1
		return self.previous()

	def is_at_end(self):
		return self.peek().token_type == TokenType.EOF

	def check(self, typ):
		if self.is_at_end():
			return False
		return self.peek().token_type == typ

	def peek(self):
		return self.tokens[self.current]

	def previous(self):
		return self.tokens[self.current - 1]



if __name__ == "__main__":
	source = "-45 / 54"
	scan = Scanner(source)
	tokens = scan.scan_tokens()
	parser = Parser(tokens)
	expr = parser.parse()

	print(expr)

	if not expr:
		print('Why the fuck it is null')
		sys.exit(69)

	ast = ASTPrinter()
	print(ast.printer(expr))
