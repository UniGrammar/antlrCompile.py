import typing

from ..ANTLRInternalClasses import ANTLRInternalClasses
from ..antlr import neededAntlrRuntimeClasses, getAntlrPath

class ANTLRInternalClassesJava(ANTLRInternalClasses):

	__slots__ = ("ji", "javaCompile", "antlrClassPath")

	ext = ".java"
	extLen = len(ext)

	_necessaryRoles = ("lexer", "parser", "listener")

	def __init__(self):
		from JAbs import SelectedJVMInitializer

		self.antlrClassPath = getAntlrPath()
		self.ji = SelectedJVMInitializer(
			[
				self.antlrClassPath
			],
			neededAntlrRuntimeClasses + ["org.antlr.v4.runtime.Parser"]
		)

		from javaMdktCompiler import javaCompile
		self.javaCompile = javaCompile

	def CharStreams(self, src):
		return self.ji.CharStreams.fromString(src)

	def CommonTokenStream(self, lexer):
		return self.ji.CommonTokenStream(lexer)

	def generateArgsForCompiler(self) -> typing.Tuple[str, ...]:
		return ("-cp", str(self.antlrClassPath))

	def _toClasses(self, compResult):
		targets = []
		remap = []
		for role in self.__class__._necessaryRoles:
			files = getattr(compResult, role)
			if len(files) == 1:
				for f in files:
					pyName = str(f.name)
					if pyName.endswith(self.__class__.ext):
						stem = pyName[: -self.__class__.extLen]
						remap.append((role, stem))
						targets.append((stem, f.content))
		compiled = self.javaCompile(targets, *self.generateArgsForCompiler())

		for role, stem in remap:
			yield (str(role), compiled[stem])
