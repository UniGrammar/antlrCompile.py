import typing
from abc import ABC, abstractmethod
from collections import OrderedDict
from pathlib import Path

from UniGrammarRuntimeCore.IParser import IParser, IParserFactory
from UniGrammarRuntimeCore.PoolManager import PoolManager

from .backends import langs2InternalMapping


class ANTLRParser(IParser):
	ext = None
	NAME = "antlr4"

	__slots__ = ("lexer", "parser", "listenerClass", "backend", "mainProductionName")

	def __init__(self, backend: typing.Type["ANTLRInternalClasses"], lexerClass=None, parserClass=None, listenerClass=None) -> None:
		self.backend = backend
		self.lexer = lexerClass(None)
		self.parser = parserClass(None)
		self.listenerClass = listenerClass
		self.mainProductionName = str(next(iter(self.ruleNames)))

	@property
	def ruleNames(self):
		return self.parser.ruleNames

	def lex(self, src: str) -> "antlr4.CommonTokenStream.CommonTokenStream":
		inputStream = self.backend.CharStreams(src)
		self.lexer.inputStream = inputStream
		tokensStream = self.backend.CommonTokenStream(self.lexer)
		return tokensStream

	def _parse(self, s: str, trace: bool=False) -> None:
		tokensStream = self.lex(s)
		self.parser.setTrace(trace)
		self.parser.setInputStream(tokensStream)  # fucking crazy shit, for lexer there is a property and no accessor methods, for parser there is no property and there ar accessor methods

	def _getTree(self):
		return getattr(self.parser, self.mainProductionName)()

	def __call__(self, s: str, trace: bool=False):
		"""Tree can be consumed only once!"""
		self._parse(s, trace)
		return self._getTree()


class CompilationResult(ABC):
	__slots__ = ("res", "language", "name", "mainProductionName")
	_dirRes = None

	def __init__(self, res, language, name: str):
		self.res = res
		self.language = language
		self.name = name

	def __iter__(self):
		for elWithRole in self.res:
			role = elWithRole.role
			el = elWithRole.files
			if el is not None:
				yield el

	def saveToDisk(self, root: Path = "."):
		root = Path(root)
		for files in self:
			if len(files) == 1:
				for f in files:
					(root / f.name).write_text(f.content)
			else:
				for i, f in enumerate(files):
					(root / (f.name + "_" + str(i))).write_text(f.content)

	def asRoleFilesItems(self):
		for elWithRole in self.res:
			role = elWithRole.role
			el = elWithRole.files
			if el is not None:
				yield (role, el)

	def rolesItems(self):
		for elWithRole in self.res:
			role = elWithRole.role
			if elWithRole.files is not None:
				yield role

	def roles(self):
		return tuple(self.rolesItems())

	def asNameContentItems(self) -> typing.Iterator[typing.Tuple[str, str]]:
		for el in self:
			for f in el:
				yield (f.name, f.content)

	def asFileNameDict(self) -> OrderedDict:
		return OrderedDict(self.asNameContentItems())

	def asRoleFilesDict(self):
		return OrderedDict(self.asRoleFilesItems())

	def __getattr__(self, k):
		return getattr(self.res, k)

	def __dir__(self):
		if self.__class__._dirRes is None:
			d = set(dir(self.res)) | set(self.__slots__) | set(dir(self.__class__))
			self.__class__._dirRes = frozenset({p for p in d if not (len(p) >= 1 and p[0] == "_")})

		return self.__class__._dirRes

	def toParser(self):
		return ANTLRParserFactory().fromCompResult(self)


backendsPool = PoolManager()

class ANTLRParserFactory(IParserFactory):
	__slots__ = ()

	PARSER_CLASS = ANTLRParser

	def _fromAttrIterable(self, backend: typing.Type["ANTLRInternalClasses"], something: typing.Iterator[typing.Tuple[str, type]]) -> ANTLRParser:
		return self.__class__.PARSER_CLASS(backend, **{(role + "Class"): ctor for role, ctor in something})

	def fromCompResult(self, compResult: CompilationResult) -> ANTLRParser:
		backend = backendsPool(langs2InternalMapping[compResult.language])
		return self._fromAttrIterable(backend, backend._toClasses(compResult))

	def fromInternal(self, internalRepr: CompilationResult) -> ANTLRParser:
		return self.fromCompResult(internalRepr)

