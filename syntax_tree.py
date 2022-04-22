import sys
import os

from scanner import Token, TokenType

class ExprVisitor():
	def visit_assign_expr(self, assign):
		pass
	
	def visit_binary_expr(self, binary):
		pass
	
	def visit_grouping_expr(self, grouping):
		pass
	
	def visit_literal_expr(self, literal):
		pass
	
	def visit_unary_expr(self, unary):
		pass
	
	def visit_logical_expr(self, logical):
		pass

	def visit_bitwise_expr(self, bitwise):
		pass


class Expr:
	def accept(self, visitor):
		pass


class AssignExpr(Expr):
	def __init__(self, name: Token, value: Expr):
		self.name = name
		self.value = value
		
	def accept(self, visitor: ExprVisitor):
		return visitor.visit_assign_expr(self)

'''
class BitwiseExpr(Expr):
	def __init__(self, expr_right: Expr, operator: Token, expr_left: Expr)
'''


class BinaryExpr(Expr):
	def __init__(self, expr_right: Expr, operator: Token, expr_left: Expr):
		self.right_expr = expr_right
		self.operator = operator
		self.left_expr = expr_left

	def accept(self, visitor):
		return visitor.visit_binary_expr(self)

	def __str__(self):
		return f'{self.right_expr} {self.operator} {self.left_expr}'


class UnaryExpr(Expr):
	def __init__(self, operator: Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor: ExprVisitor):
		return  visitor.visit_unary_expr(self)


class LiteralExpr(Expr):
	def __init__(self, literal: object):
		self.value = literal

	def accept(self, visitor: ExprVisitor):
		return visitor.visit_literal_expr(self)


class GroupingExpr(Expr):
	def __init__(self, expr: Expr):
		self.expr = expr

	def accept(self, visitor: ExprVisitor):
		return visitor.visit_grouping_expr(self)


class LogicalExpr(Expr):
	def __init__(self, left: Expr, operator: Token, right: Token):
		self.left_expr = left
		self.operator = operator
		self.right_expr = right

	def accept(self, visitor: ExprVisitor):
		return visitor.visit_logical_expr(self)
	

# For debugging purpose only
class ASTPrinter(ExprVisitor):
	def printer(self, expr: Expr):
		return expr.accept(self)

	def visit_unary_expr(self, unary):
		return self.parenthesize(unary.operator.lexeme, unary.right)

	def visit_binary_expr(self, binary):
		return self.parenthesize(binary.operator.lexeme, binary.left_expr, binary.right_expr)

	def visit_literal_expr(self, literal):
		return str(literal.value)

	def visit_logical_expr(self, logical):
		return self.parenthesize(logical.operator.lexeme, logical.left_expr, logical.right_expr)

	def visit_grouping_expr(self, group):
		return self.parenthesize("g", group.expr)

	def visit_assign_expr(self, assign):
		return self.parenthesize("var", assign.value)

	def parenthesize(self, name, *exprs):
		output = f"("
		for expr in exprs:
			output += " "
			accept_out = expr.accept(self)
			output += accept_out if accept_out else ""

		output += f" {name} )"
		return output

if __name__ == "__main__":
	lit = LiteralExpr(345)
	lit2 = LiteralExpr(43)
	tok = Token(TokenType.PLUS, "+", None, 1)
	binary = BinaryExpr(lit, tok, lit2)
	expr = GroupingExpr(binary)
	ast = ASTPrinter()
	print(ast.printer(expr))
