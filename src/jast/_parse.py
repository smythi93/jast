import enum
from io import UnsupportedOperation

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

from jast._jast import JAST
from jast._parser.JavaLexer import JavaLexer
from jast._parser.JavaParser import JavaParser
from jast._parser._convert import JASTConverter


class ParseMode(enum.Enum):
    UNIT = "unit"
    DECL = "decl"
    STMT = "stmt"
    EXPR = "expr"


class _SimpleErrorListener(ErrorListener):
    # noinspection PyPep8Naming
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseCancellationException(f"Line {line}, Column {column}: error: {msg}")


class _Parser:
    def __init__(self):
        self._error_listener = _SimpleErrorListener()
        self._parse_modes = list(ParseMode)
        self._converter = JASTConverter()

    def parse(self, src: str, mode: ParseMode | str | int = ParseMode.UNIT) -> JAST:
        if isinstance(mode, str):
            mode = ParseMode(mode)
        elif isinstance(mode, int):
            mode = self._parse_modes[mode]
        stream = InputStream(src)
        lexer = JavaLexer(stream)
        lexer.addErrorListener(self._error_listener)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParser(token_stream)
        parser.addErrorListener(self._error_listener)

        if mode == ParseMode.UNIT:
            tree = parser.compilationUnit()
        elif mode == ParseMode.DECL:
            tree = parser.declarationStart()
        elif mode == ParseMode.STMT:
            tree = parser.statementStart()
        elif mode == ParseMode.EXPR:
            tree = parser.expressionStart()
        else:
            raise ValueError(f"Invalid ParseMode: {mode}")

        return self._converter.visit(tree)


_parser = _Parser()


def parse(src: str, mode: ParseMode | str | int = ParseMode.UNIT) -> JAST:
    return _parser.parse(src, mode)
