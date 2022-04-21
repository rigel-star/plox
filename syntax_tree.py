import sys
import os

from scanner import Token


class Visitor:
	pass


class ExprVisitor(Visitor):
	def visit_assign_expr(assign: Assign):
		pass

class StmtVisitor(Visitor):
	pass


class Expr(ExprVisitor, StmtVisitor):
	pass


class BinaryExpr(Expr):
	def __init__(self, expr_right: Expr, operator: Token, expr_left: Expr):
		self.right_expr = expr_right
		self.operator = operator
		self.left_expr = expr_left


class UnaryExpr(Expr):
	def __init__(self, operator: Token, expr: Expr):
		self.operator = operator
		self.expr = expr


class LiteralExpr(Expr):
	def __init__(self, literal: object):
		self.expr = literal


class GroupExpr(Expr):
	def __init__(self, expr):
		self.expr = expr
