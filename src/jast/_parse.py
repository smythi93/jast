import enum

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

from jast._jast import JAST
from jast._parser.JavaLexer import JavaLexer
from jast._parser.JavaParser import JavaParser
from jast._parser._convert import JASTConverter


class ParseMode(enum.Enum):
    """
    The parse mode used to identify the Java code to parse
    """

    """
    Parse a complete Java compilation unit.
    """
    UNIT = "unit"
    """
    Parse a Java declaration.
    """
    DECL = "decl"
    """
    Parse a Java statement.
    """
    STMT = "stmt"
    """
    Parse a Java expression.
    """
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
    """
    Parse Java source code into an jAST.

    :param src:     The Java source code.
    :param mode:    The parse mode used to identify the java code.
                    The default is `ParseMode.UNIT` which is used to parse a complete Java compilation unit.
                    Other modes are `ParseMode.DECL`, `ParseMode.STMT`, and `ParseMode.EXPR`, for parsing
                    Java declarations, statements, and expressions, respectively.
    :return:        The jAST representing the Java source code.
    """
    return _parser.parse(src, mode)
