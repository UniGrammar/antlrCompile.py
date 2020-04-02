import typing

from ..ANTLRInternalClasses import ANTLRInternalClasses

antlr4 = None


class ANTLRInternalClassesPython(ANTLRInternalClasses):
	ext = ".py"
	extLen = len(ext)
	__slots__ = ("antlr4",)
	_necessaryRoles = ("lexer", "parser")

	@classmethod
	def __init__(self):
		import antlr4

		self.antlr4 = antlr4

	def CharStreams(self, src):
		return self.antlr4.InputStream(src)

	def CommonTokenStream(self, lexer):
		return self.antlr4.CommonTokenStream(lexer)

	def _somethingToIterable(self, something: typing.Any, selector: typing.Callable[[typing.Any, str], typing.Union[str, "ast.AST"]]):
		for role in self.__class__._necessaryRoles:
			className = something.name + role.capitalize()
			astOrText = selector(something, role, className)
			compiled = compile(astOrText, className + self.__class__.ext, "exec", optimize=2)
			globalz = {}
			eval(compiled, globalz)
			yield (role, globalz[className])

	def _toClasses(self, compResult):
		return self._somethingToIterable(compResult, lambda compResult, role, className: getattr(compResult, role)[0].content)
