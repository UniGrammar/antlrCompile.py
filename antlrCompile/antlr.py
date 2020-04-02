from enum import Enum
from pathlib import Path

antlrNs = "org.antlr"
antlrRuntimeNs = antlrNs + ".runtime"
antlrVNs = antlrNs + ".v4"
antlrVRuntimeNs = antlrVNs + ".runtime"

neededAntlrClasses = [
	antlrVNs + ".tool.Grammar",
	antlrVNs + ".parse.ANTLRParser",
	antlrVNs + ".Tool",
	antlrVNs + ".analysis.AnalysisPipeline",

	antlrRuntimeNs + ".ANTLRFileStream",
	antlrRuntimeNs + ".ANTLRStringStream",
]

neededAntlrRuntimeClasses = [
	antlrVRuntimeNs + ".CharStream",
	antlrVRuntimeNs + ".CharStreams",
	antlrVRuntimeNs + ".TokenStream",
	antlrVRuntimeNs + ".CommonTokenStream",
]

# todo: get targets via reflection from org.antlr.v4.codegen.target (class names are <target_name>Target)


def getAntlrPath() -> Path:
	return Path("./antlr4-4.11.2-SNAPSHOT-complete.jar")


class ANTLRLanguage(Enum):
	Python3 = "Python3"
	Python2 = "Python2"
	Java = "Java"
	Cpp = "Cpp"
	CSharp = "CSharp"
	Go = "Go"
	ECMAScript = JavaScript = "JavaScript"
	PHP = "PHP"
	Swift = "Swift"
