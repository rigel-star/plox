from typing import Dict


class Environment:
	def __init__(self, enclosing=None):
		self.variable_values: Dict[str, object] = dict()
		self.enclosing = enclosing


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

		print(f"Undefined variable '{name}'")


	def get_var_value(self, name):
		if name in self.variable_values:
			return self.variable_values.get(name)

		if self.enclosing:
			if name in self.enclosing.variable_values:
				return self.enclosing.variable_values.get(name)
		
		return f"Undefined variable '{name}'"


	def dump(self):
		if self.enclosing:
			for key, value in self.enclosing.items():
				print(f"{key} -> {value}")

		for key, value in self.variable_values.items():
			print(f"{key} -> {value}")