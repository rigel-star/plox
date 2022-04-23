from syntax_tree import *

from enum import Enum

class ErrorType(Enum):
	PloxTypeError = 1,
	PloxDivisonByZeroError = 2


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
			if self.check_int_operand(expr_res):
				return -int(expr_res)
			elif self.check_float_operand(expr_res):
				return -float(expr_res)

			self.runtime_error(ErrorType.PloxTypeError, "unsupported operand type(s) for -")

		elif unary.operator.token_type == TokenType.BIT_NEGATE:
			if self.check_int_operand(expr_res):
				return ~int(expr_res)
			
			self.runtime_error(ErrorType.PloxTypeError, "unsupported operand type(s) for ~")

		elif unary.operator.token_type == TokenType.NOT:
			if self.check_number_operand(expr_res):
				return not bool(expr_res)

		return None


	def visit_binary_expr(self, binary):
		left = self.evaluate(binary.left_expr)
		right = self.evaluate(binary.right_expr)

		left_type_name = left.__class__.__name__
		right_type_name = right.__class__.__name__

		if binary.operator.token_type == TokenType.MINUS:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left - right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for -: {left_type_name} and {right_type_name}")

		elif binary.operator.token_type == TokenType.PLUS:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left + right
			elif isinstance(left, str) and isinstance(right, str):
				return str(left) + str(right)

			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for +: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.SLASH:
			if self.check_number_operand(left) and self.check_number_operand(right):
				if right == 0:
					self.runtime_error(ErrorType.PloxDivisonByZeroError)
				return left / right

			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for /: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.STAR:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left * right
			elif any([self.check_str_operand(left), self.check_str_operand(right)]) and any([self.check_int_operand(left), self.check_int_operand(right)]):
				return left * right

			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for *: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.BIT_AND:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left & right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for &: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.BIT_OR:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left | right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for |: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.BIT_XOR:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left ^ right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for ^: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.BIT_SHIFT_LEFT:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left << right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for <<: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.BIT_SHIFT_RIGHT:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left >> right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for >>: {left_type_name} and {right_type_name}")
		
		elif binary.operator.token_type == TokenType.GREATER:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left > right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for >: {left_type_name} and {right_type_name}")

		elif binary.operator.token_type == TokenType.GREATER_EQUAL:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left >= right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for >=: {left_type_name} and {right_type_name}")

		elif binary.operator.token_type == TokenType.LESS:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left < right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for <: {left_type_name} and {right_type_name}")

		elif binary.operator.token_type == TokenType.LESS_EQUAL:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left <= right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for <=: {left_type_name} and {right_type_name}")

		elif binary.operator.token_type == TokenType.NOT_EQUAL:
			print(type(left), type(right))
			if type(left) == type(right):
				return left != right
			elif any([self.check_int_operand(left), self.check_int_operand(right)]) and any([self.check_float_operand(left), self.check_float_operand(right)]):
				return left != right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for !=: {left_type_name} and {right_type_name}")

		elif binary.operator.token_type == TokenType.EQUAL_EQUAL:
			if type(left) == type(right):
				return left == right
			elif any([self.check_int_operand(left), self.check_int_operand(right)]) and any([self.check_float_operand(left), self.check_float_operand(right)]):
				return left == right
			
			self.runtime_error(ErrorType.PloxTypeError, f"unsupported operand type(s) for ==: {left_type_name} and {right_type_name}")

		return None


	def runtime_error(self, typ, msg=None):
		if typ == ErrorType.PloxTypeError:
			sys.stderr.write(f"TypeError: {msg if msg else ''}\n")
		elif typ == ErrorType.PloxDivisonByZeroError:
			sys.stderr.write(f"DivisionByZeroError: {msg if msg else 'division by zero'}\n")
		sys.exit(12)


	def is_equal(self, obj1, obj2):
		if obj1 is None and obj2 is None:
			return True
		if obj1 is None:
			return False
		return obj1 is obj2


	def check_str_operand(self, value):
		return isinstance(value, str)


	def check_number_operand(self, value):
		return self.check_int_operand(value) or self.check_float_operand(value)


	def check_int_operand(self, value):
		return isinstance(value, int)


	def check_float_operand(self, value):
		return isinstance(value, float)


	def check_float_operand(self, value):
		if isinstance(value, float):
			return True
		return False


	def evaluate(self, expr):
		return expr.accept(self)