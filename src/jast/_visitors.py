import ast
from typing import Any

from jast._jast import JAST


class JNodeVisitor:
    # noinspection PyMethodMayBeStatic
    def default_result(self) -> Any:
        return None

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def aggregate_result(self, aggregate, result) -> Any:
        return result

    def visit(self, node: JAST):
        """Visit a node."""
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        # noinspection PyArgumentList
        return visitor(node)

    def generic_visit(self, node: JAST):
        aggregate = self.default_result()
        for field, value in node:
            if isinstance(value, list):
                for item in value:
                    result = self.visit(item)
                    aggregate = self.aggregate_result(aggregate, result)
            elif isinstance(value, JAST):
                result = self.visit(value)
                aggregate = self.aggregate_result(aggregate, result)
        return aggregate


class JNodeTransformer(JNodeVisitor):
    def generic_visit(self, node: JAST):
        for field, old_value in node:
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, JAST):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, JAST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, JAST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node
