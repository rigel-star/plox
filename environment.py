from typing import Dict


class Environment:
	def __init__(self):
		self.variable_values: Dict[str, object] = dict()


	def declare(self, name, value):
		self.variable_values[name] = value


	def get_var_value(self, name):
		if name in self.variable_values:
			return self.variable_values.get(name)
		
		print(f"Undefined variable: {name}")
		return None


	def dump(self):
		for key, value in self.variable_values.items():
			print(f"{key} -> {value}")