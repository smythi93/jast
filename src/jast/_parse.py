import enum

from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

from jast._jast import JAST
from jast._parser import sa_java
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
    Parse a Java decl.
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
    """
    Parse a Java module directive.
    """
    DIRE = "dire"


class _SimpleErrorListener(ErrorListener):
    # noinspection PyPep8Naming
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseCancellationException(f"Line {line}, Column {column}: error: {msg}")


class _SpeedyAntlrErrorListener(sa_java.SA_ErrorListener):
    """This is invoked from the speedy ANTLR parser when a syntax error is encountered"""

    def __init__(self, filename=None):
        self.filename = filename
        super().__init__()

    def syntaxError(
        self,
        input_stream,
        offending_symbol,
        char_index: int,
        line: int,
        column: int,
        msg,
    ):
        raise ParseCancellationException(f"Line {line}, Column {column}: error: {msg}")


class _Parser:
    def __init__(self):
        self._parse_modes = list(ParseMode)
        self._converter = JASTConverter()

    def parse(
        self,
        src: str,
        mode: ParseMode | str | int = ParseMode.UNIT,
        legacy: bool = False,
    ) -> JAST:
        if isinstance(mode, str):
            mode = ParseMode(mode)
        elif isinstance(mode, int):
            mode = self._parse_modes[mode]
        stream = InputStream(src)

        if mode == ParseMode.UNIT:
            entry_rule_name = "compilationUnit"
        elif mode == ParseMode.DECL:
            entry_rule_name = "declarationStart"
        elif mode == ParseMode.STMT:
            entry_rule_name = "statementStart"
        elif mode == ParseMode.DIRE:
            entry_rule_name = "directiveStart"
        else:
            entry_rule_name = "expressionStart"
        if True or legacy or not sa_java.USE_CPP_IMPLEMENTATION:
            error_listener = _SimpleErrorListener()
            parser = sa_java._py_parse
        else:
            error_listener = _SpeedyAntlrErrorListener()
            parser = sa_java._cpp_parse
        tree = parser(stream, entry_rule_name, error_listener)

        return self._converter.visit(tree)


_parser = _Parser()


def parse(
    src: str, mode: ParseMode | str | int = ParseMode.UNIT, legacy: bool = False
) -> JAST:
    """
    Parse Java source code into an jAST.

    :param src:     The Java source code.
    :param mode:    The parse mode used to identify the java code.
                    The default is `ParseMode.UNIT` which is used to parse a complete Java compilation unit.
                    Other modes are `ParseMode.DECL`, `ParseMode.STMT`, and `ParseMode.EXPR`, for parsing
                    Java declarations, statements, and expressions, respectively.
    :param legacy:  If True, use the legacy parser implementation.
    :return:        The jAST represents the Java source code.
    """
    return _parser.parse(src, mode, legacy)
