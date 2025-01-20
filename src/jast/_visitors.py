from copy import copy
from typing import Any

from jast._jast import JAST


class JNodeVisitor:
    """
    A base node visitor class for JAST nodes.
    This class is meant to be subclassed, with the subclass adding visit methods for different node types.
    """

    # noinspection PyMethodMayBeStatic
    def default_result(self) -> Any:
        """
        Return the default result value.
        :return: The default result value.
        """
        return None

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def aggregate_result(self, aggregate, result) -> Any:
        """
        Aggregate a result into an aggregate value.
        :param aggregate:   The aggregate value.
        :param result:      The result to add to the aggregate.
        :return:            The new aggregate value.
        """
        return result

    def visit(self, node: JAST):
        """Visit a node."""
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        # noinspection PyArgumentList
        return visitor(node)

    def generic_visit(self, node: JAST):
        """
        Default visitor for nodes.
        :param node:    The node to visit.
        :return:        The result of the visit.
        """
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
    """
    A base node transformer class for JAST nodes.
    This class is meant to be subclassed, with the subclass adding visit methods for different node types.
    The visiting modifies the original jAST.
    """

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


class JNodeKeepTransformer(JNodeTransformer):
    """
    A base node transformer class for JAST nodes.
    This class is meant to be subclassed, with the subclass adding visit methods for different node types.
    The visiting keeps the original jAST.
    """

    def generic_visit(self, node: JAST):
        node = copy(node)
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
