from typing import Callable
from .compiler import Compiler, SeaFunction, SeaRecord, SeaType
from .syntax.Parser import Parser

class Backend:
	def __init__(self, compiler: Compiler, output_file: str):
		self.compiler = compiler
		self.output_file = output_file
		self.line_ending = '\n'
		self.depth = 0
		self.indent = '\t'
		self.block_needs_line_ending = False
		self.force_indent_next = False
		self.module = None
		self.using = []
		self.module_stack = ['main']

	def __enter__(self):
		self.file = open(self.output_file, 'w')
		return self

	def __exit__(self, _a, _b, _c):
		self.file.close()

	def needs_line_ending(self, stat: Parser.StatContext):
		return not (
			stat.stat_for() is not None or
			stat.stat_each() is not None
		)

	def write(self, text: str, indent: bool = True):
		if indent or self.force_indent_next:
			self.file.write(self.indent * self.depth)
			if self.force_indent_next:
				self.force_indent_next = False
		self.file.write(text)

	def writeln(self, text: str, indent: bool = True):
		if indent or self.force_indent_next:
			self.file.write(self.indent * self.depth)
			if self.force_indent_next:
				self.force_indent_next = False
		self.file.write(text)
		self.file.write('\n')

	def type(self, type: SeaType) -> str: ...
	def typed_id(self, type: SeaType, id: str) -> str: ...

	def file_begin(self): ...
	def file_end(self): ...

	def use(self, module: str): ...
	def rec(self, name: str, record: SeaRecord): ...
	def fun(self, name: str, func: SeaFunction): ...
	def var(self, name: str, type: SeaType, value: Callable): ...
	def let(self, name: str, type: SeaType, value: Callable): ...
	def assign(self, name: str, value: Callable): ...
	def ret(self, value: Callable): ...

	def block_begin(self): ...
	def block_end(self): ...
	def invoke(self, it: Callable, args: list[Callable]): ...
	def if_(self, cond: Callable): ...
	def else_(self): ...
	def for_(self, define: Callable, cond: Callable, inc: Callable): ...
	def each_begin(self, var: str, of: str): ...
	def each_end(self): ...

	def true(self): ...
	def false(self): ...

	def dot(self, left: Callable, right: Callable): ...
	def not_(self, value: Callable): ...
	def and_(self, left: Callable, right: Callable): ...
	def or_(self, left: Callable, right: Callable): ...
	def eq(self, left: Callable, right: Callable): ...
	def neq(self, left: Callable, right: Callable): ...
	def gt(self, left: Callable, right: Callable): ...
	def gteq(self, left: Callable, right: Callable): ...
	def lt(self, left: Callable, right: Callable): ...
	def lteq(self, left: Callable, right: Callable): ...
	def inc(self, value: Callable): ...
	def dec(self, value: Callable): ...

	def add(self, left: Callable, right: Callable): ...
	def sub(self, left: Callable, right: Callable): ...
	def mul(self, left: Callable, right: Callable): ...
	def div(self, left: Callable, right: Callable): ...
	def mod(self, left: Callable, right: Callable): ...

	def number(self, it: str): ...
	def id(self, it: str): ...
	def string(self, it: str, c: bool): ...
	def array(self, items: list[Callable]): ...
	def new(self, rec: str, items: list[Callable]): ...
	def ref(self, id: str): ...
	def deref(self, value: Callable): ...
	def cast(self, type: SeaType, value: Callable): ...

	def raw(self, code: str): ...

	def comment(self, text: str): ...
	def multiline_comment(self, text: str): ...
