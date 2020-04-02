from .java import ANTLRInternalClassesJava
from .python import ANTLRInternalClassesPython
from ..antlr import ANTLRLanguage

langs2InternalMapping = {
	ANTLRLanguage.Java: ANTLRInternalClassesJava,
	ANTLRLanguage.Python3: ANTLRInternalClassesPython,
}
