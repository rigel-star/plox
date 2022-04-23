from typing import Dict

class Environment:
	def __init__(self, enclosing = None, pre = None):
		self.variable_values: Dict[str, object] = dict()
		self.enclosing = enclosing

		if pre:
			for key, value in pre.items():
				self.variable_values[key] = value


	def declare(self, name, value):
		self.variable_values[name] = value


	def assign(self, name, value):
		if name in self.variable_values:
			self.variable_values[name] = value
			return

		if self.enclosing:
			if name in self.enclosing.variable_values:
				self.enclosing.variable_values[name] = value
			return

		print(f"Undefined identifier '{name}'")


	def get_var_value(self, name):
		if name in self.variable_values:
			return self.variable_values.get(name)

		if self.enclosing:
			if name in self.enclosing.variable_values:
				return self.enclosing.variable_values.get(name)

		print(f"Undefined identifier '{name}'")


	def dump(self):
		if self.enclosing:
			for key, value in self.enclosing.variable_values.items():
				print(f"{key} -> {value}")

		for key, value in self.variable_values.items():
			print(f"{key} -> {value}")
