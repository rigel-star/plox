from syntax_tree import *
from environment import Environment
from typing import List
from enum import Enum
import sys


class ErrorType(Enum):
	PloxTypeError = 1,
	PloxDivisonByZeroError = 2


class Interpreter(ExprVisitor, StmtVisitor):
	def __init__(self):
		self.globals = Environment()
		self.init_globals()
		self.stop = False
		self.var_env = Environment(enclosing=self.globals)


	def init_globals(self):
		import globals
		sqrt_math_func = globals.Sqrt()
		self.globals.declare("sqrt", sqrt_math_func)


	def interpret(self, stmts: List[Stmt]):
		for stmt in stmts:
			#print(stmt)
			self.execute(stmt)

		#self.var_env.dump()


	def execute(self, stmt):
		stmt.accept(self)


	#expressions part
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

			self.runtime_unsupported_operands_error("-", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.PLUS:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left + right
			elif isinstance(left, str) and isinstance(right, str):
				return str(left) + str(right)

			self.runtime_unsupported_operands_error("+", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.SLASH:
			if self.check_number_operand(left) and self.check_number_operand(right):
				if right == 0:
					self.runtime_error(ErrorType.PloxDivisonByZeroError)
				return left / right

			self.runtime_unsupported_operands_error("/", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.STAR:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left * right
			elif any([self.check_str_operand(left), self.check_str_operand(right)]) and any([self.check_int_operand(left), self.check_int_operand(right)]):
				return left * right

			self.runtime_unsupported_operands_error("*", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.BIT_AND:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left & right

			self.runtime_unsupported_operands_error("&", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.BIT_OR:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left | right

			self.runtime_unsupported_operands_error("|", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.BIT_XOR:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left ^ right

			self.runtime_unsupported_operands_error("^", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.BIT_SHIFT_LEFT:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left << right

			self.runtime_unsupported_operands_error("<<", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.BIT_SHIFT_RIGHT:
			if self.check_int_operand(left) and self.check_int_operand(right):
				return left >> right

			self.runtime_unsupported_operands_error(">>", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.GREATER:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left > right

			self.runtime_unsupported_operands_error(">", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.GREATER_EQUAL:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left >= right

			self.runtime_unsupported_operands_error(">=", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.LESS:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left < right

			self.runtime_unsupported_operands_error("<", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.LESS_EQUAL:
			if self.check_number_operand(left) and self.check_number_operand(right):
				return left <= right

			self.runtime_unsupported_operands_error("<=", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.NOT_EQUAL:
			if type(left) == type(right):
				return left != right
			elif any([self.check_int_operand(left), self.check_int_operand(right)]) and any([self.check_float_operand(left), self.check_float_operand(right)]):
				return left != right

			self.runtime_unsupported_operands_error("!=", left_type_name, right_type_name)

		elif binary.operator.token_type == TokenType.EQUAL_EQUAL:
			if type(left) == type(right):
				return left == right
			elif any([self.check_int_operand(left), self.check_int_operand(right)]) and any([self.check_float_operand(left), self.check_float_operand(right)]):
				return left == right

			self.runtime_unsupported_operands_error("==", left_type_name, right_type_name)

		return None


	def visit_variable_expr(self, var):
		return self.var_env.get_var_value(var.name.lexeme)


	def visit_anon_func_expr(self, anon):
		from callable import PloxFunction
		func = FunctionDeclStmt(None, anon.parameters, anon.body)
		plox_func = PloxFunction(func, self.var_env)
		return plox_func


	def visit_assign_expr(self, assign):
		var_name = assign.name.lexeme
		value = self.evaluate(assign.value)
		self.var_env.assign(var_name, value)
		return value


	def visit_logical_expr(self, logical):
		left_expr = self.evaluate(logical.left_expr)
		operator = logical.operator
		right_expr = self.evaluate(logical.right_expr)

		if operator.token_type == TokenType.OR:
			return left_expr or right_expr
		elif operator.token_type == TokenType.AND:
			return left_expr and right_expr

		return None


	def visit_func_call_expr(self, func_call_expr):
		from callable import PloxCallable

		callee = self.evaluate(func_call_expr.callee)
		args = list()

		for arg in func_call_expr.arguments:
			eval = self.evaluate(arg)
			args.append(eval)

		if not isinstance(callee, PloxCallable):
			print(f'\'{func_call_expr.callee.name.lexeme}\' is not a function')
			sys.exit(13)

		return callee.call(self, args)


	def visit_class_prop_get_expr(self, get):
		from callable import PloxInstance
		obj = self.evaluate(get.obj)

		if not isinstance(obj, PloxInstance):
			print("Only instances can have properties")
			sys.exit(14)

		return obj.get(get.name.lexeme)


	def visit_class_prop_set_expr(self, set):
		from callable import PloxInstance
		obj = self.evaluate(set.obj)

		if not isinstance(obj, PloxInstance):
			print("Only instances can have fields")
			sys.exit(15)

		value = self.evaluate(set.value)
		obj.set(set.name.lexeme, value)
		return value


	def visit_func_decl_stmt(self, func_decl):
		from callable import PloxFunction
		function = PloxFunction(func_decl, self.var_env)
		self.var_env.variable_values[func_decl.name.lexeme] = function


	# statements part
	def visit_print_stmt(self, printt):
		expr_result = self.evaluate(printt.expr)
		# sys.stdout.write(self.stringify(expr_result))
		print(self.stringify(expr_result))


	def visit_expr_stmt(self, expr_stmt):
		self.evaluate(expr_stmt.expr)


	def visit_if_stmt(self, if_stmt):
		condition = self.evaluate(if_stmt.condition)
		if condition:
			self.execute(if_stmt.if_true)
		else:
			if if_stmt.if_false:
				self.execute(if_stmt.if_false)


	def visit_var_declare_stmt(self, var_decl):
		value = "undefined"
		if var_decl.init is not None:
			value = self.evaluate(var_decl.init)

		#declare new variable
		self.var_env.declare(var_decl.name, value)


	def visit_while_stmt(self, while_stmt):
		# print(self.stringify(while_stmt))
		while self.evaluate(while_stmt.condition):
			if self.stop == 1:
				break
			else:
				self.execute(while_stmt.body)
		return None


	def visit_return_stmt(self, ret):
		from callable import ReturnException
		return_value = None

		if ret.value is not None:
			return_value = self.evaluate(ret.value)

		raise ReturnException(return_value)
	
	def visit_break_stmt(self, br):
		from callable import BreakException
		break_value = None
		if br is not None:
			break_value = self.evaluate(br.stop)
		if isinstance(break_value, bool):
			if break_value == True:
				self.stop = 1
			else:
				self.stop = 2
		else:
			raise BreakException('BreakValue Error', 'None Bool')

	def visit_class_decl_stmt(self, cls):
		import callable
		kls = callable.PloxClass(cls.name.lexeme)
		self.var_env.declare(cls.name.lexeme, kls)


	def visit_block_stmt(self, block):
		env = Environment(enclosing=self.var_env)
		self.execute_block(block.statements, env)


	def execute_block(self, stmts, env):
		prev_env = self.var_env
		self.var_env = env

		for stmt in stmts:
			self.execute(stmt)

		self.var_env = prev_env


	def stringify(self, obj):
		if obj is None:
			return "nil"
		return str(obj)


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


	def evaluate(self, expr):
		return expr.accept(self)


	def runtime_unsupported_operands_error(self, operator, type1, type2):
		self.runtime_error(ErrorType.PloxTypeError, f'unsupported operand type(s) for {operator}: {type1} and {type2}')
