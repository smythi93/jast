"""
This module contains the abstract syntax tree (AST) classes for the Java AST (JAST).
"""

import abc
from typing import List, Any, Iterator, Tuple, Union


class JAST(abc.ABC):
    """
    Abstract base class for all JAST classes.
    """

    def __init__(self, **kwargs):
        """
        Fallback constructor for all JAST classes.
        :param kwargs: keyword arguments
        """
        pass

    def __hash__(self):
        """
        Hash function for JAST classes.
        :return: hash value
        """
        return hash(id(self))

    def __iter__(self) -> Iterator[Tuple[str, "JAST" | List["JAST"]]]:
        """
        Iterates over the fields of the JAST class.
        :return:
        """
        return iter([])

    def __copy__(self):
        """
        Copy function for JAST classes.
        :return: copy of the JAST class
        """
        obj = jtype(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj


class _JAST(JAST, abc.ABC):
    """
    Abstract base class for all JAST classes that have a location in the source code.
    """

    def __init__(
        self,
        lineno: int = None,
        col_offset: int = None,
        end_lineno: int = None,
        end_col_offset: int = None,
        **kwargs,
    ):
        """
        Constructor for all JAST classes that have a location in the source code.

        :param lineno:          The starting line number of the JAST class.
        :param col_offset:      The starting column offset of the JAST class.
        :param end_lineno:      The ending line number of the JAST class.
        :param end_col_offset:  The ending column offset of the JAST class.
        :param kwargs:          keyword arguments
        """
        super().__init__(**kwargs)
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset


# Identifiers


class identifier(_JAST, str):
    """
    Represents an identifier in the Java AST.
    """

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)


# Names


class qname(_JAST):
    """
    Represents a qualified qname in the Java AST.

    <identifier>.<identifier>.<identifier>...
    """

    def __init__(self, identifiers: List[identifier] = None, **kwargs):
        super().__init__(**kwargs)
        if not identifiers:
            raise ValueError("identifier is required for qname")
        self.identifiers = identifiers

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifiers", self.identifiers


# Literals


class Literal(_JAST, abc.ABC):
    """
    Abstract base class for all literal values in the Java AST.
    """

    def __init__(self, value: Any, **kwargs):
        super().__init__(**kwargs)
        self.value = value


class IntegerLiteral(Literal):
    """
    Represents an integer literal in the Java AST.
    """

    def __init__(self, value: int, long: bool = False, **kwargs):
        super().__init__(value, **kwargs)
        self.long = long


class FloatLiteral(Literal):
    """
    Represents a float literal in the Java AST.
    """

    def __init__(self, value: float, double: bool = False, **kwargs):
        super().__init__(value, **kwargs)
        self.double = double


class BoolLiteral(Literal):
    """
    Represents a boolean literal in the Java AST.
    """

    def __init__(self, value: bool, **kwargs):
        super().__init__(value, **kwargs)


class CharLiteral(Literal):
    """
    Represents a character literal in the Java AST.
    """

    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)


class StringLiteral(Literal):
    """
    Represents a string literal in the Java AST.
    """

    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)


class TextBlock(Literal):
    """
    Represents a text block literal in the Java AST.
    """

    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)


class NullLiteral(Literal):
    """
    Represents a null literal in the Java AST.
    """

    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)


# Modifiers


class modifier(_JAST, abc.ABC):
    """
    Abstract base class for all modifiers in the Java AST.
    """


class Transitive(modifier):
    """
    Represents the transitive modifier in the Java AST.
    """


class Static(modifier):
    """
    Represents the static modifier in the Java AST.
    """


class Public(modifier):
    """
    Represents the public modifier in the Java AST.
    """


class Protected(modifier):
    """
    Represents the protected modifier in the Java AST.
    """


class Private(modifier):
    """
    Represents the private modifier in the Java AST.
    """


class Abstract(modifier):
    """
    Represents the abstract modifier in the Java AST.
    """


class Final(modifier):
    """
    Represents the final modifier in the Java AST.
    """


class Sealed(modifier):
    """
    Represents the sealed modifier in the Java AST.
    """


class NonSealed(modifier):
    """
    Represents the non-sealed modifier in the Java AST.
    """


class Strictfp(modifier):
    """
    Represents the strictfp modifier in the Java AST.
    """


class Transient(modifier):
    """
    Represents the transient modifier in the Java AST.
    """


class Volatile(modifier):
    """
    Represents the volatile modifier in the Java AST.
    """


class Synchronized(modifier):
    """
    Represents the synchronized modifier in the Java AST.
    """


class Native(modifier):
    """
    Represents the native modifier in the Java AST.
    """


class Default(modifier):
    """
    Represents the default modifier in the Java AST.
    """


class ElementValuePair(_JAST):
    """
    Represents an element-value pair in the Java AST.

    <id> = <value>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, value: "element" = None, **kwargs):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required for ElementValuePair")
        if value is None:
            raise ValueError("value is required for ElementValuePair")
        self.id = id
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        yield "value", self.value


class ElementValueArrayInitializer(_JAST):
    """
    Represents an element-value array initializer in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(self, values: List["element"] = None, **kwargs):
        super().__init__(**kwargs)
        self.values = values or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "values", self.values


class Annotation(modifier):
    """
    Represents an annotation in the Java AST.

    @<qname>(<element-value-pairs>)
    """

    def __init__(
        self,
        name: qname = None,
        elements: List[Union[ElementValuePair, "element"]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for Annotation")
        self.name = name
        self.elements = elements

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name
        if self.elements:
            yield "elements", self.elements


"""
Represents a jtype for element values in the Java AST.
"""
element = Union[ElementValueArrayInitializer, Annotation, "Expr"]


# Types


# noinspection PyShadowingBuiltins
class jtype(_JAST, abc.ABC):
    """
    Abstract base class for all types in the Java AST.
    """


class Void(jtype):
    """
    Represents the void jtype in the Java AST.
    """


class Var(jtype):
    """
    Represents var for variable types in the Java AST.
    """


class PrimitiveType(jtype, abc.ABC):
    """
    Abstract base class for all primitive types in the Java AST.
    """

    def __init__(self, annotations: List[Annotation] = None, **kwargs):
        super().__init__(**kwargs)
        self.annotations = annotations or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations


class Boolean(PrimitiveType):
    """
    Represents the boolean primitive jtype in the Java AST.
    """


class Byte(PrimitiveType):
    """
    Represents the byte primitive jtype in the Java AST.
    """


class Short(PrimitiveType):
    """
    Represents the short primitive jtype in the Java AST.
    """


class Int(PrimitiveType):
    """
    Represents the int primitive jtype in the Java AST.
    """


class Long(PrimitiveType):
    """
    Represents the long primitive jtype in the Java AST.
    """


class Char(PrimitiveType):
    """
    Represents the char primitive jtype in the Java AST.
    """


class Float(PrimitiveType):
    """
    Represents the float primitive jtype in the Java AST.
    """


class Double(PrimitiveType):
    """
    Represents the double primitive jtype in the Java AST.
    """


class WildcardBound(_JAST):
    """
    Represents a wildcard bound in the Java AST.

    (extends | super) <jtype>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: jtype = None,
        extends: bool = False,
        super_: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for WildcardBound")
        if extends == super_:
            raise ValueError(
                "extends and super_ are mutually exclusive for WildcardBound"
            )
        self.type = type
        self.extends = extends
        self.super = super_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type


class Wildcard(jtype):
    """
    Represents a wildcard jtype in the Java AST.

    <annotation>* ? [<bound>]
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        bound: WildcardBound = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.annotations = annotations or []
        self.bound = bound

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        if self.bound:
            yield "bound", self.bound


class TypeArguments(_JAST):
    """
    Represents jtype arguments in the Java AST.

    < <jtype>, <jtype>, ... >
    """

    def __init__(self, types: List[jtype] = None, **kwargs):
        super().__init__(**kwargs)
        if types is None:
            raise ValueError("types is required for TypeArguments")
        self.types = types

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class Coit(jtype):
    """
    Represents a simple class or interface jtype in the Java AST.

    <annotation>* <id>[<jtype-arguments>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        type_arguments: TypeArguments = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required")
        self.annotations = annotations or []
        self.id = id
        self.type_arguments = type_arguments

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id
        if self.type_arguments:
            yield "type_arguments", self.type_arguments


class ClassType(jtype):
    """
    Represents a class jtype in the Java AST.

    <annotation>* <coit>.<coit>.<coit>...
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        coits: List[Coit] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not coits:
            raise ValueError("coits is required")
        self.annotations = annotations or []
        self.coits = coits

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "coits", self.coits


class Dim(_JAST):
    """
    Represents a dimension in the Java AST.

    []
    """

    def __init__(self, annotations: List[Annotation] = None, **kwargs):
        super().__init__(**kwargs)
        self.annotations = annotations or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations


class ArrayType(jtype):
    """
    Represents an array jtype in the Java AST.

    <annotation>* <jtype>[]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        type: jtype = None,
        dims: List[Dim] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required")
        self.annotations = annotations or []
        self.type = type
        self.dims = dims or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "jtype", self.type
        if self.dims:
            yield "dims", self.dims


class VariableDeclaratorId(_JAST):
    """
    Represents a variable declarator id in the Java AST.

    <id><dim><dim>...
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, dims: List[Dim] = None, **kwargs):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required for VariableDeclaratorId")
        self.id = id
        self.dims = dims or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        if self.dims:
            yield "dims", self.dims


# jtype Parameters


class TypeBound(_JAST):
    """
    Represents a jtype bound in the Java AST.

    <annotation>* <jtype> & <jtype> & ...
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        types: List[jtype] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not types:
            raise ValueError("types is required for TypeBound")
        self.annotations = annotations or []
        self.types = types

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class typeparam(_JAST):
    """
    Represents a jtype parameter in the Java AST.

    <annotation>* <id> [<bound>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        bound: TypeBound = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required")
        self.annotations = annotations or []
        self.id = id
        self.bound = bound or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id
        if self.bound:
            yield "bound", self.bound


class typeparams(_JAST):
    """
    Represents jtype parameters in the Java AST.

    < <jtype-parameter>, <jtype-parameter>, ... >
    """

    def __init__(self, parameters: List[typeparam] = None, **kwargs):
        super().__init__(**kwargs)
        if not parameters:
            raise ValueError("parameters is required for typeparams")
        self.parameters = parameters

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "parameters", self.parameters


# Pattern


class Pattern(_JAST):
    """
    Represents a pattern in the Java AST.

    <modifier>* <jtype> <annotation>* <id>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        annotations: List[Annotation] = None,
        id: identifier = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for Pattern")
        if id is None:
            raise ValueError("id is required for Pattern")
        self.modifiers = modifiers or []
        self.type = type
        self.annotations = annotations or []
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id


class GuardedPattern(_JAST):
    """
    Represents a guarded pattern in the Java AST.

    <pattern> && <condition> && <condition> && ...
    """

    def __init__(
        self,
        pattern: Pattern = None,
        conditions: List["Expr"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if pattern is None:
            raise ValueError("pattern is required for GuardedPattern")
        if conditions is None:
            raise ValueError("condition is required for GuardedPattern")
        self.pattern = pattern
        self.conditions = conditions

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "pattern", self.pattern
        yield "conditions", self.conditions


# Operators


class OP(JAST, abc.ABC):
    """
    Abstract base class for all operators in the Java AST.
    """


class AssignmentOP(JAST, abc.ABC):
    """
    Abstract base class for all assignment operators in the Java AST.
    """


class Assign(AssignmentOP):
    """
    Represents the assignment operator in the Java AST.

    =
    """


class AddAssign(AssignmentOP):
    """
    Represents the addition assignment operator in the Java AST.

    +=
    """


class SubAssign(AssignmentOP):
    """
    Represents the subtraction assignment operator in the Java AST.

    -=
    """


class MulAssign(AssignmentOP):
    """
    Represents the multiplication assignment operator in the Java AST.

    *=
    """


class DivAssign(AssignmentOP):
    """
    Represents the division assignment operator in the Java AST.

    /=
    """


class ModAssign(AssignmentOP):
    """
    Represents the modulo assignment operator in the Java AST.

    %=
    """


class AndAssign(AssignmentOP):
    """
    Represents the bitwise AND assignment operator in the Java AST.

    &=
    """


class OrAssign(AssignmentOP):
    """
    Represents the bitwise OR assignment operator in the Java AST.

    |=
    """


class XorAssign(AssignmentOP):
    """
    Represents the bitwise XOR assignment operator in the Java AST.

    ^=
    """


class LShiftAssign(AssignmentOP):
    """
    Represents the left shift assignment operator in the Java AST.

    <<=
    """


class RShiftAssign(AssignmentOP):
    """
    Represents the right shift assignment operator in the Java AST.

    >>=
    """


class URShiftAssign(AssignmentOP):
    """
    Represents the unsigned right shift assignment operator in the Java AST.

    >>>=
    """


class Operator(OP, abc.ABC):
    """
    Abstract base class for all binary operators in the Java AST.
    """


class Or(Operator):
    """
    Represents the logical OR operator in the Java AST.

    ||
    """


class And(Operator):
    """
    Represents the logical AND operator in the Java AST.

    &&
    """


class BitOr(Operator):
    """
    Represents the bitwise OR operator in the Java AST.

    |
    """


class BitXor(Operator):
    """
    Represents the bitwise XOR operator in the Java AST.

    ^
    """


class BitAnd(Operator):
    """
    Represents the bitwise AND operator in the Java AST.

    &
    """


class Eq(Operator):
    """
    Represents the equality operator in the Java AST.

    ==
    """


class NotEq(Operator):
    """
    Represents the inequality operator in the Java AST.

    !=
    """


class Lt(Operator):
    """
    Represents the less than operator in the Java AST.

    <
    """


class LtE(Operator):
    """
    Represents the less than or equal to operator in the Java AST.

    <=
    """


class Gt(Operator):
    """
    Represents the greater than operator in the Java AST.

    >
    """


class GtE(Operator):
    """
    Represents the greater than or equal to operator in the Java AST.

    >=
    """


class LShift(Operator):
    """
    Represents the left shift operator in the Java AST.

    <<
    """


class RShift(Operator):
    """
    Represents the right shift operator in the Java AST.

    >>
    """


class URShift(Operator):
    """
    Represents the unsigned right shift operator in the Java AST.

    >>>
    """


class Add(Operator):
    """
    Represents the addition operator in the Java AST.

    +
    """


class Sub(Operator):
    """
    Represents the subtraction operator in the Java AST.

    -
    """


class Mul(Operator):
    """
    Represents the multiplication operator in the Java AST.

    *
    """


class Div(Operator):
    """
    Represents the division operator in the Java AST.

    /
    """


class Mod(Operator):
    """
    Represents the modulo operator in the Java AST.

    %
    """


class UnaryOperator(OP, abc.ABC):
    """
    Abstract base class for all unary operators in the Java AST.
    """


class PreInc(UnaryOperator):
    """
    Represents the pre-increment operator in the Java AST.

    ++
    """


class PreDec(UnaryOperator):
    """
    Represents the pre-decrement operator in the Java AST.

    --
    """


class UAdd(UnaryOperator):
    """
    Represents the unary plus operator in the Java AST.

    +
    """


class USub(UnaryOperator):
    """
    Represents the unary minus operator in the Java AST.

    -
    """


class Invert(UnaryOperator):
    """
    Represents the bitwise inversion operator in the Java AST.

    ~
    """


class Not(UnaryOperator):
    """
    Represents the logical negation operator in the Java AST.

    !
    """


class PostOperator(OP, abc.ABC):
    """
    Abstract base class for all post operators in the Java AST.
    """


class PostInc(PostOperator):
    """
    Represents the post-increment operator in the Java AST.
    """


class PostDec(PostOperator):
    """
    Represents the post-decrement operator in the Java AST.
    """


# Expressions


class Expr(_JAST, abc.ABC):
    """
    Abstract base class for all expressions in the Java AST.
    """

    def __init__(self, level: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.level = level


class Call(Expr):
    """
    Represents a function call in the Java AST.

    <function>(<argument>, <argument>, ...)
    """

    def __init__(
        self,
        function: Expr = None,
        arguments: List[Expr] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if function is None:
            raise ValueError("expr is required for Call")
        self.function = function
        self.arguments = arguments or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "function", self.function
        if self.arguments:
            yield "arguments", self.arguments


class Lambda(Expr):
    """
    Represents a lambda function in the Java AST.

    <parameter> -> <body>
    (<parameter>, <parameter>, ...) -> <body>
    """

    def __init__(
        self,
        parameters: identifier
        | List[identifier]
        | List[Union["param", "arity"]] = None,
        body: Union[Expr, "Block"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if parameters is None:
            raise ValueError("parameters is required for Lambda")
        if body is None:
            raise ValueError("body is required for Lambda")
        if isinstance(parameters, params) and parameters.receiver_parameter:
            raise ValueError("receiver_parameter is not allowed for Lambda")
        self.parameters = parameters
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "parameters", self.parameters
        yield "body", self.body


class Assignment(Expr):
    """
    Represents an assignment in the Java AST.

    <target> <op> <value>
    """

    def __init__(
        self,
        target: Expr = None,
        op: AssignmentOP = None,
        value: Expr = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if target is None:
            raise ValueError("target is required for Assignment")
        if op is None:
            raise ValueError("op is required for Assignment")
        if value is None:
            raise ValueError("value is required for Assignment")
        self.target = target
        self.op = op
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "target", self.target
        yield "op", self.op
        yield "value", self.value


class IfExp(Expr):
    """
    Represents an if expression in the Java AST.

    <test> ? <body> : <orelse>
    """

    def __init__(
        self,
        test: Expr = None,
        body: Expr = None,
        orelse: Expr = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if test is None:
            raise ValueError("test is required for IfExp")
        if body is None:
            raise ValueError("body is required for IfExp")
        if orelse is None:
            raise ValueError("orelse is required for IfExp")
        self.test = test
        self.body = body
        self.orelse = orelse

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body
        yield "orelse", self.orelse


class BinOp(Expr):
    """
    Represents a binary operation in the Java AST.

    <left> <op> <right>
    """

    def __init__(
        self, left: Expr = None, op: Operator = None, right: Expr = None, **kwargs
    ):
        super().__init__(**kwargs)
        if left is None:
            raise ValueError("left is required for BinOp")
        if op is None:
            raise ValueError("op is required for BinOp")
        if right is None:
            raise ValueError("right is required for BinOp")
        self.left = left
        self.op = op
        self.right = right

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "left", self.left
        yield "op", self.op
        yield "right", self.right


class InstanceOf(Expr):
    """
    Represents an instanceof expression in the Java AST.

    <expr> instanceof <jtype>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, expr: Expr = None, type: jtype | Pattern = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for InstanceOf")
        if type is None:
            raise ValueError("jtype is required for InstanceOf")
        self.expr = expr
        self.type = type

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "jtype", self.type


class UnaryOp(Expr):
    """
    Represents a unary operation in the Java AST.

    <op> <expr>
    """

    def __init__(self, op: UnaryOperator = None, expr: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if op is None:
            raise ValueError("op is required for UnaryOp")
        if expr is None:
            raise ValueError("expr is required for UnaryOp")
        self.op = op
        self.expr = expr

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "op", self.op
        yield "expr", self.expr


class PostUnaryOp(Expr):
    """
    Represents a post-unary operation in the Java AST.

    <expr> <op>
    """

    def __init__(self, expr: Expr = None, op: PostOperator = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for PostUnaryOp")
        if op is None:
            raise ValueError("op is required for PostUnaryOp")
        self.expr = expr
        self.op = op

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "op", self.op


class Cast(Expr):
    """
    Represents a cast expression in the Java AST.

    (<jtype>) <expr>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        type: TypeBound = None,
        expr: Expr = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for Cast")
        if expr is None:
            raise ValueError("expr is required for Cast")
        self.annotations = annotations or []
        self.type = type
        self.expr = expr

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "jtype", self.type
        yield "expr", self.expr


class NewObject(Expr):
    """
    Represents a new object creation in the Java AST.

    new <jtype>(<argument>, <argument>, ...) [{ <body> }]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type_arguments: TypeArguments = None,
        type: jtype = None,
        arguments: List[Expr] = None,
        body: List["declaration"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not type:
            raise ValueError("jtype is required for ObjectCreation")
        self.type_arguments = type_arguments
        self.type = type
        self.arguments = arguments or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "jtype", self.type
        if self.arguments:
            yield "arguments", self.arguments
        if self.body:
            yield "body", self.body


class NewInnerObject(Expr):
    """
    Represents a new inner object creation in the Java AST.

    <expr>.new <jtype>(<argument>, <argument>, ...) [{ <body> }]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type_arguments: TypeArguments = None,
        id: identifier = None,
        template_arguments: TypeArguments = None,
        arguments: List[Expr] = None,
        body: List["declaration"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required for ObjectCreation")
        self.type_arguments = type_arguments
        self.id = id
        self.template_arguments = template_arguments
        self.arguments = arguments or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "id", self.id
        if self.template_arguments:
            yield "template_arguments", self.template_arguments
        if self.arguments:
            yield "arguments", self.arguments
        if self.body:
            yield "body", self.body


class DimExpr(_JAST):
    """
    Represents a dimension expression in the Java AST.

    [ <expr> ]
    """

    def __init__(
        self, annotations: List[Annotation] = None, expr: Expr = None, **kwargs
    ):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for DimExpr")
        self.annotations = annotations or []
        self.expr = expr

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "expr", self.expr


class NewArray(Expr):
    """
    Represents a new array creation in the Java AST.

    new <jtype><dim_expr><dim_expr>...[<dim><dim>...]
    new <jtype><dim><dim>... [<initializer>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: jtype = None,
        expr_dims: List[DimExpr] = None,
        dims: List[Dim] = None,
        initializer: "ArrayInitializer" = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for ArrayCreation")
        if expr_dims and initializer:
            raise ValueError(
                "expr_dims and initializer are mutually exclusive for ArrayCreation"
            )
        self.type = type
        self.expr_dims = expr_dims
        self.dims = dims
        self.initializer = initializer

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        if self.expr_dims:
            yield "expr_dims", self.expr_dims
        if self.dims:
            yield "dims", self.dims
        if self.initializer:
            yield "initializer", self.initializer


class SwitchExprLabel(JAST, abc.ABC):
    """
    Abstract base class for all switch expression labels in the Java AST.
    """


class ExprCase(SwitchExprLabel):
    """
    Represents a case label for switch expressions in the Java AST.
    """


class ExprDefault(SwitchExprLabel):
    """
    Represents a default label for switch expressions in the Java AST.
    """


class SwitchExprRule(_JAST):
    """
    Represents a rule in a switch expression in the Java AST.
    """

    def __init__(
        self,
        label: SwitchExprLabel = None,
        cases: List[Expr | GuardedPattern] = None,
        arrow: bool = False,
        body: List["Statement"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if label is None:
            raise ValueError("label is required for SwitchExprRule")
        if not cases:
            raise ValueError("cases is required for SwitchExprRule")
        if not body:
            raise ValueError("body is required for SwitchExprRule")
        self.label = label
        self.cases = cases
        self.arrow = arrow
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "label", self.label
        yield "cases", self.cases
        yield "body", self.body


class SwitchExpr(Expr):
    """
    Represents a switch expression in the Java AST.
    """

    def __init__(
        self,
        expr: Expr = None,
        rules: List[SwitchExprRule] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for SwitchExpr")
        self.expr = expr
        self.rules = rules or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        if self.rules:
            yield "rules", self.rules


class This(Expr):
    """
    Represents the this expression in the Java AST.

    this
    """

    def __init__(
        self,
        arguments: List[Expr] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.arguments = arguments

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.arguments:
            yield "arguments", self.arguments


class Super(Expr):
    """
    Represents the super expression in the Java AST.

    super
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type_arguments: TypeArguments = None,
        id: identifier = None,
        arguments: List[Expr] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.type_arguments = type_arguments
        self.id = id
        self.arguments = arguments

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        if self.id:
            yield "id", self.id
        if self.arguments:
            yield "arguments", self.arguments


class Constant(Expr):
    """
    Represents a constant expression in the Java AST.

    <value>
    """

    def __init__(self, value: Literal = None, **kwargs):
        super().__init__(**kwargs)
        if value is None:
            raise ValueError("literal is required for Constant")
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value


class Name(Expr):
    """
    Represents a qname expression in the Java AST.

    <id>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, **kwargs):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required for Name")
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id


class ClassExpr(Expr):
    """
    Represents a class expression in the Java AST.

    <jtype>.class
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, **kwargs):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for ClassExpr")
        self.type = type

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type


class ExplicitGenericInvocation(Expr):
    """
    Represents an explicit generic invocation in the Java AST.
    """

    def __init__(
        self,
        type_arguments: TypeArguments = None,
        expr: Expr = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for ExplicitGenericInvocation")
        self.type_arguments = type_arguments
        self.expr = expr

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "expr", self.expr


class ArrayAccess(Expr):
    """
    Represents an array access in the Java AST.

    <expr>[<index>]
    """

    def __init__(self, expr: Expr = None, index: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for ArrayAccess")
        if index is None:
            raise ValueError("index is required for ArrayAccess")
        self.expr = expr
        self.index = index

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "index", self.index


class Member(Expr):
    """
    Represents a member access in the Java AST.

    <expr>.<member>
    """

    def __init__(self, expr: Expr = None, member: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for Member")
        if member is None:
            raise ValueError("member is required for Member")
        self.expr = expr
        self.member = member

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "member", self.member


class Reference(Expr):
    """
    Represents a method reference in the Java AST.

    <jtype>::<id>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: Expr | jtype = None,
        type_arguments: TypeArguments = None,
        id: identifier = None,
        new: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for Reference")
        if new and identifier:
            raise ValueError("new and id are mutually exclusive for Reference")
        if new == bool(id):
            raise ValueError("new and id are mutually exclusive for Reference")
        self.type = type
        self.type_arguments = type_arguments
        self.id = id
        self.new = new

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        if self.id:
            yield "id", self.id


# Arrays


class ArrayInitializer(_JAST):
    """
    Represents an array initializer in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(self, values: List[Union[Expr, "ArrayInitializer"]] = None, **kwargs):
        super().__init__(**kwargs)
        self.values = values or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "values", self.values


# Parameters


class receiver(_JAST):
    """
    Represents a receiver parameter in the Java AST.
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: jtype = None,
        identifiers: List[identifier] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for receiver")
        self.type = type
        self.identifiers = identifiers

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        if self.identifiers:
            yield "identifiers", self.identifiers


class param(_JAST):
    """
    Represents a parameter in the Java AST.

    <modifier>* <jtype> <id>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        id: VariableDeclaratorId = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for param")
        if id is None:
            raise ValueError("id is required for param")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "id", self.id


class arity(_JAST):
    """
    Represents a variable arity parameter in the Java AST.
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        annotations: List[Annotation] = None,
        id: VariableDeclaratorId = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for arity")
        if id is None:
            raise ValueError("id is required for arity")
        self.modifiers = modifiers or []
        self.type = type
        self.annotations = annotations or []
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id


class params(_JAST):
    """
    Represents formal parameters in the Java AST.

    (<receiver-parameter>, <parameter>, ...)
    (<parameter>, <parameter>, ...)
    """

    def __init__(
        self,
        receiver_parameter: receiver = None,
        parameters: List[param | arity] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.receiver_parameter = receiver_parameter
        self.parameters = parameters or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.receiver_parameter:
            yield "receiver_parameter", self.receiver_parameter
        if self.parameters:
            yield "parameters", self.parameters


# Statements


class Statement(_JAST, abc.ABC):
    """
    Abstract base class for all statements in the Java AST.
    """


class LocalClassDeclaration(Statement):
    """
    Represents a local class declaration in the Java AST.

    class { <declaration> <declaration> ... }
    """

    def __init__(self, declaration: "Class" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalClassDeclaration")
        self.declaration = declaration

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalInterfaceDeclaration(Statement):
    """
    Represents a local interface declaration in the Java AST.

    interface { <declaration> <declaration> ... }
    """

    def __init__(self, declaration: "Interface" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalInterfaceDeclaration")
        self.declaration = declaration

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalRecordDeclaration(Statement):
    """
    Represents a local record declaration in the Java AST.

    record { <declaration> <declaration> ... }
    """

    def __init__(self, declaration: "Record" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalRecordDeclaration")
        self.declaration = declaration

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalVariableDeclaration(Statement):
    """
    Represents a local variable declaration in the Java AST.

    <modifier>* <jtype> <declarator>, <declarator>, ...;
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        declarators: List["declarator"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for LocalVariableDeclaration")
        if not declarators:
            raise ValueError("declarators is required for LocalVariableDeclaration")
        self.modifiers = modifiers or []
        self.type = type
        self.declarators = declarators

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "declarators", self.declarators


class Block(Statement):
    """
    Represents a block statement in the Java AST.

    { <statement> <statement> ... }
    """

    def __init__(self, body: List[Statement] = None, **kwargs):
        super().__init__(**kwargs)
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


class Compound(Statement):
    """
    Represents a compound statement in the Java AST.

    <statement> <statement> ...
    """

    def __init__(self, statements: List[Statement] = None, **kwargs):
        super().__init__(**kwargs)
        self.statements = statements or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "statements", self.statements


class Empty(Statement):
    """
    Represents an empty statement in the Java AST.

    ;
    """


class Labeled(Statement):
    """
    Represents a labeled statement in the Java AST.

    <id>: <statement>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, body: Statement = None, **kwargs):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required for LabeledStatement")
        if body is None:
            raise ValueError("statement is required for LabeledStatement")
        self.id = id
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        yield "body", self.body


class Expression(Statement):
    """
    Represents an expression statement in the Java AST.

    <expression>;
    """

    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for ExpressionStatement")
        self.expression = expression

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


class If(Statement):
    """
    Represents an if statement in the Java AST.

    if (<test>) <body> [else <orelse>]
    """

    def __init__(
        self,
        test: Expr = None,
        body: Statement = None,
        orelse: Statement = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if test is None:
            raise ValueError("test is required for IfStatement")
        if body is None:
            raise ValueError("then_statement is required for IfStatement")
        self.test = test
        self.body = body
        self.orelse = orelse

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body
        if self.orelse:
            yield "else_statement", self.orelse


class Assert(Statement):
    """
    Represents an assert statement in the Java AST.

    assert <test> [ : <message> ];
    """

    def __init__(self, test: Expr = None, message: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if test is None:
            raise ValueError("condition is required for AssertStatement")
        self.test = test
        self.message = message

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        if self.message:
            yield "message", self.message


class SwitchLabel(_JAST, abc.ABC):
    """
    Abstract base class for all switch labels in the Java AST.
    """


class Match(Expr):
    """
    Represents a match for switch statements in the Java AST.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, ident: identifier = None, **kwargs):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for Match")
        if ident is None:
            raise ValueError("ident is required for Match")
        self.type = type
        self.ident = ident

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        yield "ident", self.ident


class Case(SwitchLabel):
    """
    Represents a case label for switch statements in the Java AST.

    case <expression>:
    """

    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if not expression:
            raise ValueError("constants is required for Case")
        self.expression = expression

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


class DefaultCase(SwitchLabel):
    """
    Represents a default label for switch statements in the Java AST.

    default:
    """


class Throw(Statement):
    """
    Represents a throw statement in the Java AST.

    throw <expression>;
    """

    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for ThrowStatement")
        self.expression = expression

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


class SwitchGroup(_JAST):
    """
    Represents a group of switch labels in the Java AST.
    """

    def __init__(
        self,
        labels: List[SwitchLabel] = None,
        statements: List[Statement] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not labels:
            raise ValueError("labels is required for SwitchGroup")
        if not statements:
            raise ValueError("statements is required for SwitchGroup")
        self.labels = labels
        self.statements = statements

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "labels", self.labels
        yield "statements", self.statements


class SwitchBlock(_JAST):
    """
    Represents a block of switch groups and labels in the Java AST.
    """

    def __init__(
        self,
        groups: List[SwitchGroup] = None,
        labels: List[SwitchLabel] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.groups = groups or []
        self.labels = labels or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "groups", self.groups
        yield "labels", self.labels


class Switch(Statement):
    """
    Represents a switch statement in the Java AST.

    switch (<expression>) { <block> }
    """

    def __init__(self, expression: Expr = None, block: SwitchBlock = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for SwitchStatement")
        if not block:
            raise ValueError("blocks is required for SwitchStatement")
        self.expression = expression
        self.block = block

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression
        yield "block", self.block


class While(Statement):
    """
    Represents a while statement in the Java AST.

    while (<test>) <body>
    """

    def __init__(self, test: Expr = None, body: Statement = None, **kwargs):
        super().__init__(**kwargs)
        if test is None:
            raise ValueError("test is required for WhileStatement")
        if body is None:
            raise ValueError("statement is required for WhileStatement")
        self.test = test
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body


class DoWhile(Statement):
    """
    Represents a do-while statement in the Java AST.

    do <body> while (<test>)
    """

    def __init__(self, body: Statement = None, test: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if body is None:
            raise ValueError("statement is required for DoWhileStatement")
        if test is None:
            raise ValueError("test is required for DoWhileStatement")
        self.body = body
        self.test = test

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body
        yield "test", self.test


class For(Statement):
    """
    Represents a for statement in the Java AST.

    for (<init>; <test>; <update>) <body>
    """

    def __init__(
        self,
        init: List[Expr] | LocalVariableDeclaration = None,
        test: Expr = None,
        update: List[Expr] = None,
        body: Statement = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if body is None:
            raise ValueError("statement is required for ForStatement")
        self.init = init or []
        self.test = test
        self.update = update or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.init:
            yield "init", self.init
        if self.test:
            yield "test", self.test
        if self.update:
            yield "update", self.update
        yield "body", self.body


class ForEach(Statement):
    """
    Represents a for-each statement in the Java AST.

    for (<jtype> <id> : <expression>) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        id: VariableDeclaratorId = None,
        expression: Expr = None,
        body: Statement = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for ForEachStatement")
        if id is None:
            raise ValueError("id is required for ForEachStatement")
        if expression is None:
            raise ValueError("expression is required for ForEachStatement")
        if body is None:
            raise ValueError("body is required for ForEachStatement")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id
        self.expression = expression
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "id", self.id
        yield "expression", self.expression
        yield "body", self.body


class Break(Statement):
    """
    Represents a break statement in the Java AST.

    break [<id>];
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, **kwargs):
        super().__init__(**kwargs)
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.id:
            yield "id", self.id


class Continue(Statement):
    """
    Represents a continue statement in the Java AST.

    continue [<id>];
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, **kwargs):
        super().__init__(**kwargs)
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.id:
            yield "id", self.id


class Return(Statement):
    """
    Represents a return statement in the Java AST.

    return [<expression>];
    """

    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        self.expression = expression

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.expression:
            yield "expression", self.expression


class Synch(Statement):
    """
    Represents a synchronized statement in the Java AST.

    synchronized (<expression>) <block>
    """

    def __init__(self, expression: Expr = None, block: Block = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for SynchronizedStatement")
        if block is None:
            raise ValueError("block is required for SynchronizedStatement")
        self.expression = expression
        self.block = block

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression
        yield "block", self.block


class CatchClause(_JAST):
    """
    Represents a catch clause in the Java AST.

    catch (<jtype> <id>) <block>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        exceptions: List[qname] = None,
        id: identifier = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not exceptions:
            raise ValueError("exceptions is required for CatchClause")
        if id is None:
            raise ValueError("id is required for CatchClause")
        if body is None:
            raise ValueError("body is required for CatchClause")
        self.modifiers = modifiers or []
        self.exceptions = exceptions
        self.id = id
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "exceptions", self.exceptions
        yield "id", self.id
        yield "body", self.body


class Try(Statement):
    """
    Represents a try statement in the Java AST.

    try <block> [catch (<jtype> <id>) <block>]* [finally <block>]
    """

    def __init__(
        self,
        body: Block = None,
        catches: List[CatchClause] = None,
        final: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if body is None:
            raise ValueError("block is required for TryStatement")
        if not catches and not final:
            raise ValueError("catches or final is required for TryStatement")
        self.body = body
        self.catches = catches or []
        self.final = final

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body
        if self.catches:
            yield "catches", self.catches
        if self.final:
            yield "final", self.final


class Resource(_JAST):
    """
    Represents a resource in the Java AST.

    <modifier>* <jtype> <declarator>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        declarator: "declarator" = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for Resource")
        if declarator is None:
            raise ValueError("declarator is required for Resource")
        self.modifiers = modifiers or []
        self.type = type
        self.declarator = declarator

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "declarator", self.declarator


class TryWithResources(Statement):
    """
    Represents a try-with-resources statement in the Java AST.

    try (<resource>)* <block> [catch (<jtype> <id>) <block>]* [finally <block>]
    """

    def __init__(
        self,
        resources: List[Resource | qname] = None,
        body: Block = None,
        catches: List[CatchClause] = None,
        final: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not resources:
            raise ValueError("resources is required for TryWithResourcesStatement")
        if body is None:
            raise ValueError("body is required for TryWithResourcesStatement")
        self.resources = resources
        self.body = body
        self.catches = catches or []
        self.final = final

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "resources", self.resources
        yield "body", self.body
        if self.catches:
            yield "catches", self.catches
        if self.final:
            yield "final", self.final


class Yield(Statement):
    """
    Represents a yield statement in the Java AST.

    yield <expression>;
    """

    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for YieldStatement")
        self.expression = expression

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


# Declarations


# noinspection PyPep8Naming
class declaration(_JAST, abc.ABC):
    """
    Abstract base class for all declarations in the Java AST.
    """


class EmptyDecl(declaration):
    """
    Represents an empty declaration in the Java AST.

    ;
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Package declaration


class Package(declaration):
    """
    Represents a package declaration in the Java AST.

    package <qname>;
    """

    def __init__(
        self, annotations: List[Annotation] = None, name: qname = None, **kwargs
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for Package")
        self.annotations = annotations or []
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "qname", self.name


# Import Declarations


class Import(declaration):
    """
    Represents an import declaration in the Java AST.

    import <qname>;
    import static <qname>;
    import <qname>.*;
    import static <qname>.*;
    """

    def __init__(
        self,
        static: bool = False,
        name: qname = None,
        on_demand: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for Import")
        self.static = static
        self.name = name
        self.on_demand = on_demand

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name


# Module declaration


class directive(_JAST, abc.ABC):
    """
    Abstract base class for all module directives in the Java AST.
    """


class Requires(directive):
    """
    Represents a requires directive in the Java AST.

    requires <qname>;
    """

    def __init__(
        self,
        modifiers: List[modifier] = None,
        name: qname = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for Requires")
        self.modifiers = modifiers
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "qname", self.name


class Exports(directive):
    """
    Represents an exports directive in the Java AST.

    exports <qname> [to <qname>];
    """

    def __init__(
        self,
        name: qname = None,
        to: qname = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for Exports")
        self.name = name
        self.to = to

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name
        if self.to:
            yield "to", self.to


class Opens(directive):
    """
    Represents an opens directive in the Java AST.

    opens <qname> [to <qname>];
    """

    def __init__(
        self,
        name: qname = None,
        to: qname = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for Opens")
        self.name = name
        self.to = to

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name
        if self.to:
            yield "to", self.to


class UsesDirective(directive):
    """
    Represents an uses directive in the Java AST.

    uses <qname>;
    """

    def __init__(
        self,
        name: qname = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("qname is required for UsesDirective")
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name


class ProvidesDirective(directive):
    """
    Represents a provides directive in the Java AST.

    provides <qname> with <qname>;
    """

    def __init__(
        self,
        name: qname = None,
        with_: qname = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("jtype is required for ProvidesDirective")
        if not with_:
            raise ValueError("with_ is required for ProvidesDirective")
        self.name = name
        self.with_ = with_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name
        yield "with", self.with_


class Module(declaration):
    """
    Represents a module declaration in the Java AST.

    module <qname> { <directive> <directive> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        open: bool = False,
        name: qname = None,
        directives: List[directive] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not name:
            raise ValueError("qname is required for Module")
        self.open = open
        self.name = name
        self.directives = directives or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "open", self.open
        if self.directives:
            yield "directives", self.directives


# Field Declarations


class declarator(_JAST):
    """
    Represents a variable declarator in the Java AST.

    <id> [= <initializer>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        id: VariableDeclaratorId = None,
        initializer: Expr | ArrayInitializer = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id_ is required for declarator")
        self.id = id
        self.initializer = initializer

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        if self.initializer:
            yield "initializer", self.initializer


class Field(declaration):
    """
    Represents a field declaration in the Java AST.

    <modifier>* <jtype> <declarator>, <declarator>, ...;
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        declarators: List[declarator] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for Field")
        if not declarators:
            raise ValueError("declarators is required for Field")
        self.modifiers = modifiers or []
        self.type = type
        self.declarators = declarators

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "declarators", self.declarators


# Method Declarations


class Method(declaration):
    """
    Represents a method declaration in the Java AST.

    <modifier>* <jtype> <id>(<parameter>, <parameter>, ...) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type_params: typeparams = None,
        annotations: List[Annotation] = None,
        return_type: jtype = None,
        id: identifier = None,
        parameters: params = None,
        dims: List[Dim] = None,
        throws: List[qname] = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if return_type is None:
            raise ValueError("return_type is required for Method")
        if id is None:
            raise ValueError("qname is required for Method")
        self.modifiers = modifiers or []
        self.type_params = type_params or []
        self.annotations = annotations or []
        self.return_type = return_type
        self.id = id
        self.parameters = parameters
        self.dims = dims or []
        self.throws = throws or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_params:
            yield "type_params", self.type_params
        if self.annotations:
            yield "annotations", self.annotations
        yield "return_type", self.return_type
        yield "id", self.id
        if self.parameters:
            yield "parameters", self.parameters
        if self.dims:
            yield "dims", self.dims
        if self.throws:
            yield "throws", self.throws
        if self.body:
            yield "body", self.body


# Constructor declaration


class Constructor(declaration):
    """
    Represents a constructor declaration in the Java AST.

    <modifier>* <id>(<parameter>, <parameter>, ...) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type_params: typeparams = None,
        id: identifier = None,
        parameters: params = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("id is required for Constructor")
        self.modifiers = modifiers or []
        self.type_params = type_params or []
        self.id = id
        self.parameters = parameters or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_params:
            yield "type_params", self.type_params
        yield "id", self.id
        if self.parameters:
            yield "parameters", self.parameters
        if self.body:
            yield "body", self.body


# Initializers


class Initializer(declaration):
    """
    Represents an initializer in the Java AST.

    { <statement> <statement> ... }
    static { <statement> <statement> ... }
    """

    def __init__(self, body: Block = None, static: bool = False, **kwargs):
        super().__init__(**kwargs)
        if body is None:
            raise ValueError("body is required for Initializer")
        self.body = body
        self.static = static

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


# Interface


class Interface(declaration):
    """
    Represents an interface declaration in the Java AST.

    <modifier>* interface <qname> { <declaration> <declaration> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        type_params: typeparams = None,
        extends: List[jtype] = None,
        permits: List[jtype] = None,
        body: List[declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("qname is required for Interface")
        self.modifiers = modifiers or []
        self.id = id
        self.type_params = type_params or []
        self.extends = extends or []
        self.permits = permits or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "id", self.id
        if self.type_params:
            yield "type_params", self.type_params
        if self.extends:
            yield "extends", self.extends
        if self.permits:
            yield "permits", self.permits
        if self.body:
            yield "body", self.body


class AnnotationMethod(declaration):
    """
    Represents an annotation method declaration in the Java AST.

    <modifier>* <jtype> <identifier>() [default <element>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        id: identifier = None,
        default: element = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for AnnotationMethod")
        if id is None:
            raise ValueError("qname is required for AnnotationMethod")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id
        self.default = default

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "id", self.id
        if self.default:
            yield "default", self.default


class AnnotationDecl(declaration):
    """
    Represents an annotation declaration in the Java AST.

    <modifier>* @interface <identifier> { <declaration> <declaration> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        extends: List[jtype] = None,
        permits: List[jtype] = None,
        body: List[declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("qname is required for AnnotationInterfaceDeclaration")
        self.modifiers = modifiers or []
        self.name = id
        self.extends = extends or []
        self.permits = permits or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "qname", self.name
        if self.extends:
            yield "extends", self.extends
        if self.permits:
            yield "permits", self.permits
        if self.body:
            yield "body", self.body


# ClassExpr Declarations


class Class(declaration):
    """
    Represents a class declaration in the Java AST.

    <modifier>* class <qname> { <declaration> <declaration> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        type_params: typeparams = None,
        extends: jtype = None,
        implements: List[jtype] = None,
        permits: List[jtype] = None,
        body: List[declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("qname is required for Class")
        self.modifiers = modifiers or []
        self.id = id
        self.type_params = type_params or []
        self.extends = extends
        self.implements = implements or []
        self.permits = permits or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "id", self.id
        if self.type_params:
            yield "type_params", self.type_params
        if self.extends:
            yield "extends", self.extends
        if self.implements:
            yield "implements", self.implements
        if self.permits:
            yield "permits", self.permits
        if self.body:
            yield "body", self.body


class enumconstant(_JAST):
    """
    Represents an enum constant in the Java AST.

    <annotation>* <qname> [(<argument>, <argument>, ...)] [<block>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        arguments: List[Expr] = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("qname is required for enumconstant")
        self.annotations = annotations or []
        self.name = id
        self.arguments = arguments
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "qname", self.name
        if self.arguments:
            yield "arguments", self.arguments
        if self.body:
            yield "body", self.body


class Enum(declaration):
    """
    Represents an enum declaration in the Java AST.

    <modifier>* enum <qname> { <constant>, <constant>, ...[; <declaration> <declaration> ... ]}
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        implements: List[jtype] = None,
        constants: List[enumconstant] = None,
        body: List[declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("qname is required for Enum")
        self.modifiers = modifiers or []
        self.name = id
        self.implements = implements or []
        self.constants = constants or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "qname", self.name
        if self.implements:
            yield "implements", self.implements
        if self.constants:
            yield "constants", self.constants
        if self.body:
            yield "body", self.body


class recordcomponent(_JAST):
    """
    Represents a record component in the Java AST.

    <jtype> <qname>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, id: identifier = None, **kwargs):
        super().__init__(**kwargs)
        if type is None:
            raise ValueError("jtype is required for recordcomponent")
        if id is None:
            raise ValueError("qname is required for recordcomponent")
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        yield "id", self.id


class Record(Class):
    """
    Represents a record declaration in the Java AST.

    <modifier>* record <qname> (<component>, <component>, ...) [implements <jtype>, <jtype>, ...] {
        <declaration> <declaration> ...
    }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        type_params: typeparams = None,
        components: List[recordcomponent] = None,
        implements: List[jtype] = None,
        body: List[declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id is None:
            raise ValueError("qname is required for Record")
        self.modifiers = modifiers or []
        self.name = id
        self.type_params = type_params or []
        self.components = components or []
        self.implements = implements or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "qname", self.name
        if self.type_params:
            yield "type_params", self.type_params
        if self.components:
            yield "components", self.components
        if self.implements:
            yield "implements", self.implements
        if self.body:
            yield "body", self.body


# Compilation Unit


# noinspection PyPep8Naming
class mod(JAST, abc.ABC):
    """
    Abstract base class for all compilation units in the Java AST.
    """


class CompilationUnit(mod):
    """
    Represents an ordinary compilation unit in the Java AST.

    [<package>] [<import> <import> ...] <declaration> <declaration> ...
    """

    def __init__(
        self,
        package: Package = None,
        imports: List[Import] = None,
        declarations: List[declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.package = package
        self.imports = imports or []
        self.declarations = declarations or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.package:
            yield "package", self.package
        if self.imports:
            yield "imports", self.imports
        yield "declarations", self.declarations


class ModularUnit(mod):
    """
    Represents a modular compilation unit in the Java AST.

    [<import> <import> ...] <module>
    """

    def __init__(
        self,
        imports: List[Import] = None,
        module: Module = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not module:
            raise ValueError("module is required for ModularUnit")
        self.imports = imports or []
        self.module = module

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.imports:
            yield "imports", self.imports
        yield "module", self.module
