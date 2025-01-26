"""
This module contains the abstract syntax tree (AST) classes for the Java AST (JAST).
"""

import abc
from typing import List, Any, Iterator, Tuple, Union


class JAST(abc.ABC):
    """
    Abstract base class for all JAST classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Fallback constructor for all JAST classes.
        :param kwargs: keyword args
        """
        pass

    def __hash__(self):
        """
        Hash func for JAST classes.
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
        Copy func for JAST classes.
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
        *args,
        **kwargs,
    ):
        """
        Constructor for all JAST classes that have a location in the source code.

        :param lineno:          The starting line number of the JAST class.
        :param col_offset:      The starting column offset of the JAST class.
        :param end_lineno:      The ending line number of the JAST class.
        :param end_col_offset:  The ending column offset of the JAST class.
        :param kwargs:          keyword args
        """
        super().__init__(*args, **kwargs)
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset


# Identifiers


class identifier(JAST, str):
    """
    Represents an identifier in the Java AST.
    """

    def __init__(self, value: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def __new__(cls, *args, **kwargs):
        return str.__new__(identifier, *args, **kwargs)

    def __copy__(self):
        return identifier(self.value)


# Names


class qname(JAST):
    """
    Represents a qualified qname in the Java AST.

    <identifier>.<identifier>.<identifier>...
    """

    def __init__(self, identifiers: List[identifier] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not identifiers:
            raise ValueError("identifier is required for qname")
        self.identifiers = identifiers

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifiers", self.identifiers


# Literals


class literal(JAST, abc.ABC):
    """
    Abstract base class for all literal values in the Java AST.
    """

    def __init__(self, value: Any, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value


class IntLiteral(literal, int):
    """
    Represents an integer literal in the Java AST.
    """

    def __init__(self, value: int, long: bool = False, *args, **kwargs):
        super().__init__(value, *args, **kwargs)
        self.long = long

    def __new__(cls, value, *args, **kwargs):
        obj = int.__new__(cls, value)
        IntLiteral.__init__(obj, value, *args, **kwargs)
        return obj

    def __copy__(self):
        return IntLiteral(self.value, self.long)


class FloatLiteral(literal, float):
    """
    Represents a float literal in the Java AST.
    """

    def __init__(self, value: float, double: bool = False, *args, **kwargs):
        super().__init__(value, *args, **kwargs)
        self.double = double

    def __new__(cls, value, *args, **kwargs):
        obj = float.__new__(cls, value)
        FloatLiteral.__init__(obj, value, *args, **kwargs)
        return obj

    def __copy__(self):
        return FloatLiteral(self.value, self.double)


# noinspection PyFinal
class BoolLiteral(literal, int):
    """
    Represents a boolean literal in the Java AST.
    """

    def __init__(self, value: bool, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

    def __new__(cls, value, *args, **kwargs):
        obj = int.__new__(cls, value)
        BoolLiteral.__init__(obj, value, **kwargs)
        return obj

    def __copy__(self):
        return BoolLiteral(self.value)


class CharLiteral(literal, str):
    """
    Represents a character literal in the Java AST.
    """

    def __init__(self, value: str, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

    def __new__(cls, value, *args, **kwargs):
        assert len(value) == 1, "CharLiteral must be a single character"
        obj = str.__new__(cls, value)
        CharLiteral.__init__(obj, value, *args, **kwargs)
        return obj

    def __copy__(self):
        return CharLiteral(self.value)


class StringLiteral(literal, str):
    """
    Represents a string literal in the Java AST.
    """

    def __init__(self, value: str, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

    def __new__(cls, value, *args, **kwargs):
        obj = str.__new__(cls, value)
        StringLiteral.__init__(obj, value, *args, **kwargs)
        return obj

    def __copy__(self):
        return StringLiteral(self.value)


class TextBlock(literal, str):
    """
    Represents a text body literal in the Java AST.
    """

    def __init__(self, value: str, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

    def __new__(cls, value, *args, **kwargs):
        obj = str.__new__(cls, value)
        TextBlock.__init__(obj, value, *args, **kwargs)
        return obj

    def __copy__(self):
        return TextBlock(self.value)


class NullLiteral(literal):
    """
    Represents a null literal in the Java AST.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)


# Modifiers


class modifier(JAST, abc.ABC):
    """
    Abstract base class for all modifiers in the Java AST.
    """


class Abstract(modifier):
    """
    Represents the abstract modifier in the Java AST.
    """


class Default(modifier):
    """
    Represents the default modifier in the Java AST.
    """


class Final(modifier):
    """
    Represents the final modifier in the Java AST.
    """


class Native(modifier):
    """
    Represents the native modifier in the Java AST.
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


class Sealed(modifier):
    """
    Represents the sealed modifier in the Java AST.
    """


class NonSealed(modifier):
    """
    Represents the non-sealed modifier in the Java AST.
    """


class Static(modifier):
    """
    Represents the static modifier in the Java AST.
    """


class Strictfp(modifier):
    """
    Represents the strictfp modifier in the Java AST.
    """


class Synchronized(modifier):
    """
    Represents the synchronized modifier in the Java AST.
    """


class Transient(modifier):
    """
    Represents the transient modifier in the Java AST.
    """


class Transitive(modifier):
    """
    Represents the transitive modifier in the Java AST.
    """


class Volatile(modifier):
    """
    Represents the volatile modifier in the Java AST.
    """


class elementvaluepair(JAST):
    """
    Represents an element-value pair in the Java AST.

    <label> = <value>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        id: identifier = None,
        value: Union["elementarrayinit", "Annotation", "expr"] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("id is required for elementvaluepair")
        if value is None:
            raise ValueError("value is required for elementvaluepair")
        self.id = id
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        yield "value", self.value


class elementarrayinit(JAST):
    """
    Represents an element-value array initializer in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(
        self,
        values: List[Union["elementarrayinit", "Annotation", "expr"]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        elements: List[
            Union[elementvaluepair, elementarrayinit, "Annotation", "expr"]
        ] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if name is None:
            raise ValueError("qname is required for Annotation")
        self.name = name
        self.elements = elements

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        if self.elements:
            yield "elements", self.elements


# Types


# noinspection PyShadowingBuiltins
class jtype(JAST, abc.ABC):
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


class primitivetype(jtype, abc.ABC):
    """
    Abstract base class for all primitive types in the Java AST.
    """

    def __init__(self, annotations: List[Annotation] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.annotations = annotations or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations


class Boolean(primitivetype):
    """
    Represents the boolean primitive jtype in the Java AST.
    """


class Byte(primitivetype):
    """
    Represents the byte primitive jtype in the Java AST.
    """


class Short(primitivetype):
    """
    Represents the short primitive jtype in the Java AST.
    """


class Int(primitivetype):
    """
    Represents the int primitive jtype in the Java AST.
    """


class Long(primitivetype):
    """
    Represents the long primitive jtype in the Java AST.
    """


class Char(primitivetype):
    """
    Represents the char primitive jtype in the Java AST.
    """


class Float(primitivetype):
    """
    Represents the float primitive jtype in the Java AST.
    """


class Double(primitivetype):
    """
    Represents the double primitive jtype in the Java AST.
    """


class wildcardbound(JAST):
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for wildcardbound")
        if extends == super_:
            raise ValueError(
                "extends and super_ are mutually exclusive for wildcardbound"
            )
        self.type = type
        self.extends = extends
        self.super_ = super_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type


class Wildcard(jtype):
    """
    Represents a wildcard jtype in the Java AST.

    <annotation>* ? [<bound>]
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        bound: wildcardbound = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.annotations = annotations or []
        self.bound = bound

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        if self.bound:
            yield "bound", self.bound


class typeargs(JAST):
    """
    Represents jtype args in the Java AST.

    < <jtype>, <jtype>, ... >
    """

    def __init__(self, types: List[jtype] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if types is None:
            raise ValueError("types is required for typeargs")
        self.types = types

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class Coit(jtype):
    """
    Represents a simple class or interface jtype in the Java AST.

    <annotation>* <label>[<jtype-args>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        type_args: typeargs = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("id is required")
        self.annotations = annotations or []
        self.id = id
        self.type_args = type_args

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id
        if self.type_args:
            yield "type_args", self.type_args


class ClassType(jtype):
    """
    Represents a class jtype in the Java AST.

    <annotation>* <coit>.<coit>.<coit>...
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        coits: List[Coit] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not coits:
            raise ValueError("coits is required")
        self.annotations = annotations or []
        self.coits = coits

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "coits", self.coits


class dim(JAST):
    """
    Represents a dimension in the Java AST.

    []
    """

    def __init__(self, annotations: List[Annotation] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        dims: List[dim] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required")
        self.annotations = annotations or []
        self.type = type
        self.dims = dims or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "type", self.type
        if self.dims:
            yield "dims", self.dims


class variabledeclaratorid(JAST):
    """
    Represents a variable declarator label in the Java AST.

    <id><dim><dim>...
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, dims: List[dim] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("id is required for variabledeclaratorid")
        self.id = id
        self.dims = dims or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        if self.dims:
            yield "dims", self.dims


# jtype Parameters


class typebound(JAST):
    """
    Represents a jtype bound in the Java AST.

    <annotation>* <jtype> & <jtype> & ...
    """

    def __init__(
        self,
        annotations: List[Annotation] = None,
        types: List[jtype] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not types:
            raise ValueError("types is required for typebound")
        self.annotations = annotations or []
        self.types = types

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class typeparam(JAST):
    """
    Represents a jtype parameter in the Java AST.

    <annotation>* <label> [<bound>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        bound: typebound = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("id is required")
        self.annotations = annotations or []
        self.id = id
        self.bound = bound

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id
        if self.bound:
            yield "bound", self.bound


class typeparams(JAST):
    """
    Represents jtype args in the Java AST.

    < <parameter>, <parameter>, ... >
    """

    def __init__(self, parameters: List[typeparam] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not parameters:
            raise ValueError("parameters is required for typeparams")
        self.parameters = parameters

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "parameters", self.parameters


# pattern


class pattern(JAST):
    """
    Represents a pattern in the Java AST.

    <modifier>* <jtype> <annotation>* <label>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        annotations: List[Annotation] = None,
        id: identifier = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("type is required for pattern")
        if id is None:
            raise ValueError("id is required for pattern")
        self.modifiers = modifiers or []
        self.type = type
        self.annotations = annotations or []
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id


class guardedpattern(JAST):
    """
    Represents a guarded pattern in the Java AST.

    <pattern> && <condition> && <condition> && ...
    """

    def __init__(
        self,
        value: pattern = None,
        conditions: List["expr"] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("pattern is required for guardedpattern")
        self.value = value
        self.conditions = conditions or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value
        if self.conditions:
            yield "conditions", self.conditions


# Operators


class operator(JAST, abc.ABC):
    """
    Abstract base class for all binary operators in the Java AST.
    """


class Or(operator):
    """
    Represents the logical OR operator in the Java AST.

    ||
    """


class And(operator):
    """
    Represents the logical AND operator in the Java AST.

    &&
    """


class BitOr(operator):
    """
    Represents the bitwise OR operator in the Java AST.

    |
    """


class BitXor(operator):
    """
    Represents the bitwise XOR operator in the Java AST.

    ^
    """


class BitAnd(operator):
    """
    Represents the bitwise AND operator in the Java AST.

    &
    """


class Eq(operator):
    """
    Represents the equality operator in the Java AST.

    ==
    """


class NotEq(operator):
    """
    Represents the inequality operator in the Java AST.

    !=
    """


class Lt(operator):
    """
    Represents the less than operator in the Java AST.

    <
    """


class LtE(operator):
    """
    Represents the less than or equal to operator in the Java AST.

    <=
    """


class Gt(operator):
    """
    Represents the greater than operator in the Java AST.

    >
    """


class GtE(operator):
    """
    Represents the greater than or equal to operator in the Java AST.

    >=
    """


class LShift(operator):
    """
    Represents the left shift operator in the Java AST.

    <<
    """


class RShift(operator):
    """
    Represents the right shift operator in the Java AST.

    >>
    """


class URShift(operator):
    """
    Represents the unsigned right shift operator in the Java AST.

    >>>
    """


class Add(operator):
    """
    Represents the addition operator in the Java AST.

    +
    """


class Sub(operator):
    """
    Represents the subtraction operator in the Java AST.

    -
    """


class Mult(operator):
    """
    Represents the multiplication operator in the Java AST.

    *
    """


class Div(operator):
    """
    Represents the division operator in the Java AST.

    /
    """


class Mod(operator):
    """
    Represents the modulo operator in the Java AST.

    %
    """


class unaryop(JAST, abc.ABC):
    """
    Abstract base class for all unary operators in the Java AST.
    """


class PreInc(unaryop):
    """
    Represents the pre-increment operator in the Java AST.

    ++
    """


class PreDec(unaryop):
    """
    Represents the pre-decrement operator in the Java AST.

    --
    """


class UAdd(unaryop):
    """
    Represents the unary plus operator in the Java AST.

    +
    """


class USub(unaryop):
    """
    Represents the unary minus operator in the Java AST.

    -
    """


class Invert(unaryop):
    """
    Represents the bitwise inversion operator in the Java AST.

    ~
    """


class Not(unaryop):
    """
    Represents the logical negation operator in the Java AST.

    !
    """


class postop(JAST, abc.ABC):
    """
    Abstract base class for all post operators in the Java AST.
    """


class PostInc(postop):
    """
    Represents the post-increment operator in the Java AST.
    """


class PostDec(postop):
    """
    Represents the post-decrement operator in the Java AST.
    """


# Expressions


class expr(_JAST, abc.ABC):
    """
    Abstract base class for all expressions in the Java AST.
    """


class Lambda(expr):
    """
    Represents a lambda func in the Java AST.

    <parameter> -> <body>
    (<parameter>, <parameter>, ...) -> <body>
    """

    def __init__(
        self,
        args: identifier | List[identifier] | "params" = None,
        body: Union[expr, "Block"] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if args is None:
            raise ValueError("args is required for Lambda")
        if body is None:
            raise ValueError("body is required for Lambda")
        if isinstance(args, params) and args.receiver_parameter:
            raise ValueError("receiver_param is not allowed for Lambda")
        self.args = args
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "args", self.args
        yield "body", self.body


class Assign(expr):
    """
    Represents an assignment in the Java AST.

    <target> <op> <value>
    """

    def __init__(
        self,
        target: expr = None,
        op: operator = None,
        value: expr = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if target is None:
            raise ValueError("target is required for Assign")
        if value is None:
            raise ValueError("value is required for Assign")
        self.target = target
        self.op = op
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "target", self.target
        if self.op:
            yield "op", self.op
        yield "value", self.value


class IfExp(expr):
    """
    Represents an if value in the Java AST.

    <test> ? <body> : <orelse>
    """

    def __init__(
        self,
        test: expr = None,
        body: expr = None,
        orelse: expr = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class BinOp(expr):
    """
    Represents a binary operation in the Java AST.

    <left> <op> <right>
    """

    def __init__(
        self,
        left: expr = None,
        op: operator = None,
        right: expr = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class InstanceOf(expr):
    """
    Represents an instanceof value in the Java AST.

    <value> instanceof <type>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self, value: expr = None, type: jtype | pattern = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for InstanceOf")
        if type is None:
            raise ValueError("jtype is required for InstanceOf")
        self.value = value
        self.type = type

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value
        yield "type", self.type


class UnaryOp(expr):
    """
    Represents a unary operation in the Java AST.

    <op> <operand>
    """

    def __init__(self, op: unaryop = None, operand: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if op is None:
            raise ValueError("op is required for UnaryOp")
        if operand is None:
            raise ValueError("operand is required for UnaryOp")
        self.op = op
        self.operand = operand

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "op", self.op
        yield "operand", self.operand


class PostOp(expr):
    """
    Represents a post-unary operation in the Java AST.

    <operand> <op>
    """

    def __init__(self, operand: expr = None, op: postop = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if operand is None:
            raise ValueError("operand is required for PostOp")
        if op is None:
            raise ValueError("op is required for PostOp")
        self.operand = operand
        self.op = op

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "operand", self.operand
        yield "op", self.op


class Cast(expr):
    """
    Represents a cast value in the Java AST.

    (<jtype>) <value>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        type: typebound = None,
        value: expr = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for Cast")
        if value is None:
            raise ValueError("value is required for Cast")
        self.annotations = annotations or []
        self.type = type
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "type", self.type
        yield "value", self.value


class NewObject(expr):
    """
    Represents a new object creation in the Java AST.

    new <type>(<arg>, <arg>, ...) [{ <body> }]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type_args: typeargs = None,
        type: jtype = None,
        template_args: typeargs = None,
        args: List[expr] = None,
        body: List["declaration"] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not type:
            raise ValueError("jtype is required for ObjectCreation")
        self.type_args = type_args
        self.type = type
        self.template_args = template_args
        self.args = args or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_args:
            yield "type_args", self.type_args
        yield "type", self.type
        if self.template_args:
            yield "template_args", self.template_args
        if self.args:
            yield "args", self.args
        if self.body:
            yield "body", self.body


class NewArray(expr):
    """
    Represents a new array creation in the Java AST.

    new <jtype><expr_dim><expr_dim>...[<dim><dim>...]
    new <jtype><dim><dim>... [<initializer>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: jtype = None,
        expr_dims: List[expr] = None,
        dims: List[dim] = None,
        initializer: "arrayinit" = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for ArrayCreation")
        if expr_dims and initializer:
            raise ValueError(
                "expr_dims and initializer are mutually exclusive for ArrayCreation"
            )
        self.type = type
        self.expr_dims = expr_dims or []
        self.dims = dims or []
        self.initializer = initializer

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.expr_dims:
            yield "expr_dims", self.expr_dims
        if self.dims:
            yield "dims", self.dims
        if self.initializer:
            yield "initializer", self.initializer


class switchexplabel(JAST, abc.ABC):
    """
    Abstract base class for all switch value labels in the Java AST.
    """


class ExpCase(switchexplabel):
    """
    Represents a case label for switch expressions in the Java AST.
    """


class ExpDefault(switchexplabel):
    """
    Represents a default label for switch expressions in the Java AST.
    """


class switchexprule(JAST):
    """
    Represents a rule in a switch value in the Java AST.
    """

    def __init__(
        self,
        label: switchexplabel = None,
        cases: List[expr | guardedpattern] = None,
        arrow: bool = False,
        body: List["stmt"] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if label is None:
            raise ValueError("label is required for switchexprule")
        if not cases:
            raise ValueError("cases is required for switchexprule")
        if not body:
            raise ValueError("body is required for switchexprule")
        self.label = label
        self.cases = cases
        self.arrow = arrow
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "label", self.label
        yield "cases", self.cases
        yield "body", self.body


class SwitchExp(expr):
    """
    Represents a switch value in the Java AST.
    """

    def __init__(
        self,
        value: expr = None,
        rules: List[switchexprule] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for SwitchExp")
        self.value = value
        self.rules = rules or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value
        if self.rules:
            yield "rules", self.rules


class This(expr):
    # noinspection GrazieInspection
    """
    Represents the this expression in the Java AST.

    this
    """

    def __init__(
        self,
        arguments: List[expr] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.arguments = arguments

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.arguments:
            yield "args", self.arguments


class Super(expr):
    """
    Represents the super value in the Java AST.

    super
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type_args: typeargs = None,
        id: identifier = None,
        args: List[expr] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        self.type_args = type_args
        self.id = id
        self.args = args

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_args:
            yield "type_args", self.type_args
        if self.id:
            yield "label", self.id
        if self.args:
            yield "args", self.args


class Constant(expr):
    """
    Represents a constant value in the Java AST.

    <value>
    """

    def __init__(self, value: literal = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("literal is required for Constant")
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value


class Name(expr):
    """
    Represents a qname value in the Java AST.

    <label>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("label is required for Name")
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id


class ClassExpr(expr):
    """
    Represents a class value in the Java AST.

    <jtype>.class
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for ClassExpr")
        self.type = type

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type


class ExplicitGenericInvocation(expr):
    """
    Represents an explicit generic invocation in the Java AST.
    """

    def __init__(
        self,
        type_args: typeargs = None,
        value: expr = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for ExplicitGenericInvocation")
        self.type_args = type_args
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_args:
            yield "type_args", self.type_args
        yield "value", self.value


class Subscript(expr):
    """
    Represents an array access in the Java AST.

    <value>[<index>]
    """

    def __init__(self, value: expr = None, index: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for Subscript")
        if index is None:
            raise ValueError("index is required for Subscript")
        self.value = value
        self.index = index

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value
        yield "index", self.index


class Member(expr):
    """
    Represents a member access in the Java AST.

    <value>.<member>
    """

    def __init__(self, value: expr = None, member: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for Member")
        if member is None:
            raise ValueError("member is required for Member")
        self.value = value
        self.member = member

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value
        yield "member", self.member


class Call(expr):
    """
    Represents a func call in the Java AST.

    <func>(<argument>, <argument>, ...)
    """

    def __init__(
        self,
        func: expr = None,
        args: List[expr] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if func is None:
            raise ValueError("value is required for Call")
        self.func = func
        self.args = args or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "func", self.func
        if self.args:
            yield "args", self.args


class Reference(expr):
    """
    Represents a method reference in the Java AST.

    <jtype>::<label>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: expr | jtype = None,
        type_args: typeargs = None,
        id: identifier = None,
        new: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("type is required for Reference")
        if new and id:
            raise ValueError("new and label are mutually exclusive for Reference")
        self.type = type
        self.type_args = type_args
        self.id = id
        self.new = new

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.type_args:
            yield "type_args", self.type_args
        if self.id:
            yield "label", self.id


# Arrays


class arrayinit(JAST):
    """
    Represents an array initializer in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(self, values: List[Union[expr, "arrayinit"]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = values or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "values", self.values


# Parameters


class receiver(JAST):
    """
    Represents a receiver parameter in the Java AST.
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: jtype = None,
        identifiers: List[identifier] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for receiver")
        self.type = type
        self.identifiers = identifiers

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        if self.identifiers:
            yield "identifiers", self.identifiers


class param(JAST):
    """
    Represents a parameter in the Java AST.

    <modifier>* <jtype> <label>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        id: variabledeclaratorid = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for param")
        if id is None:
            raise ValueError("label is required for param")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "label", self.id


class arity(JAST):
    """
    Represents a variable arity parameter in the Java AST.
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        annotations: List[Annotation] = None,
        id: variabledeclaratorid = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for arity")
        if id is None:
            raise ValueError("label is required for arity")
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
        yield "label", self.id


class params(JAST):
    """
    Represents formal args in the Java AST.

    (<receiver-parameter>, <parameter>, ...)
    (<parameter>, <parameter>, ...)
    """

    def __init__(
        self,
        receiver_param: receiver = None,
        parameters: List[param | arity] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.receiver_parameter = receiver_param
        self.parameters = parameters or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.receiver_parameter:
            yield "receiver_param", self.receiver_parameter
        if self.parameters:
            yield "args", self.parameters


# Statements


class stmt(_JAST, abc.ABC):
    """
    Abstract base class for all body in the Java AST.
    """


class Empty(stmt):
    """
    Represents an empty statement in the Java AST.

    ;
    """


class Block(stmt):
    """
    Represents a body statement in the Java AST.

    { <statement> <statement> ... }
    """

    def __init__(self, body: List[stmt] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


class Compound(stmt):
    """
    Represents a compound statement in the Java AST.

    <statement> <statement> ...
    """

    def __init__(self, body: List[stmt] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


class LocalClass(stmt):
    """
    Represents a local class decl in the Java AST.

    class { <decl> <decl> ... }
    """

    def __init__(self, decl: "Class" = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if decl is None:
            raise ValueError("decl is required for LocalClass")
        self.declaration = decl

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "decl", self.declaration


class LocalInterface(stmt):
    """
    Represents a local interface decl in the Java AST.

    interface { <decl> <decl> ... }
    """

    def __init__(self, decl: "Interface" = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if decl is None:
            raise ValueError("decl is required for LocalInterface")
        self.declaration = decl

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "decl", self.declaration


class LocalRecord(stmt):
    """
    Represents a local record decl in the Java AST.

    record { <decl> <decl> ... }
    """

    def __init__(self, decl: "Record" = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if decl is None:
            raise ValueError("decl is required for LocalRecord")
        self.declaration = decl

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "decl", self.declaration


class LocalVariable(stmt):
    """
    Represents a local variable decl in the Java AST.

    <modifier>* <jtype> <declarator>, <declarator>, ...;
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        declarators: List["declarator"] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for LocalVariable")
        if not declarators:
            raise ValueError("declarators is required for LocalVariable")
        self.modifiers = modifiers or []
        self.type = type
        self.declarators = declarators

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "declarators", self.declarators


class Labeled(stmt):
    """
    Represents a labeled statement in the Java AST.

    <label>: <statement>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, label: identifier = None, body: stmt = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if label is None:
            raise ValueError("label is required for LabeledStatement")
        if body is None:
            raise ValueError("statement is required for LabeledStatement")
        self.label = label
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "label", self.label
        yield "body", self.body


class Expression(stmt):
    """
    Represents an exc statement in the Java AST.

    <value>;
    """

    def __init__(self, value: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for ExpressionStatement")
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value


class If(stmt):
    """
    Represents an if statement in the Java AST.

    if (<test>) <body> [else <orelse>]
    """

    def __init__(
        self,
        test: expr = None,
        body: stmt = None,
        orelse: stmt = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class Assert(stmt):
    """
    Represents an assert statement in the Java AST.

    assert <test> [ : <msg> ];
    """

    def __init__(self, test: expr = None, msg: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if test is None:
            raise ValueError("condition is required for AssertStatement")
        self.test = test
        self.msg = msg

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        if self.msg:
            yield "msg", self.msg


class switchlabel(JAST, abc.ABC):
    """
    Abstract base class for all switch labels in the Java AST.
    """


class Match(expr):
    """
    Represents a match for switch body in the Java AST.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, id: identifier = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for Match")
        if id is None:
            raise ValueError("id is required for Match")
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        yield "id", self.id


class Case(switchlabel):
    """
    Represents a case label for switch body in the Java AST.

    case <guard>:
    """

    def __init__(self, guard: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not guard:
            raise ValueError("constants is required for Case")
        self.guard = guard

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "guard", self.guard


class DefaultCase(switchlabel):
    """
    Represents a default label for switch body in the Java AST.

    default:
    """


class Throw(stmt):
    """
    Represents a throw statement in the Java AST.

    throw <exc>;
    """

    def __init__(self, exc: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if exc is None:
            raise ValueError("value is required for ThrowStatement")
        self.exc = exc

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "exc", self.exc


class switchgroup(JAST):
    """
    Represents a group of switch labels in the Java AST.

    <label> <label> ... <statement> <statement> ...
    """

    def __init__(
        self,
        labels: List[switchlabel] = None,
        statements: List[stmt] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not labels:
            raise ValueError("labels is required for switchgroup")
        if not statements:
            raise ValueError("body is required for switchgroup")
        self.labels = labels
        self.statements = statements

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "labels", self.labels
        yield "body", self.statements


class switchblock(JAST):
    """
    Represents a body of switch groups and labels in the Java AST.

    [<group> <group> ...] [<label> <label> ...]
    """

    def __init__(
        self,
        groups: List[switchgroup] = None,
        labels: List[switchlabel] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.groups = groups or []
        self.labels = labels or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "groups", self.groups
        yield "labels", self.labels


class Switch(stmt):
    """
    Represents a switch statement in the Java AST.

    switch (<subject>) { <body> }
    """

    def __init__(self, subject: expr = None, body: switchblock = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if subject is None:
            raise ValueError("value is required for SwitchStatement")
        if not body:
            raise ValueError("blocks is required for SwitchStatement")
        self.subject = subject
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "subject", self.subject
        yield "body", self.body


class While(stmt):
    """
    Represents a while statement in the Java AST.

    while (<test>) <body>
    """

    def __init__(self, test: expr = None, body: stmt = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if test is None:
            raise ValueError("test is required for WhileStatement")
        if body is None:
            raise ValueError("statement is required for WhileStatement")
        self.test = test
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body


class DoWhile(stmt):
    """
    Represents a do-while statement in the Java AST.

    do <body> while (<test>)
    """

    def __init__(self, body: stmt = None, test: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if body is None:
            raise ValueError("statement is required for DoWhileStatement")
        if test is None:
            raise ValueError("test is required for DoWhileStatement")
        self.body = body
        self.test = test

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body
        yield "test", self.test


class For(stmt):
    """
    Represents a for statement in the Java AST.

    for (<init>; <test>; <update>) <body>
    """

    def __init__(
        self,
        init: List[expr] | LocalVariable = None,
        test: expr = None,
        update: List[expr] = None,
        body: stmt = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class ForEach(stmt):
    """
    Represents a for-each statement in the Java AST.

    for (<jtype> <id> : <iter>) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        id: variabledeclaratorid = None,
        iter: expr = None,
        body: stmt = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for ForEachStatement")
        if id is None:
            raise ValueError("label is required for ForEachStatement")
        if iter is None:
            raise ValueError("value is required for ForEachStatement")
        if body is None:
            raise ValueError("body is required for ForEachStatement")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id
        self.iter = iter
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "id", self.id
        yield "iter", self.iter
        yield "body", self.body


class Break(stmt):
    """
    Represents a break statement in the Java AST.

    break [<label>];
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, label: identifier = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.label:
            yield "label", self.label


class Continue(stmt):
    """
    Represents a continue statement in the Java AST.

    continue [<label>];
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, label: identifier = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.label:
            yield "label", self.label


class Return(stmt):
    """
    Represents a return statement in the Java AST.

    return [<value>];
    """

    def __init__(self, value: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.value:
            yield "value", self.value


class Synch(stmt):
    """
    Represents a synchronized statement in the Java AST.

    synchronized (<lock>) <body>
    """

    def __init__(self, lock: expr = None, block: Block = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if lock is None:
            raise ValueError("value is required for SynchronizedStatement")
        if block is None:
            raise ValueError("body is required for SynchronizedStatement")
        self.lock = lock
        self.block = block

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "lock", self.lock
        yield "body", self.block


class catch(JAST):
    """
    Represents a catch clause in the Java AST.

    catch (<exc>, <exc>, ... <id>) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        excs: List[qname] = None,
        id: identifier = None,
        body: Block = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not excs:
            raise ValueError("excs is required for catch")
        if id is None:
            raise ValueError("label is required for catch")
        if body is None:
            raise ValueError("body is required for catch")
        self.modifiers = modifiers or []
        self.excs = excs
        self.id = id
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "excs", self.excs
        yield "id", self.id
        yield "body", self.body


class Try(stmt):
    """
    Represents a try statement in the Java AST.

    try <body> [catch (<jtype> <label>) <body>]* [finally <body>]
    """

    def __init__(
        self,
        body: Block = None,
        catches: List[catch] = None,
        final: Block = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if body is None:
            raise ValueError("body is required for TryStatement")
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


class resource(JAST):
    """
    Represents a resource in the Java AST.

    <modifier>* <jtype> <declarator>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        variable: "declarator" = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for resource")
        if declarator is None:
            raise ValueError("declarator is required for resource")
        self.modifiers = modifiers or []
        self.type = type
        self.variable = variable

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "jtype", self.type
        yield "variable", self.variable


class TryWithResources(stmt):
    """
    Represents a try-with-resources statement in the Java AST.

    try (<resource>)* <body> [catch (<jtype> <label>) <body>]* [finally <body>]
    """

    def __init__(
        self,
        resources: List[resource | qname] = None,
        body: Block = None,
        catches: List[catch] = None,
        final: Block = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class Yield(stmt):
    """
    Represents a yield statement in the Java AST.

    yield <value>;
    """

    def __init__(self, value: expr = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if value is None:
            raise ValueError("value is required for YieldStatement")
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value


# Declarations


# noinspection PyPep8Naming
class declaration(_JAST, abc.ABC):
    """
    Abstract base class for all declarations in the Java AST.
    """


class EmptyDecl(declaration):
    """
    Represents an empty decl in the Java AST.

    ;
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Package decl


class Package(declaration):
    """
    Represents a package decl in the Java AST.

    package <qname>;
    """

    def __init__(
        self, annotations: List[Annotation] = None, name: qname = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
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
    Represents an import decl in the Java AST.

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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if name is None:
            raise ValueError("qname is required for Import")
        self.static = static
        self.name = name
        self.on_demand = on_demand

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name


# Module decl


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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if name is None:
            raise ValueError("qname is required for Opens")
        self.name = name
        self.to = to

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name
        if self.to:
            yield "to", self.to


class Uses(directive):
    """
    Represents an uses directive in the Java AST.

    uses <qname>;
    """

    def __init__(
        self,
        name: qname = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if name is None:
            raise ValueError("qname is required for Uses")
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name


class Provides(directive):
    """
    Represents a provides directive in the Java AST.

    provides <qname> with <qname>;
    """

    def __init__(
        self,
        name: qname = None,
        with_: qname = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if name is None:
            raise ValueError("jtype is required for Provides")
        if not with_:
            raise ValueError("with_ is required for Provides")
        self.name = name
        self.with_ = with_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "qname", self.name
        yield "with", self.with_


class Module(declaration):
    """
    Represents a module decl in the Java AST.

    module <qname> { <directive> <directive> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        open: bool = False,
        name: qname = None,
        directives: List[directive] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class declarator(JAST):
    """
    Represents a variable declarator in the Java AST.

    <label> [= <initializer>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        id: variabledeclaratorid = None,
        initializer: expr | arrayinit = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("id_ is required for declarator")
        self.id = id
        self.initializer = initializer

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "label", self.id
        if self.initializer:
            yield "initializer", self.initializer


class Field(declaration):
    """
    Represents a field decl in the Java AST.

    <modifier>* <jtype> <declarator>, <declarator>, ...;
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        declarators: List[declarator] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
    Represents a method decl in the Java AST.

    <modifier>* <jtype> <label>(<parameter>, <parameter>, ...) <body>
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
        dims: List[dim] = None,
        throws: List[qname] = None,
        body: Block = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_params:
            yield "type_params", self.type_params
        if self.annotations:
            yield "annotations", self.annotations
        yield "return_type", self.return_type
        yield "label", self.id
        if self.parameters:
            yield "args", self.parameters
        if self.dims:
            yield "dims", self.dims
        if self.throws:
            yield "throws", self.throws
        if self.body:
            yield "body", self.body


# Constructor decl


class Constructor(declaration):
    """
    Represents a constructor decl in the Java AST.

    <modifier>* <label>(<parameter>, <parameter>, ...) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type_params: typeparams = None,
        id: identifier = None,
        parameters: params = None,
        body: Block = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("label is required for Constructor")
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
        yield "label", self.id
        if self.parameters:
            yield "args", self.parameters
        if self.body:
            yield "body", self.body


# Initializers


class Initializer(declaration):
    """
    Represents an initializer in the Java AST.

    { <statement> <statement> ... }
    static { <statement> <statement> ... }
    """

    def __init__(self, body: Block = None, static: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if body is None:
            raise ValueError("body is required for Initializer")
        self.body = body
        self.static = static

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


# Interface


class Interface(declaration):
    """
    Represents an interface decl in the Java AST.

    <modifier>* interface <qname> { <decl> <decl> ... }
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        yield "label", self.id
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
    Represents an annotation method decl in the Java AST.

    <modifier>* <jtype> <identifier>() [default <element>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type: jtype = None,
        id: identifier = None,
        default: elementarrayinit | Annotation | expr = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        yield "label", self.id
        if self.default:
            yield "default", self.default


class AnnotationDecl(declaration):
    """
    Represents an annotation decl in the Java AST.

    <modifier>* @interface <identifier> { <decl> <decl> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        extends: List[jtype] = None,
        permits: List[jtype] = None,
        body: List[declaration] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
    Represents a class decl in the Java AST.

    <modifier>* class <qname> { <decl> <decl> ... }
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if id is None:
            raise ValueError("qname is required for Class")
        self.modifiers = modifiers or []
        self.id = id
        self.type_params = type_params
        self.extends = extends
        self.implements = implements or []
        self.permits = permits or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "label", self.id
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


class enumconstant(JAST):
    """
    Represents an enum constant in the Java AST.

    <annotation>* <qname> [(<argument>, <argument>, ...)] [<body>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        arguments: List[expr] = None,
        body: Block = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
            yield "args", self.arguments
        if self.body:
            yield "body", self.body


class Enum(declaration):
    """
    Represents an enum decl in the Java AST.

    <modifier>* enum <qname> { <constant>, <constant>, ...[; <decl> <decl> ... ]}
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        id: identifier = None,
        implements: List[jtype] = None,
        constants: List[enumconstant] = None,
        body: List[declaration] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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


class recordcomponent(JAST):
    """
    Represents a record component in the Java AST.

    <jtype> <qname>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, id: identifier = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type is None:
            raise ValueError("jtype is required for recordcomponent")
        if id is None:
            raise ValueError("qname is required for recordcomponent")
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "jtype", self.type
        yield "label", self.id


class Record(Class):
    """
    Represents a record decl in the Java AST.

    <modifier>* record <qname> (<component>, <component>, ...) [implements <jtype>, <jtype>, ...] {
        <decl> <decl> ...
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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

    [<package>] [<import> <import> ...] <decl> <decl> ...
    """

    def __init__(
        self,
        package: Package = None,
        imports: List[Import] = None,
        declarations: List[declaration] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not module:
            raise ValueError("module is required for ModularUnit")
        self.imports = imports or []
        self.module = module

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.imports:
            yield "imports", self.imports
        yield "module", self.module
