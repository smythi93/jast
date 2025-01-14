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
        pass

    def __hash__(self):
        return hash(id(self))

    def __iter__(self) -> Iterator[Tuple[str, "JAST" | List["JAST"]]]:
        return iter([])


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
        super().__init__(**kwargs)
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset


# Identifiers


class Identifier(_JAST):
    """
    Represents an identifier in the Java AST.
    """

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        return f"{self.name!r}"


# Names


class QualifiedName(_JAST):
    """
    Represents a qualified name in the Java AST.

    <identifier>.<identifier>.<identifier>...
    """

    def __init__(self, identifiers: List[Identifier] = None, **kwargs):
        super().__init__(**kwargs)
        if not identifiers:
            raise ValueError("identifier is required for QualifiedName")
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

    def __repr__(self):
        return f"{self.value!r}"


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


class Modifier(_JAST, abc.ABC):
    """
    Abstract base class for all modifiers in the Java AST.
    """


class Transitive(Modifier):
    """
    Represents the transitive modifier in the Java AST.
    """


class Static(Modifier):
    """
    Represents the static modifier in the Java AST.
    """


class Public(Modifier):
    """
    Represents the public modifier in the Java AST.
    """


class Protected(Modifier):
    """
    Represents the protected modifier in the Java AST.
    """


class Private(Modifier):
    """
    Represents the private modifier in the Java AST.
    """


class Abstract(Modifier):
    """
    Represents the abstract modifier in the Java AST.
    """


class Final(Modifier):
    """
    Represents the final modifier in the Java AST.
    """


class Sealed(Modifier):
    """
    Represents the sealed modifier in the Java AST.
    """


class NonSealed(Modifier):
    """
    Represents the non-sealed modifier in the Java AST.
    """


class Strictfp(Modifier):
    """
    Represents the strictfp modifier in the Java AST.
    """


class Transient(Modifier):
    """
    Represents the transient modifier in the Java AST.
    """


class Volatile(Modifier):
    """
    Represents the volatile modifier in the Java AST.
    """


class Synchronized(Modifier):
    """
    Represents the synchronized modifier in the Java AST.
    """


class Native(Modifier):
    """
    Represents the native modifier in the Java AST.
    """


class Default(Modifier):
    """
    Represents the default modifier in the Java AST.
    """


class ElementValuePair(_JAST):
    """
    Represents an element-value pair in the Java AST.

    <identifier> = <value>
    """

    def __init__(
        self, identifier: Identifier = None, value: "ElementValue" = None, **kwargs
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for ElementValuePair")
        if value is None:
            raise ValueError("value is required for ElementValuePair")
        self.identifier = identifier
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
        yield "value", self.value


class ElementValueArrayInitializer(_JAST):
    """
    Represents an element-value array initializer in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(self, values: List["ElementValue"] = None, **kwargs):
        super().__init__(**kwargs)
        self.values = values or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "values", self.values


class Annotation(Modifier):
    """
    Represents an annotation in the Java AST.

    @<name>(<element-value-pairs>)
    """

    def __init__(
        self,
        name: QualifiedName = None,
        elements: List[Union[ElementValuePair, "ElementValue"]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for Annotation")
        self.name = name
        self.elements = elements

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        if self.elements:
            yield "elements", self.elements


"""
Represents a Type for element values in the Java AST.
"""
ElementValue = Union[ElementValueArrayInitializer, Annotation, "Expr"]


# Types


class Type(_JAST, abc.ABC):
    """
    Abstract base class for all types in the Java AST.
    """


class Void(Type):
    """
    Represents the void type in the Java AST.
    """


class Var(Type):
    """
    Represents var for variable types in the Java AST.
    """


class PrimitiveType(Type, abc.ABC):
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
    Represents the boolean primitive type in the Java AST.
    """


class Byte(PrimitiveType):
    """
    Represents the byte primitive type in the Java AST.
    """


class Short(PrimitiveType):
    """
    Represents the short primitive type in the Java AST.
    """


class Int(PrimitiveType):
    """
    Represents the int primitive type in the Java AST.
    """


class Long(PrimitiveType):
    """
    Represents the long primitive type in the Java AST.
    """


class Char(PrimitiveType):
    """
    Represents the char primitive type in the Java AST.
    """


class Float(PrimitiveType):
    """
    Represents the float primitive type in the Java AST.
    """


class Double(PrimitiveType):
    """
    Represents the double primitive type in the Java AST.
    """


class WildcardBound(_JAST):
    """
    Represents a wildcard bound in the Java AST.

    (extends | super) <type>
    """

    def __init__(
        self,
        type_: Type = None,
        extends: bool = False,
        super_: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for WildcardBound")
        if extends == super_:
            raise ValueError(
                "extends and super_ are mutually exclusive for WildcardBound"
            )
        self.type = type_
        self.extends = extends
        self.super = super_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type


class Wildcard(Type):
    """
    Represents a wildcard type in the Java AST.

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
    Represents type arguments in the Java AST.

    < <type>, <type>, ... >
    """

    def __init__(self, types: List[Type] = None, **kwargs):
        super().__init__(**kwargs)
        if types is None:
            raise ValueError("types is required for TypeArguments")
        self.types = types

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class Coit(Type):
    """
    Represents a simple class or interface type in the Java AST.

    <annotation>* <identifier>[<type-arguments>]
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        identifier: Identifier = None,
        type_arguments: TypeArguments = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required")
        self.annotations = annotations or []
        self.identifier = identifier
        self.type_arguments = type_arguments

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier
        if self.type_arguments:
            yield "type_arguments", self.type_arguments


class ClassType(Type):
    """
    Represents a class type in the Java AST.

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


class ArrayType(Type):
    """
    Represents an array type in the Java AST.

    <annotation>* <type>[]
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        type_: Type = None,
        dims: List[Dim] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required")
        self.annotations = annotations or []
        self.type = type_
        self.dims = dims or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "type", self.type
        if self.dims:
            yield "dims", self.dims


class VariableDeclaratorId(_JAST):
    """
    Represents a variable declarator id in the Java AST.

    <identifier><dim><dim>...
    """

    def __init__(self, identifier: Identifier = None, dims: List[Dim] = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for VariableDeclaratorId")
        self.identifier = identifier
        self.dims = dims or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
        if self.dims:
            yield "dims", self.dims


# Type Parameters


class TypeBound(_JAST):
    """
    Represents a type bound in the Java AST.

    <annotation>* <type> & <type> & ...
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        types: List[Type] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not types:
            raise ValueError("types is required for TypeBound")
        self.annotations = annotations or []
        self.types = types

    def __repr__(self):
        return f"TypeBound({self.types!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class TypeParameter(_JAST):
    """
    Represents a type parameter in the Java AST.

    <annotation>* <identifier> [<bound>]
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        identifier: Identifier = None,
        bound: TypeBound = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required")
        self.annotations = annotations or []
        self.identifier = identifier
        self.bound = bound or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier
        if self.bound:
            yield "bound", self.bound


class TypeParameters(_JAST):
    """
    Represents type parameters in the Java AST.

    < <type-parameter>, <type-parameter>, ... >
    """

    def __init__(self, parameters: List[TypeParameter] = None, **kwargs):
        super().__init__(**kwargs)
        if not parameters:
            raise ValueError("parameters is required for TypeParameters")
        self.parameters = parameters

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "parameters", self.parameters


# Pattern


class Pattern(_JAST):
    """
    Represents a pattern in the Java AST.

    <modifier>* <type> <annotation>* <identifier>
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        annotations: List[Annotation] = None,
        identifier: Identifier = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Pattern")
        if identifier is None:
            raise ValueError("identifier is required for Pattern")
        self.modifiers = modifiers or []
        self.type = type_
        self.annotations = annotations or []
        self.identifier = identifier

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier


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
        parameters: Identifier
        | List[Identifier]
        | List[Union["Parameter", "VariableArityParameter"]] = None,
        body: Union[Expr, "Block"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if parameters is None:
            raise ValueError("parameters is required for Lambda")
        if body is None:
            raise ValueError("body is required for Lambda")
        if isinstance(parameters, FormalParameters) and parameters.receiver_parameter:
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

    <expr> instanceof <type>
    """

    def __init__(self, expr: Expr = None, type_: Type | Pattern = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for InstanceOf")
        if type_ is None:
            raise ValueError("type_ is required for InstanceOf")
        self.expr = expr
        self.type = type_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "type", self.type


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

    (<type>) <expr>
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        type_: TypeBound = None,
        expr: Expr = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Cast")
        if expr is None:
            raise ValueError("expr is required for Cast")
        self.annotations = annotations or []
        self.type = type_
        self.expr = expr

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "type", self.type
        yield "expr", self.expr


class NewObject(Expr):
    """
    Represents a new object creation in the Java AST.

    new <type>(<argument>, <argument>, ...) [{ <body> }]
    """

    def __init__(
        self,
        type_arguments: TypeArguments = None,
        type_: Type = None,
        arguments: List[Expr] = None,
        body: List["Declaration"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not type_:
            raise ValueError("type_ is required for ObjectCreation")
        self.type_arguments = type_arguments
        self.type = type_
        self.arguments = arguments or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "type", self.type
        if self.arguments:
            yield "arguments", self.arguments
        if self.body:
            yield "body", self.body


class NewInnerObject(Expr):
    """
    Represents a new inner object creation in the Java AST.

    <expr>.new <type>(<argument>, <argument>, ...) [{ <body> }]
    """

    def __init__(
        self,
        type_arguments: TypeArguments = None,
        identifier: Identifier = None,
        template_arguments: TypeArguments = None,
        arguments: List[Expr] = None,
        body: List["Declaration"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for ObjectCreation")
        self.type_arguments = type_arguments
        self.identifier = identifier
        self.template_arguments = template_arguments
        self.arguments = arguments or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "identifier", self.identifier
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

    new <type><dim_expr><dim_expr>...[<dim><dim>...]
    new <type><dim><dim>... [<initializer>]
    """

    def __init__(
        self,
        type_: Type = None,
        expr_dims: List[DimExpr] = None,
        dims: List[Dim] = None,
        initializer: "ArrayInitializer" = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for ArrayCreation")
        if expr_dims and initializer:
            raise ValueError(
                "expr_dims and initializer are mutually exclusive for ArrayCreation"
            )
        self.type = type_
        self.expr_dims = expr_dims
        self.dims = dims
        self.initializer = initializer

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
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

    def __repr__(self):
        return "SwitchExprRule()"

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

    def __repr__(self):
        return "SwitchExpr()"

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

    def __init__(
        self,
        type_arguments: TypeArguments = None,
        identifier: Identifier = None,
        arguments: List[Expr] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.type_arguments = type_arguments
        self.identifier = identifier
        self.arguments = arguments

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        if self.identifier:
            yield "identifier", self.identifier
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
    Represents a name expression in the Java AST.

    <identifier>
    """

    def __init__(self, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for Name")
        self.identifier = identifier

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier


class Class(Expr):
    """
    Represents a class expression in the Java AST.

    <type>.class
    """

    def __init__(self, type_: Type = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Class")
        self.type = type_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type


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

    <type>::<identifier>
    """

    def __init__(
        self,
        type_: Expr | Type = None,
        type_arguments: TypeArguments = None,
        identifier: Identifier = None,
        new: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Reference")
        if new and Identifier:
            raise ValueError("new and identifier are mutually exclusive for Reference")
        if new == bool(identifier):
            raise ValueError("new and identifier are mutually exclusive for Reference")
        self.type = type_
        self.type_arguments = type_arguments
        self.identifier = identifier
        self.new = new

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        if self.identifier:
            yield "identifier", self.identifier


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


class ReceiverParameter(_JAST):
    """
    Represents a receiver parameter in the Java AST.
    """

    def __init__(
        self,
        type_: Type = None,
        identifiers: List[Identifier] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for ReceiverParameter")
        self.type = type_
        self.identifiers = identifiers

    def __repr__(self):
        return f"ReceiverParameter({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.identifiers:
            yield "identifier", self.identifiers


class Parameter(_JAST):
    """
    Represents a parameter in the Java AST.

    <modifier>* <type> <identifier>
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        identifier: VariableDeclaratorId = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Parameter")
        if identifier is None:
            raise ValueError("identifier is required for Parameter")
        self.modifiers = modifiers or []
        self.type = type_
        self.identifier = identifier

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "identifier", self.identifier


class VariableArityParameter(_JAST):
    """
    Represents a variable arity parameter in the Java AST.
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        annotations: List[Annotation] = None,
        identifier: VariableDeclaratorId = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for VariableArityParameter")
        if identifier is None:
            raise ValueError("identifier is required for VariableArityParameter")
        self.modifiers = modifiers or []
        self.type = type_
        self.annotations = annotations or []
        self.identifier = identifier

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier


class FormalParameters(_JAST):
    """
    Represents formal parameters in the Java AST.

    (<receiver-parameter>, <parameter>, ...)
    (<parameter>, <parameter>, ...)
    """

    def __init__(
        self,
        receiver_parameter: ReceiverParameter = None,
        parameters: List[Parameter | VariableArityParameter] = None,
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

    def __init__(self, declaration: "ClassDeclaration" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalClassDeclaration")
        self.declaration = declaration

    def __repr__(self):
        return "LocalClassDeclaration()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalInterfaceDeclaration(Statement):
    """
    Represents a local interface declaration in the Java AST.

    interface { <declaration> <declaration> ... }
    """

    def __init__(self, declaration: "InterfaceDeclaration" = None, **kwargs):
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

    def __init__(self, declaration: "RecordDeclaration" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalRecordDeclaration")
        self.declaration = declaration

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalVariableDeclaration(Statement):
    """
    Represents a local variable declaration in the Java AST.

    <modifier>* <type> <declarator>, <declarator>, ...;
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        declarators: List["VariableDeclarator"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for LocalVariableDeclaration")
        if not declarators:
            raise ValueError("declarators is required for LocalVariableDeclaration")
        self.modifiers = modifiers or []
        self.type = type_
        self.declarators = declarators

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
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

    <identifier>: <statement>
    """

    def __init__(self, identifier: Identifier = None, body: Statement = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for LabeledStatement")
        if body is None:
            raise ValueError("statement is required for LabeledStatement")
        self.identifier = identifier
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
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

    def __init__(self, type_: Type = None, ident: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Match")
        if ident is None:
            raise ValueError("ident is required for Match")
        self.type = type_
        self.ident = ident

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        yield "ident", self.ident


class Case(SwitchLabel):
    """
    Represents a case label for switch statements in the Java AST.
    """

    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if not expression:
            raise ValueError("constants is required for Case")
        self.expression = expression

    def __repr__(self):
        return "Case()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


class DefaultCase(SwitchLabel):
    """
    Represents a default label for switch statements in the Java AST.
    """

    def __repr__(self):
        return "DefaultCase()"


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

    def __repr__(self):
        return f"ThrowStatement({self.expression!r})"

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

    def __repr__(self):
        return "WhileStatement()"

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

    def __repr__(self):
        return "DoWhileStatement()"

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

    for (<type> <identifier> : <expression>) <body>
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        identifier: VariableDeclaratorId = None,
        expression: Expr = None,
        body: Statement = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for ForEachStatement")
        if identifier is None:
            raise ValueError("identifier is required for ForEachStatement")
        if expression is None:
            raise ValueError("expression is required for ForEachStatement")
        if body is None:
            raise ValueError("body is required for ForEachStatement")
        self.modifiers = modifiers or []
        self.type = type_
        self.identifier = identifier
        self.expression = expression
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "identifier", self.identifier
        yield "expression", self.expression
        yield "body", self.body


class Break(Statement):
    """
    Represents a break statement in the Java AST.

    break [<identifier>];
    """

    def __init__(self, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        self.identifier = identifier

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.identifier:
            yield "identifier", self.identifier


class Continue(Statement):
    """
    Represents a continue statement in the Java AST.

    continue [<identifier>];
    """

    def __init__(self, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        self.identifier = identifier

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.identifier:
            yield "identifier", self.identifier


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

    catch (<type> <identifier>) <block>
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        exceptions: List[QualifiedName] = None,
        identifier: Identifier = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not exceptions:
            raise ValueError("exceptions is required for CatchClause")
        if identifier is None:
            raise ValueError("identifier is required for CatchClause")
        if body is None:
            raise ValueError("body is required for CatchClause")
        self.modifiers = modifiers or []
        self.exceptions = exceptions
        self.identifier = identifier
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "exceptions", self.exceptions
        yield "identifier", self.identifier
        yield "body", self.body


class Try(Statement):
    """
    Represents a try statement in the Java AST.

    try <block> [catch (<type> <identifier>) <block>]* [finally <block>]
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

    <modifier>* <type> <declarator>
    """

    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        declarator: "VariableDeclarator" = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Resource")
        if declarator is None:
            raise ValueError("declarator is required for Resource")
        self.modifiers = modifiers or []
        self.type = type_
        self.declarator = declarator

    def __repr__(self):
        return "Resource()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "declarator", self.declarator


class TryWithResources(Statement):
    """
    Represents a try-with-resources statement in the Java AST.

    try (<resource>)* <block> [catch (<type> <identifier>) <block>]* [finally <block>]
    """

    def __init__(
        self,
        resources: List[Resource | QualifiedName] = None,
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


class Declaration(_JAST, abc.ABC):
    """
    Abstract base class for all declarations in the Java AST.
    """


# Package Declaration


class PackageDeclaration(Declaration):
    def __init__(
        self, annotations: List[Annotation] = None, name: QualifiedName = None, **kwargs
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for PackageDeclaration")
        self.annotations = annotations or []
        self.name = name

    def __repr__(self):
        return f"PackageDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "name", self.name


# Import Declarations


class ImportDeclaration(Declaration):
    def __init__(
        self,
        name: QualifiedName = None,
        static: bool = False,
        on_demand: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for ImportDeclaration")
        self.name = name
        self.static = static
        self.on_demand = on_demand

    def __repr__(self):
        return f"ImportDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name


# Top Level Declarations


class EmptyDeclaration(Declaration):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "EmptyDeclaration()"


# Module Declaration


class ModuleDirective(_JAST, abc.ABC):
    pass


class RequiresDirective(ModuleDirective):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        name: QualifiedName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for RequiresDirective")
        self.modifiers = modifiers
        self.name = name

    def __repr__(self):
        return f"RequiresDirective({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "name", self.name


class ExportsDirective(ModuleDirective):
    def __init__(
        self,
        name: QualifiedName = None,
        to: QualifiedName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for ExportsDirective")
        self.name = name
        self.to = to

    def __repr__(self):
        return f"ExportsDirective({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        if self.to:
            yield "to", self.to


class OpensDirective(ModuleDirective):
    def __init__(
        self,
        name: QualifiedName = None,
        to: QualifiedName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for OpensDirective")
        self.name = name
        self.to = to

    def __repr__(self):
        return f"OpensDirective({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        if self.to:
            yield "to", self.to


class UsesDirective(ModuleDirective):
    def __init__(
        self,
        name: QualifiedName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("type_ is required for UsesDirective")
        self.name = name

    def __repr__(self):
        return f"UsesDirective({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name


class ProvidesDirective(ModuleDirective):
    def __init__(
        self,
        name: QualifiedName = None,
        with_: QualifiedName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("type_ is required for ProvidesDirective")
        if not with_:
            raise ValueError("with_ is required for ProvidesDirective")
        self.name = name
        self.with_ = with_

    def __repr__(self):
        return f"ProvidesDirective({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        yield "with", self.with_


class ModuleDeclaration(Declaration):
    def __init__(
        self,
        open_: bool = None,
        name: List[QualifiedName] = None,
        directives: List[ModuleDirective] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not name:
            raise ValueError("identifiers is required for ModuleDeclaration")
        self.open_ = open_
        self.name = name
        self.directives = directives or []

    def __repr__(self):
        return "ModuleDeclaration()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "open_", self.open_
        if self.directives:
            yield "directives", self.directives


# Field Declarations


class VariableDeclarator(_JAST):
    def __init__(
        self,
        id_: VariableDeclaratorId = None,
        initializer: Expr | ArrayInitializer = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id_ is None:
            raise ValueError("id_ is required for VariableDeclarator")
        self.id = id_
        self.initializer = initializer

    def __repr__(self):
        return f"VariableDeclarator({self.id!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        if self.initializer:
            yield "initializer", self.initializer


class FieldDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        declarators: List[VariableDeclarator] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for FieldDeclaration")
        if not declarators:
            raise ValueError("declarators is required for FieldDeclaration")
        if hasattr(type_, "annotations") and type_.annotations:
            raise ValueError(
                "annotations are not allowed for type in VariableRecordComponent"
            )
        self.modifiers = modifiers or []
        self.type = type_
        self.declarators = declarators

    def __repr__(self):
        return f"FieldDeclaration({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "declarators", self.declarators


# Method Declarations


class MethodDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_parameters: TypeParameters = None,
        return_type: Type = None,
        identifier: Identifier = None,
        parameters: FormalParameters = None,
        dims: List[Dim] = None,
        throws: List[QualifiedName] = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if return_type is None:
            raise ValueError("return_type is required for MethodDeclaration")
        if identifier is None:
            raise ValueError("name is required for MethodDeclaration")
        self.modifiers = modifiers or []
        self.type_parameters = type_parameters or []
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.dims = dims or []
        self.throws = throws or []
        self.body = body or []

    def __repr__(self):
        return f"MethodDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        yield "return_type", self.return_type
        yield "identifier", self.identifier
        if self.parameters:
            yield "parameters", self.parameters
        if self.dims:
            yield "dims", self.dims
        if self.throws:
            yield "throws", self.throws
        if self.body:
            yield "body", self.body


class InterfaceMethodDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_parameters: TypeParameters = None,
        annotations: List[Annotation] = None,
        return_type: Type = None,
        identifier: Identifier = None,
        parameters: FormalParameters = None,
        dims: List[Dim] = None,
        throws: List[QualifiedName] = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if return_type is None:
            raise ValueError("type_ is required for InterfaceMethodDeclaration")
        if identifier is None:
            raise ValueError("name is required for InterfaceMethodDeclaration")
        self.modifiers = modifiers or []
        self.type_parameters = type_parameters
        self.annotations = annotations or []
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.dims = dims or []
        self.throws = throws or []
        self.body = body or []

    def __repr__(self):
        return f"InterfaceMethodDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        if self.annotations:
            yield "annotations", self.annotations
        yield "return_type", self.return_type
        yield "name", self.identifier
        if self.parameters:
            yield "parameters", self.parameters
        if self.dims:
            yield "dims", self.dims
        if self.throws:
            yield "throws", self.throws
        if self.body:
            yield "body", self.body


# Initializers


class Initializer(Declaration):
    def __init__(self, body: Block = None, **kwargs):
        super().__init__(**kwargs)
        if body is None:
            raise ValueError("body is required for Initializer")
        self.body = body

    def __repr__(self):
        return "Initializer()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


class StaticInitializer(Declaration):
    def __init__(self, body: Block = None, **kwargs):
        super().__init__(**kwargs)
        if not body:
            raise ValueError("body is required for StaticInitializer")
        self.body = body

    def __repr__(self):
        return "StaticInitializer()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


# Constructor Declaration


class ConstructorDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_parameters: TypeParameters = None,
        identifier: Identifier = None,
        parameters: FormalParameters = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for ConstructorDeclaration")
        self.modifiers = modifiers or []
        self.type_parameters = type_parameters or []
        self.identifier = identifier
        self.parameters = parameters or []
        self.body = body

    def __repr__(self):
        return f"ConstructorDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        yield "identifier", self.identifier
        if self.parameters:
            yield "parameters", self.parameters
        if self.body:
            yield "body", self.body


class CompactConstructorDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for CompactConstructorDeclaration")
        self.modifiers = modifiers or []
        self.identifier = identifier
        self.body = body

    def __repr__(self):
        return f"CompactConstructorDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "identifier", self.identifier
        if self.body:
            yield "body", self.body


# Constant Declarations


class ConstantDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        declarators: List[VariableDeclarator] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for ConstantDeclaration")
        if not declarators:
            raise ValueError("declarators is required for ConstantDeclaration")
        self.modifiers = modifiers or []
        self.type = type_
        self.declarators = declarators

    def __repr__(self):
        return f"ConstantDeclaration({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "declarators", self.declarators


# InterfaceDeclaration


class InterfaceDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        type_parameters: TypeParameters = None,
        extends: List[Type] = None,
        permits: List[Type] = None,
        body: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for NormalInterfaceDeclaration")
        self.modifiers = modifiers or []
        self.identifier = identifier
        self.type_parameters = type_parameters or []
        self.extends = extends or []
        self.permits = permits or []
        self.body = body or []

    def __repr__(self):
        return f"NormalInterfaceDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "identifier", self.identifier
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        if self.extends:
            yield "extends", self.extends
        if self.permits:
            yield "permits", self.permits
        if self.body:
            yield "body", self.body


class AnnotationMethodDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        identifier: Identifier = None,
        default: ElementValue = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for AnnotationMethodDeclaration")
        if identifier is None:
            raise ValueError("name is required for AnnotationMethodDeclaration")
        if hasattr(type_, "annotations") and type_.annotations:
            raise ValueError(
                "annotations are not allowed for type in AnnotationMethodDeclaration"
            )
        self.modifiers = modifiers or []
        self.type = type_
        self.identifier = identifier
        self.default = default

    def __repr__(self):
        return f"AnnotationMethodDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "identifier", self.identifier
        if self.default:
            yield "default", self.default


class AnnotationConstantDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_: Type = None,
        declarators: List[VariableDeclarator] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for AnnotationConstantDeclaration")
        if not declarators:
            raise ValueError(
                "declarators is required for AnnotationConstantDeclaration"
            )
        self.modifiers = modifiers or []
        self.type = type_
        self.declarators = declarators

    def __repr__(self):
        return "AnnotationConstantDeclaration()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "declarators", self.declarators


class AnnotationDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        extends: List[Type] = None,
        permits: List[Type] = None,
        body: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for AnnotationInterfaceDeclaration")
        self.modifiers = modifiers or []
        self.name = identifier
        self.extends = extends or []
        self.permits = permits or []
        self.body = body or []

    def __repr__(self):
        return f"AnnotationInterfaceDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "name", self.name
        if self.extends:
            yield "extends", self.extends
        if self.permits:
            yield "permits", self.permits
        if self.body:
            yield "body", self.body


# Class Declarations


class ClassDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        type_parameters: TypeParameters = None,
        extends: Type = None,
        implements: List[Type] = None,
        permits: List[Type] = None,
        body: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for ClassDeclaration")
        self.modifiers = modifiers or []
        self.identifier = identifier
        self.type_parameters = type_parameters or []
        self.extends = extends
        self.implements = implements or []
        self.permits = permits or []
        self.body = body or []

    def __repr__(self):
        return f"ClassDeclaration({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "identifier", self.identifier
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        if self.extends:
            yield "extends", self.extends
        if self.implements:
            yield "implements", self.implements
        if self.permits:
            yield "permits", self.permits
        if self.body:
            yield "body", self.body


class EnumConstant(_JAST):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        identifier: Identifier = None,
        arguments: List[Expr] = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for EnumConstant")
        self.annotations = annotations or []
        self.name = identifier
        self.arguments = arguments
        self.body = body

    def __repr__(self):
        return f"EnumConstant({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "name", self.name
        if self.arguments:
            yield "arguments", self.arguments
        if self.body:
            yield "body", self.body


class EnumDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        implements: List[Type] = None,
        constants: List[EnumConstant] = None,
        body: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for EnumDeclaration")
        self.modifiers = modifiers or []
        self.name = identifier
        self.implements = implements or []
        self.constants = constants or []
        self.body = body or []

    def __repr__(self):
        return f"EnumDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "name", self.name
        if self.implements:
            yield "implements", self.implements
        if self.constants:
            yield "constants", self.constants
        if self.body:
            yield "body", self.body


class RecordComponent(_JAST):
    def __init__(self, type_: Type = None, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for RecordComponent")
        if identifier is None:
            raise ValueError("name is required for RecordComponent")
        self.type = type_
        self.identifier = identifier

    def __repr__(self):
        return f"RecordComponent({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        yield "identifier", self.identifier


class RecordDeclaration(ClassDeclaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        type_parameters: TypeParameters = None,
        components: List[RecordComponent] = None,
        implements: List[ClassType] = None,
        body: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for RecordDeclaration")
        self.modifiers = modifiers or []
        self.name = identifier
        self.type_parameters = type_parameters or []
        self.components = components or []
        self.implements = implements or []
        self.body = body or []

    def __repr__(self):
        return f"RecordDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "name", self.name
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        if self.components:
            yield "components", self.components
        if self.implements:
            yield "implements", self.implements
        if self.body:
            yield "body", self.body


# Compilation Unit


class CompilationUnit(JAST, abc.ABC):
    pass


class OrdinaryCompilationUnit(CompilationUnit):
    def __init__(
        self,
        package: PackageDeclaration = None,
        imports: List[ImportDeclaration] = None,
        declarations: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.package = package
        self.imports = imports or []
        self.declarations = declarations or []

    def __repr__(self):
        return "OrdinaryCompilationUnit()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.package:
            yield "package", self.package
        if self.imports:
            yield "imports", self.imports
        yield "declarations", self.declarations


class ModularCompilationUnit(CompilationUnit):
    def __init__(
        self,
        imports: List[ImportDeclaration] = None,
        module: ModuleDeclaration = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not module:
            raise ValueError("module is required for ModularCompilationUnit")
        self.imports = imports or []
        self.module = module

    def __repr__(self):
        return "ModularCompilationUnit()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.imports:
            yield "imports", self.imports
        yield "module", self.module
