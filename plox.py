#!/usr/bin/env python3

import sys
import os
import argparse
from typing import List, Dict, Tuple

# custom
from scanner import Token, Scanner
from parser import Parser
from interpreter import Interpreter


def error(line, message):
	print(f"[{line}]: {message}")


def run(program):
	scan = Scanner(program)
	tokens = scan.scan_tokens()
	parser = Parser(tokens)
	stmts = parser.parse()
	interp = Interpreter()
	interp.interpret(stmts)


def run_program(file_name):
	with open(file_name) as f:
		byte_array = bytearray()
		while True:
			byte = f.read(1)
			if not byte:
				break
			byte_array.append(ord(byte))
		run(byte_array.decode())


def run_prompt():
	interp = Interpreter()
	while True:
		line = input(">>> ")
		if line is not None:
			if line.startswith("{"):
				while True:
					temp = input("\t")
					if temp == "}":
						break
					line += temp
				line += "}"

			scan = Scanner(line)
			tokens = scan.scan_tokens()
			parser = Parser(tokens)
			stmts = parser.parse()
			interp.interpret(stmts)


if __name__ == "__main__":
	if len(sys.argv) > 2:
		print("Usage: plox [script]")
		sys.exit(32)
	elif len(sys.argv) == 2:
		run_program(sys.argv[1])
	else:
		run_prompt()
