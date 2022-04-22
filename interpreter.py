from syntax_tree import *


class Interpreter(ExprVisitor):
	def interpret(self, expr):
		output = self.evaluate(expr)
		print(output)


	def visit_literal_expr(self, literal):
		return literal.value


	def visit_grouping_expr(self, group):
		return self.evaluate(group.expr)


	def visit_unary_expr(self, unary):
		expr_res = self.evaluate(unary.right)

		if unary.operator.token_type == TokenType.MINUS:
			if self.check_float_operand(expr_res):
				return -float(expr_res)
			else:
				self.runtime_error(f"[line {unary.operator.line}]: [-(minus)] operand must be of number type")

		elif unary.operator.token_type == TokenType.BIT_NEGATE:
			if self.check_int_operand(expr_res):
				return ~int(expr_res)
			else:
				self.runtime_error(f"[line {unary.operator.line}]: [-(minus)] operand must be of int type")

		elif unary.operator.token_type == TokenType.NOT:
			if isinstance(expr_res, bool):
				return not bool(expr_res)

		return None


	def visit_binary_expr(self, binary):
		left = self.evaluate(binary.left_expr)
		right = self.evaluate(binary.right_expr)

		if binary.operator.token_type == TokenType.MINUS:
			if isinstance(left, str) and isinstance(right, str):
				if left.isdigit() and right.isdigit():
					return int(left) - int(right)
				elif left.isdecimal() and right.isdecimal():
					return float(left) - float(right)
			
			self.runtime_error(f"[line {binary.operator.line}]: [-(minus)] operand must be of number or str type")

		elif binary.operator.token_type == TokenType.PLUS:
			if isinstance(left, str) and isinstance(right, str):
				if left.isdigit() and right.isdigit():
					return int(left) + int(right)
				elif left.isdecimal() and right.isdecimal():
					return float(left) + float(right)
			
			self.runtime_error(f"[line {binary.operator.line}]: [+(plus)] operand must be of number or str type")

		elif binary.operator.token_type == TokenType.SLASH:
			return float(left) / float(right)

		elif binary.operator.token_type == TokenType.STAR:
			return float(left) * float(right)

		elif binary.operator.token_type == TokenType.BIT_AND:
			if isinstance(left, str) and isinstance(right, str):
				if left.isdigit() and right.isdigit():
					return int(left) & int(right)
			
			self.runtime_error(f"[line {binary.operator.line}]: [&(and)] operand must be of int type")

		elif binary.operator.token_type == TokenType.BIT_OR:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left | right
			else:
				self.runtime_error(f"[line {binary.operator.line}]: [|(or)] operand must be of int type")

		elif binary.operator.token_type == TokenType.BIT_XOR:
			if isinstance(left, str) and isinstance(right, str):
				if left.isdigit() and right.isdigit():
					return int(left) ^ int(right)
			
			self.runtime_error(f"[line {binary.operator.line}]: [^(xor)] operand must be of int type")

		elif binary.operator.token_type == TokenType.BIT_SHIFT_LEFT:
			if isinstance(left, str) and isinstance(right, str):
				if left.isdigit() and right.isdigit():
					return int(left) << int(right)
			
			self.runtime_error(f"[line {binary.operator.line}]: [<<(left shift)] operand must be of int type")

		elif binary.operator.token_type == TokenType.BIT_SHIFT_RIGHT:
			if isinstance(left, str) and isinstance(right, str):
				if left.isdigit() and right.isdigit():
					return int(left) >> int(right)

			self.runtime_error(f"[line {binary.operator.line}]: [>>(right shift)] operand must be of int type")

		elif binary.operator.token_type == TokenType.GREATER:
			return float(left) > float(right)

		elif binary.operator.token_type == TokenType.GREATER_EQUAL:
			return float(left) >= float(right)

		elif binary.operator.token_type == TokenType.LESS:
			return float(left) < float(right)

		elif binary.operator.token_type == TokenType.LESS_EQUAL:
			return float(left) <= float(right)

		elif binary.operator.token_type == TokenType.NOT_EQUAL:
			return not self.is_equal(left, right)

		elif binary.operator.token_type == TokenType.EQUAL_EQUAL:
			print(left, right)
			return self.is_equal(left, right)

		return None


	def runtime_error(self, msg):
		print("RuntimeError:", msg)
		sys.exit(69)


	def is_equal(self, obj1, obj2):
		if obj1 is None and obj2 is None:
			return True
		if obj1 is None:
			return False
		return obj1 is obj2


	def check_int_operand(self, value):
		if isinstance(value, int):
			return True
		return False


	def check_float_operand(self, value):
		if isinstance(value, float):
			return True
		return False


	def evaluate(self, expr):
		return expr.accept(self)