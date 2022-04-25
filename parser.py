import sys
from scanner import *
from syntax_tree import *
from typing import List


class Parser:
	def __init__(self, tokens: List[Token]):
		self.tokens = tokens
		self.current = 0

		# for token in tokens:
		# 	print(token)
		#
		# sys.exit(1)


	def parse(self):
		statements: List[Stmt] = list()

		while not self.is_at_end():
			stmt = self.parse_decl_stmt()
			# print(stmt)
			statements.append(stmt)

		return statements


	def parse_decl_stmt(self):
		if self.match(TokenType.VAR):
			self.advance() # advance to identifier name
			name = self.consume(TokenType.IDENTIFIER, "Expected variable name after var keyword.")

			initialization = None
			if self.match(TokenType.EQUAL):
				self.advance()
				initialization = self.parse_anon_func_expr()

			self.consume(TokenType.SEMICOLON, "Expected ';' after expression. Variable declaration must end with ;.")

			var_stmt = VarDeclareStmt(name.lexeme, initialization)
			return var_stmt

		if self.match(TokenType.FUN):
			self.advance() # advance pass 'fun'
			func_decl = self.parse_func_decl_stmt()
			return func_decl

		return self.parse_stmt()


	def parse_func_decl_stmt(self):
		name = self.consume(TokenType.IDENTIFIER, "Function statements require a function name")
		self.consume(TokenType.LEFT_PAREN, "Expected '(' name")

		params = list()
		if not self.check(TokenType.RIGHT_PAREN):
			params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name inside parenthesis"))

			while self.check(TokenType.COMMA):
				self.advance()
				if len(params) >= 100:
					print("Can't have more than 100 parameters")
					sys.exit(11)

				params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name inside parenthesis"))

		self.consume(TokenType.RIGHT_PAREN, "Expected ')' after parameter(s)")
		self.consume(TokenType.LEFT_BRACE, "Expected '{' before function body")
		body = self.parse_block_stmt()

		func_decl = FunctionDeclStmt(name, params, body)
		return func_decl


	def parse_stmt(self):
		if self.match(TokenType.PRINT):
			self.advance()
			self.consume(TokenType.LEFT_PAREN, "Expected '(' after print statement")
			return self.parse_print_stmt()

		elif self.match(TokenType.LEFT_BRACE):
			self.advance()
			stmts = self.parse_block_stmt()
			block = BlockStmt(stmts)
			return block

		elif self.match(TokenType.IF):
			self.advance()
			self.consume(TokenType.LEFT_PAREN, "Expected '(' before conditional expression")
			condition = self.parse_expr()
			self.consume(TokenType.RIGHT_PAREN, "Expected ')' after conditional expression")

			if_true = self.parse_decl_stmt()
			if_false = None
			if self.match(TokenType.ELSE):
				self.advance()
				if_false = self.parse_decl_stmt()

			if_stmt = IfStmt(condition, if_true, if_false)
			return if_stmt

		elif self.match(TokenType.WHILE):
			self.advance()
			self.consume(TokenType.LEFT_PAREN, "Expected '(' before conditional expression")
			condition = self.parse_expr()
			self.consume(TokenType.RIGHT_PAREN, "Expected ')' after conditional expression")

			body = self.parse_decl_stmt()
			while_stmt = WhileStmt(condition, body)
			return while_stmt

		return self.parse_expr_stmt()


	def parse_block_stmt(self):
		stmts = list()
		while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
			stmts.append(self.parse_decl_stmt())

		self.consume(TokenType.RIGHT_BRACE, "Expected '}' to end block statement")
		return stmts


	def parse_expr_stmt(self):
		expr = self.parse_expr()
		self.consume(TokenType.SEMICOLON, "Expected ';' after expression")
		expr_stm = ExprStmt(expr)
		return expr_stm


	def parse_print_stmt(self):
		expr: Expr = self.parse_expr()
		self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
		self.consume(TokenType.SEMICOLON, "Expected ';' after print statement")
		print_stmt = PrintStmt(expr)
		return print_stmt


	def parse_expr(self):
		return self.parse_anon_func_expr()


	def parse_anon_func_expr(self):
		anon_func = None

		if self.match(TokenType.FUN):
			self.advance()
			self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'fun' keyword in anonymous function expression")

			params = list()
			if not self.check(TokenType.RIGHT_PAREN):
				params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name inside parenthesis"))

				while self.check(TokenType.COMMA):
					self.advance()
					if len(params) >= 100:
						print("Can't have more than 100 parameters")
						sys.exit(11)

					params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name inside parenthesis"))

			self.consume(TokenType.RIGHT_PAREN, "Expected ')' after parameter(s)")
			self.consume(TokenType.LEFT_BRACE, "Expected '{' before function body")
			body = self.parse_block_stmt()

			anon_func = AnonFunctionExpr(params, body)
			return anon_func

		return self.parse_assign_expr()


	def parse_assign_expr(self):
		expr = self.parse_or_expr()
		if self.match(TokenType.EQUAL):
			equals = self.peek()
			self.advance()
			value = self.parse_assign_expr()

			if isinstance(expr, VariableExpr):
				identifier_token = expr.name
				assign = AssignExpr(identifier_token, value)
				return assign

			self.error(equals, "Invalid lvalue")
		return expr


	def parse_or_expr(self):
		expr = self.parse_and_expr()

		if self.match(TokenType.OR):
			operator = self.peek()
			self.advance()
			right = self.parse_and_expr()
			expr = LogicalExpr(expr, operator, right)

		return expr


	def parse_and_expr(self):
		expr = self.parse_bitwise()

		if self.match(TokenType.AND):
			operator = self.peek()
			self.advance()
			right = self.parse_bitwise()
			expr = LogicalExpr(expr, operator, right)

		return expr


	def parse_bitwise(self):
		expr = self.parse_equality()

		if self.match(TokenType.BIT_AND, TokenType.BIT_OR, TokenType.BIT_XOR, TokenType.BIT_SHIFT_LEFT, TokenType.BIT_SHIFT_RIGHT):
			operator = self.peek()
			self.advance()
			right = self.parse_equality()
			expr = BinaryExpr(expr, operator, right)

		return expr


	def parse_equality(self):
		expr = self.parse_comparision()

		if self.match(TokenType.NOT_EQUAL, TokenType.EQUAL_EQUAL):
			operator = self.peek()
			self.advance()
			right = self.parse_comparision()
			expr = BinaryExpr(expr, operator, right)

		return expr


	def parse_comparision(self):
		expr = self.parse_term()

		if self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
			operator = self.peek()
			self.advance()
			right = self.parse_term()
			expr = BinaryExpr(expr, operator, right)

		return expr


	def parse_term(self):
		expr = self.parse_factor()

		if self.match(TokenType.MINUS, TokenType.PLUS):
			operator = self.peek()
			self.advance()
			right = self.parse_factor()
			expr = BinaryExpr(expr, operator, right)

		return expr


	def parse_factor(self):
		expr = self.parse_unary()

		if self.match(TokenType.SLASH, TokenType.STAR):
			operator = self.peek()
			self.advance()
			right = self.parse_unary()
			expr = BinaryExpr(expr, operator, right)

		return expr


	def parse_unary(self):
		if self.match(TokenType.NOT, TokenType.MINUS, TokenType.BIT_NEGATE):
			operator = self.peek()
			self.advance()
			right = self.parse_unary()
			un = UnaryExpr(operator, right)
			return un

		return self.parse_func_call()


	def parse_func_call(self):
		expr = self.parse_primary()

		if self.check(TokenType.LEFT_PAREN):
			self.advance() # advance pass (
			args: List[Expr] = list()

			if not self.check(TokenType.RIGHT_PAREN):
				args.append(self.parse_expr())

				while self.check(TokenType.COMMA):
					self.advance()
					args.append(self.parse_expr())

			self.consume(TokenType.RIGHT_PAREN, "Expected ')' to end function call")
			expr = FunctionCallExpr(expr, args)
		return expr


	def parse_primary(self):
		expr = None

		if self.match(TokenType.TRUE):
			expr = LiteralExpr(True)
			self.advance()

		if self.match(TokenType.FALSE):
			expr = LiteralExpr(False)
			self.advance()

		if self.match(TokenType.NIL):
			expr = LiteralExpr(None)
			self.advance()

		if self.match(TokenType.STRING, TokenType.NUMBER):
			expr = LiteralExpr(self.peek().literal)
			self.advance()

		if self.match(TokenType.LEFT_PAREN):
			self.advance()
			expr = self.parse_expr()
			self.consume(TokenType.RIGHT_PAREN, "Mismatched parenthesis")
			expr = GroupingExpr(expr)

		if self.match(TokenType.IDENTIFIER):
			expr = VariableExpr(self.peek())
			self.advance()

		return expr


	def consume(self, typ, msg):
		if self.check(typ):
			return self.advance()
		self.error(self.peek(), msg)


	def error(self, token, msg):
		print(f'[line {token.line}] {msg}')
		sys.exit(12)


	def match(self, *types):
		for typ in types:
			if self.check(typ):
				# self.advance()
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
