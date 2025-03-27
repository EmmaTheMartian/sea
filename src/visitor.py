from typing import Optional
import antlr4
from antlr4.tree.Tree import TerminalNodeImpl
from .backend import Backend
from .backend_c import Backend_C
from .compiler import SEA_VOID, Compiler, SeaFunction, SeaRecord, SeaType
from .syntax.Lexer import Lexer
from .syntax.Parser import Parser
from .syntax.ParserListener import ParserListener

class Visitor(ParserListener):
	def __init__(self, backend: Backend):
		self.backend = backend

	def _writer(self, expr: Parser.ExprContext, index: Optional[int] = None):
		if index is None:
			return lambda: self.write_expr(expr)
		else:
			return lambda: self.write_expr(expr.getChild(index))

	def _simple_writer(self, expr: Parser.ExprContext):
		return lambda: self.write_expr(expr)

	def enterComment(self, ctx:Parser.CommentContext):
		if ctx.COMMENT() is not None:
			self.backend.comment(ctx.COMMENT().getText().removeprefix('//'))
		else:
			self.backend.multiline_comment(ctx.MULTILINE_COMMENT().getText().removeprefix('/*').removesuffix('*/'))

	def write_expr(self, expr: Parser.ExprContext):
		def _writer(index: int):
			def it():
				self.write_expr(expr.getChild(index))
			return it

		if expr.expr() is not None and expr.part_invoke() is not None:
			e = expr.part_invoke()
			print(e)
			items = []
			for i in range(1, e.getChildCount() - 1):
				item = e.children[i]
				if isinstance(item, TerminalNodeImpl):
					continue
				items.append(self._writer(e, i))
			self.backend.invoke(self._writer(expr, 0), items)
		# Operators
		elif expr.OP_DOT() is not None: self.backend.dot(_writer(0), _writer(2))
		elif expr.OP_NOT() is not None: self.backend.not_(_writer(1))
		elif expr.OP_AND() is not None: self.backend.and_(_writer(0), _writer(2))
		elif expr.OP_OR() is not None: self.backend.or_(_writer(0), _writer(2))
		elif expr.OP_EQ() is not None: self.backend.eq(_writer(0), _writer(2))
		elif expr.OP_NEQ() is not None: self.backend.neq(_writer(0), _writer(2))
		elif expr.OP_GT() is not None: self.backend.gt(_writer(0), _writer(2))
		elif expr.OP_GTEQ() is not None: self.backend.gteq(_writer(0), _writer(2))
		elif expr.OP_LT() is not None: self.backend.lt(_writer(0), _writer(2))
		elif expr.OP_LTEQ() is not None: self.backend.lteq(_writer(0), _writer(2))
		elif expr.OP_INC() is not None: self.backend.inc(_writer(1))
		elif expr.OP_DEC() is not None: self.backend.dec(_writer(1))
		# Math
		elif expr.ADD() is not None: self.backend.add(_writer(0), _writer(1))
		elif expr.SUB() is not None: self.backend.sub(_writer(0), _writer(1))
		elif expr.MUL() is not None: self.backend.mul(_writer(0), _writer(1))
		elif expr.DIV() is not None: self.backend.div(_writer(0), _writer(1))
		elif expr.MOD() is not None: self.backend.mod(_writer(0), _writer(1))
		# Literals
		elif expr.NUMBER() is not None:
			self.backend.number(expr.NUMBER().getText())
		elif expr.STRING() is not None:
			self.backend.number(expr.STRING().getText())
		elif expr.TRUE() is not None:
			self.backend.true()
		elif expr.FALSE() is not None:
			self.backend.false()
		elif expr.ID() is not None:
			self.backend.id(expr.ID().getText())
		elif expr.expr_list() is not None:
			e = expr.expr_list()
			items = []
			for i in range(1, e.getChildCount() - 1):
				item = e.children[i]
				if isinstance(item, TerminalNodeImpl):
					continue
				items.append(self._writer(e, i))
			self.backend.array(items)
		elif expr.expr_new() is not None:
			e = expr.expr_new()
			items = []
			for i in range(1, e.getChildCount() - 1):
				item = e.children[i]
				if isinstance(item, TerminalNodeImpl):
					continue
				items.append(self._writer(e, i))
			self.backend.new(e.ID().symbol.text, items)

	def enterStat(self, ctx:Parser.StatContext):
		print("asdf")
		if ctx.expr() is not None:
			print("fdsa")
			print(ctx.expr().getText())
			self.write_expr(ctx.expr())

	def exitStat(self, ctx:Parser.StatContext):
		if self.backend.needs_line_ending(ctx):
			self.backend.write(self.backend.line_ending, False)
		else:
			self.backend.writeln('', False)

	def enterStat_var(self, ctx:Parser.Stat_varContext):
		self.backend.var(
			ctx.ID().symbol.text,
			SeaType.from_str(ctx.typedesc().getText()),
			self._writer(ctx.expr())
		)

	def enterStat_let(self, ctx:Parser.Stat_letContext):
		self.backend.let(
			ctx.ID().symbol.text,
			SeaType.from_str(ctx.typedesc().getText()),
			self._writer(ctx.expr())
		)

	def enterStat_assign(self, ctx:Parser.Stat_assignContext):
		self.backend.assign(ctx.ID().symbol.text, self._writer(ctx.expr()))
		pass

	def enterStat_ret(self, ctx:Parser.Stat_retContext):
		self.backend.ret(self._writer(ctx.expr()))

	def enterFun(self, ctx:Parser.FunContext):
		params = {}
		part = ctx.part_params()
		for i in range(1, part.getChildCount() - 1):
			param = part.children[i]
			if isinstance(param, TerminalNodeImpl):
				continue
			params[param.ID().symbol.text] = SeaType.from_str(param.typedesc().getText())
		del part

		if ctx.COLON() is not None:
			returns = SeaType.from_str(ctx.getChild(4).getText())
		else:
			returns = SEA_VOID

		self.backend.fun(ctx.ID().symbol.text, SeaFunction(returns, params))

	def enterRaw_block(self, ctx:Parser.Raw_blockContext):
		self.backend.raw(ctx.getChild(1).getText())

	def enterRec(self, ctx:Parser.RecContext):
		name = ctx.ID().symbol.text
		fields = {}
		part = ctx.part_params()
		for i in range(1, part.getChildCount() - 1):
			param = part.children[i]
			if isinstance(param, TerminalNodeImpl):
				continue
			fields[param.ID().symbol.text] = SeaType.from_str(param.typedesc().getText())
		del part
		self.backend.rec(name, SeaRecord(fields))

	def enterExpr_block(self, ctx:Parser.Expr_blockContext):
		self.backend.block_start()

	def exitExpr_block(self, ctx:Parser.Expr_blockContext):
		self.backend.block_end()

	def enterExpr_if(self, ctx:Parser.Expr_ifContext):
		self.backend.if_(self._writer(ctx.expr()))
		# ctx.expr_block()
		if ctx.ELSE() is not None:
			self.backend.else_()

	def enterStat_for(self, ctx:Parser.Stat_forContext):
		self.backend.for_(self._writer(ctx.expr(0)), self._writer(ctx.expr(1)), self._writer(ctx.expr(2)))

	def enterStat_each(self, ctx:Parser.Stat_eachContext):
		self.backend.each_begin(ctx.ID(0).symbol.text, ctx.ID(1).symbol.text)

	def exitStat_each(self, ctx:Parser.Stat_eachContext):
		self.backend.each_end()


def visit(file_path: str):
	input_stream = antlr4.FileStream(file_path)
	lexer = Lexer(input_stream)
	stream = antlr4.CommonTokenStream(lexer)
	parser = Parser(stream)

	tree = parser.program()
	print(tree.toStringTree(recog = parser))

	walker = antlr4.ParseTreeWalker()
	with Backend_C(Compiler(), "output.c") as backend:
		walker.walk(Visitor(backend), tree)
