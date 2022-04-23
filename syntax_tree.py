import sys
import os
from typing import List

from scanner import Token, TokenType

class ExprVisitor:
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

	def visit_variable_expr(self, variable):
		pass

	def visit_logical_expr(self, logical):
		pass

	def visit_func_call_expr(self, func):
		pass


# Expressions in program
class Expr:
	def accept(self, visitor: ExprVisitor):
		pass


class AssignExpr(Expr):
	def __init__(self, name: Token, value: Expr):
		self.name = name
		self.value = value

	def accept(self, visitor: ExprVisitor):
		return visitor.visit_assign_expr(self)


class BinaryExpr(Expr):
	def __init__(self, expr_left: Expr, operator: Token, expr_right: Expr):
		self.right_expr = expr_right
		self.operator = operator
		self.left_expr = expr_left

	def accept(self, visitor):
		return visitor.visit_binary_expr(self)


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


class VariableExpr(Expr):
	def __init__(self, name: Token):
		self.name = name

	def accept(self, visitor):
		return visitor.visit_variable_expr(self)


class LogicalExpr(Expr):
	def __init__(self, left_expr: Expr, operator: Token, right_expr: Expr):
		self.right_expr = right_expr
		self.operator = operator
		self.left_expr = left_expr

	def accept(self, visitor: ExprVisitor):
		return visitor.visit_logical_expr(self)


class FunctionCallExpr(Expr):
	def __init__(self, callee, args):
		self.callee = callee
		self.arguments = args

	def accept(self, visitor: ExprVisitor):
		return visitor.visit_func_call_expr(self)


# Statements in program
class StmtVisitor:
	def visit_print_stmt(self, printt):
		pass

	def visit_expr_stmt(self, expr_stmt):
		pass

	def visit_var_declare_stmt(self, var_decl):
		pass

	def visit_block_stmt(self, block):
		pass

	def visit_if_stmt(self, if_stmt):
		pass

	def visit_while_stmt(self, while_stmt):
		pass

<<<<<<< HEAD
=======
	def visit_func_decl_stmt(self, func_decl):
		pass

>>>>>>> feature-branch

class Stmt:
	def accept(self, visitor: StmtVisitor):
		pass


class PrintStmt(Stmt):
	def __init__(self, expr: Expr):
		self.expr = expr

	def accept(self, visitor: StmtVisitor):
		visitor.visit_print_stmt(self)


class ExprStmt(Stmt):
	def __init__(self, expr: Expr):
		self.expr = expr

	def accept(self, visitor: StmtVisitor):
		visitor.visit_expr_stmt(self)


class VarDeclareStmt(Stmt):
	def __init__(self, name: str, init: Expr):
		self.name = name
		self.init = init

	def accept(self, visitor: StmtVisitor):
		visitor.visit_var_declare_stmt(self)


class BlockStmt(Stmt):
	def __init__(self, stmts: List[Stmt]):
		self.statements = stmts

	def accept(self, visitor: StmtVisitor):
		visitor.visit_block_stmt(self)


class IfStmt(Stmt):
	def __init__(self, condition: Expr, if_true: Stmt, if_false: Stmt):
		self.condition = condition
		self.if_true = if_true
		self.if_false = if_false

	def accept(self, visitor: StmtVisitor):
		visitor.visit_if_stmt(self)


class WhileStmt(Stmt):
	def __init__(self, condition: Expr, body: Stmt):
		self.condition = condition
		self.body = body

	def accept(self, visitor: StmtVisitor):
		visitor.visit_while_stmt(self)


<<<<<<< HEAD
=======
class FunctionDeclStmt(Stmt):
	def __init__(self, name, params, body):
		self.name = name
		self.parameters = params
		self.body = body

	def accept(self, visitor: StmtVisitor):
		visitor.visit_func_decl_stmt(self)


>>>>>>> feature-branch
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
