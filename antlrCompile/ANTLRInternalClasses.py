from abc import ABC, abstractmethod


class ANTLRInternalClasses(ABC):
	__slots__ = ()

	ext = None

	@abstractmethod
	def CharStreams(self, src):
		raise NotImplementedError

	@abstractmethod
	def CommonTokenStream(self, lexers):
		raise NotImplementedError

	@abstractmethod
	def _toClasses(self, compResult):
		raise NotImplementedError
