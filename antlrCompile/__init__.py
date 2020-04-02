import typing
from abc import ABC, abstractmethod
from pathlib import Path
from collections import OrderedDict, defaultdict
import threading

from .antlr import neededAntlrClasses, getAntlrPath, ANTLRLanguage
from .core import CompilationResult

from UniGrammarRuntimeCore.ICompiler import ICompiler


class ANTLR(ICompiler):
	__slots__ = ("ji", "t")

	def __init__(self) -> None:
		from JAbs import SelectedJVMInitializer

		antlrClassPath = getAntlrPath()
		self.ji = SelectedJVMInitializer(
			[
				antlrClassPath
			],
			neededAntlrClasses
		)

		self.t = self.ji.Tool()
		self.t.outputDirectory = None

	def parse(self, grammar: typing.Union[Path, str]):
		if isinstance(grammar, Path):
			gF = grammar.absolute()
			gT = gF.read_text()
		elif isinstance(grammar, str):
			gT = grammar

		return self.t.parseGrammarFromString(gT)

	def compileStr(self, grammarText: str, target: ANTLRLanguage = None, fileName: typing.Union[Path, str] = "grammar.g4") -> CompilationResult:
		"""Parses the DSL string and generates internal object from it. `fileName` must not be used for retrieving source, instead it must provide hints, useful for caching or more meaningful error messages and may be just ignored if the backend doesn't support its usage this way."""

		target = ANTLRLanguage(target)
		rAST = self.parse(grammarText)

		if fileName is None:
			fileName = "grammar.g4"
		else:
			fileName = str(fileName)

		rAST.defaultOptions["language"] = target.value

		g = self.t.createGrammar(rAST)
		#print(g.ast.toStringTree())

		g.fileName = fileName

		res = self.t.processInMemory(g, True)

		#r = g.getRule(0)
		#mainRuleName = r.name

		return CompilationResult(res, target, g.name)

	def compile(self, grammar: typing.Union[Path, str], target: ANTLRLanguage = ANTLRLanguage.Python3, fileName: typing.Optional[typing.Union[Path, str]] = None) -> CompilationResult:
		if isinstance(grammar, Path):
			assert fileName is None
			return self.compileFile(grammar, target)
		return self.compileStr(grammar, target, fileName)


class Vis:
	__slots__ = ("ji", "MyListener")
	def __init__(self) -> None:
		from JAbs import SelectedJVMInitializer

		antlrClassPath = getAntlrPath()
		self.ji = SelectedJVMInitializer(
			[
				antlrClassPath
			],
			[
				"org.antlr.v4.gui.Trees",
				"org.antlr.v4.gui.TreePostScriptGenerator",
				"java.util.ArrayList",
				"java.util.Arrays",
				"java.awt.event.WindowListener"
			]
		)

		class MyListener(self.ji.WindowListener, metaclass=self.ji._Implements):
			# fuck, no __slots__ here
			def __init__(self, e: threading.Event):
				self.e = e

			@self.ji._Override
			def windowClosed(self, e: "java.awt.event.WindowEvent"):
				pass
				self.e.set()

			@self.ji._Override
			def windowClosing(self, e: "java.awt.event.WindowEvent"):
				pass
			@self.ji._Override
			def windowOpened(self, e: "java.awt.event.WindowEvent"):
				pass
			@self.ji._Override
			def windowIconified(self, e: "java.awt.event.WindowEvent"):
				pass
			@self.ji._Override
			def windowDeiconified(self, e: "java.awt.event.WindowEvent"):
				pass
			@self.ji._Override
			def windowActivated(self, e: "java.awt.event.WindowEvent"):
				pass
			@self.ji._Override
			def windowDeactivated(self, e: "java.awt.event.WindowEvent"):
				pass

		self.MyListener = MyListener

	def blockOnGUIWindow(self, wind):
		"""Blocks untill window is closed"""
		e = threading.Event()
		listn = self.MyListener(e)
		wind.addWindowListener(listn)
		e.wait()

	def treeGUIVisualization(self, parser: "ANTLRParser", source: str, block: bool=True) -> None:
		"""Shows a GUI dialog with parse tree"""
		fullTree = parser(source)
		task = self.ji.Trees.inspect(fullTree, self.ji.Arrays.asList(parser.ruleNames))
		wind = task.get()

		if block:
			self.blockOnGUIWindow(wind)

		return wind

	def treePostScriptVisualization(self, parser: "ANTLRParser", source: str, fontName: str = "Helvetica", fontSize: int = 11, gapBetweenLevels: typing.Optional[float] = None, gapBetweenNodes: typing.Optional[float] = None, nodeWidthPadding: typing.Optional[int] = None, nodeHeightPaddingAbove: typing.Optional[int] = None, nodeHeightPaddingBelow: typing.Optional[int] = None) -> str:
		"""Returns a PostScript string for parse tree image"""
		fullTree = parser(source)

		g = self.ji.TreePostScriptGenerator(self.ji.Arrays.asList(parser.ruleNames), fullTree, fontName, fontSize)

		if gapBetweenLevels is not None:
			g.gapBetweenLevels = gapBetweenLevels
		if gapBetweenNodes is not None:
			g.gapBetweenNodes = gapBetweenNodes
		if nodeWidthPadding is not None:
			g.nodeWidthPadding = nodeWidthPadding
		if nodeHeightPaddingAbove is not None:
			g.nodeHeightPaddingAbove = nodeHeightPaddingAbove
		if nodeHeightPaddingBelow is not None:
			g.nodeHeightPaddingBelow = nodeHeightPaddingBelow

		return g.getPS()
