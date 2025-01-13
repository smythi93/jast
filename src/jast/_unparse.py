import ast

import jast._jast as jast

from jast._visitors import JNodeVisitor


ast.NodeVisitor.visit_Is()


class _Unparser(JNodeVisitor):
    def __init__(self, indent=4):
        self._indent = indent
        self._current_level = 0
        self._level_can_be_equal = False

    def visit_Identifier(self, node: jast.Identifier):
        return node.name
