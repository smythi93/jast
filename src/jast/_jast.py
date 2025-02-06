"""
This body contains the abstract syntax tree (AST) classes for the Java AST (JAST).
"""

import abc
from typing import List, Any, Iterator, Tuple, Union


class JASTError(ValueError):
    pass


class JAST(abc.ABC):
    """
    Abstract base class for all JAST classes.
    """

    def __init__(self, *vargs, **kwargs):
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
        for field, value in self:
            if isinstance(value, list):
                setattr(obj, field, getattr(self, field)[:])
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
        *vargs,
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
        super().__init__(*vargs, **kwargs)
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset


# Identifiers


class identifier(JAST, str):
    """
    Represents an identifier in the Java AST.
    """

    def __init__(self, value: str, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.value = value

    def __new__(cls, *vargs, **kwargs):
        return str.__new__(identifier, *vargs, **kwargs)

    def __copy__(self):
        return identifier(self.value)


# Names


class qname(JAST):
    """
    Represents a qualified qname in the Java AST.

    <identifier>.<identifier>.<identifier>...
    """

    def __init__(self, identifiers: List[identifier] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if not identifiers:
            raise JASTError("identifier is required for qname")
        self.identifiers = identifiers

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifiers", self.identifiers


# Literals


class literal(JAST, abc.ABC):
    """
    Abstract base class for all literal values in the Java AST.
    """

    def __init__(self, value: Any, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.value = value


class IntLiteral(literal, int):
    """
    Represents an integer literal in the Java AST.
    """

    def __init__(self, value: int, long: bool = False, *vargs, **kwargs):
        super().__init__(value, *vargs, **kwargs)
        self.long = long

    def __new__(cls, value, *vargs, **kwargs):
        obj = int.__new__(cls, value)
        IntLiteral.__init__(obj, value, *vargs, **kwargs)
        return obj

    def __copy__(self):
        return IntLiteral(self.value, self.long)


class FloatLiteral(literal, float):
    """
    Represents a float literal in the Java AST.
    """

    def __init__(self, value: float, double: bool = False, *vargs, **kwargs):
        super().__init__(value, *vargs, **kwargs)
        self.double = double

    def __new__(cls, value, *vargs, **kwargs):
        obj = float.__new__(cls, value)
        FloatLiteral.__init__(obj, value, *vargs, **kwargs)
        return obj

    def __copy__(self):
        return FloatLiteral(self.value, self.double)


# noinspection PyFinal
class BoolLiteral(literal, int):
    """
    Represents a boolean literal in the Java AST.
    """

    def __init__(self, value: bool, *vargs, **kwargs):
        super().__init__(value, *vargs, **kwargs)

    def __new__(cls, value, *vargs, **kwargs):
        obj = int.__new__(cls, value)
        BoolLiteral.__init__(obj, value, **kwargs)
        return obj

    def __copy__(self):
        return BoolLiteral(self.value)


class CharLiteral(literal, str):
    """
    Represents a character literal in the Java AST.
    """

    def __init__(self, value: str, *vargs, **kwargs):
        super().__init__(value, *vargs, **kwargs)

    def __new__(cls, value, *vargs, **kwargs):
        assert len(value) == 1, "CharLiteral must be a single character"
        obj = str.__new__(cls, value)
        CharLiteral.__init__(obj, value, *vargs, **kwargs)
        return obj

    def __copy__(self):
        return CharLiteral(self.value)


class StringLiteral(literal, str):
    """
    Represents a string literal in the Java AST.
    """

    def __init__(self, value: str, *vargs, **kwargs):
        super().__init__(value, *vargs, **kwargs)

    def __new__(cls, value, *vargs, **kwargs):
        obj = str.__new__(cls, value)
        StringLiteral.__init__(obj, value, *vargs, **kwargs)
        return obj

    def __copy__(self):
        return StringLiteral(self.value)


class TextBlock(literal):
    """
    Represents a text body literal in the Java AST.
    """

    def __init__(self, value: str, *vargs, **kwargs):
        super().__init__(value, *vargs, **kwargs)

    def __copy__(self):
        return TextBlock(self.value[:])


class NullLiteral(literal):
    """
    Represents a null literal in the Java AST.
    """

    def __init__(self, *vargs, **kwargs):
        super().__init__(None, *vargs, **kwargs)


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required for elementvaluepair")
        if value is None:
            raise JASTError("value is required for elementvaluepair")
        self.id = id
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        yield "value", self.value


class elementarrayinit(JAST):
    """
    Represents an element-value array init in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(
        self,
        values: List[Union["elementarrayinit", "Annotation", "expr"]] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Annotation")
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

    def __init__(self, annotations: List[Annotation] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("jtype is required for wildcardbound")
        if extends == super_:
            raise JASTError(
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
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

    def __init__(self, types: List[jtype] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if types is None:
            raise JASTError("types is required for typeargs")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not coits:
            raise JASTError("coits is required")
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

    def __init__(self, annotations: List[Annotation] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("jtype is required")
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
    def __init__(self, id: identifier = None, dims: List[dim] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required for variabledeclaratorid")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not types:
            raise JASTError("types is required for typebound")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required")
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

    def __init__(self, parameters: List[typeparam] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if not parameters:
            raise JASTError("parameters is required for typeparams")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for pattern")
        if id is None:
            raise JASTError("id is required for pattern")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("pattern is required for guardedpattern")
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
            raise JASTError("args is required for Lambda")
        if body is None:
            raise JASTError("body is required for Lambda")
        if isinstance(args, params) and args.receiver_param:
            raise JASTError("receiver_param is not allowed for Lambda")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if target is None:
            raise JASTError("target is required for Assign")
        if value is None:
            raise JASTError("value is required for Assign")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if test is None:
            raise JASTError("test is required for IfExp")
        if body is None:
            raise JASTError("body is required for IfExp")
        if orelse is None:
            raise JASTError("orelse is required for IfExp")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if left is None:
            raise JASTError("left is required for BinOp")
        if op is None:
            raise JASTError("op is required for BinOp")
        if right is None:
            raise JASTError("right is required for BinOp")
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
        self, value: expr = None, type: jtype | pattern = None, *vargs, **kwargs
    ):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for InstanceOf")
        if type is None:
            raise JASTError("jtype is required for InstanceOf")
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

    def __init__(self, op: unaryop = None, operand: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if op is None:
            raise JASTError("op is required for UnaryOp")
        if operand is None:
            raise JASTError("operand is required for UnaryOp")
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

    def __init__(self, operand: expr = None, op: postop = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if operand is None:
            raise JASTError("operand is required for PostOp")
        if op is None:
            raise JASTError("op is required for PostOp")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("jtype is required for Cast")
        if value is None:
            raise JASTError("value is required for Cast")
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
        args: List[expr] = None,
        body: List["declaration"] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not type:
            raise JASTError("type is required for ObjectCreation")
        self.type_args = type_args
        self.type = type
        self.args = args or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_args:
            yield "type_args", self.type_args
        yield "type", self.type
        if self.args:
            yield "args", self.args
        if self.body:
            yield "body", self.body


class NewArray(expr):
    """
    Represents a new array creation in the Java AST.

    new <jtype><expr_dim><expr_dim>...[<dim><dim>...]
    new <jtype><dim><dim>... [<init>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        type: jtype = None,
        expr_dims: List[expr] = None,
        dims: List[dim] = None,
        init: "arrayinit" = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("jtype is required for ArrayCreation")
        if expr_dims and init:
            raise JASTError(
                "expr_dims and init are mutually exclusive for ArrayCreation"
            )
        self.type = type
        self.expr_dims = expr_dims or []
        self.dims = dims or []
        self.init = init

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.expr_dims:
            yield "expr_dims", self.expr_dims
        if self.dims:
            yield "dims", self.dims
        if self.init:
            yield "init", self.init


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if label is None:
            raise JASTError("label is required for switchexprule")
        if not cases and isinstance(label, ExpCase):
            raise JASTError("cases is required for switchexprule with case")
        elif cases and isinstance(label, ExpDefault):
            raise JASTError("cases is not allowed for switchexprule with default")
        self.label = label
        self.cases = cases
        self.arrow = arrow
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "label", self.label
        if self.cases:
            yield "cases", self.cases
        if self.body:
            yield "body", self.body


class SwitchExp(expr):
    """
    Represents a switch value in the Java AST.
    """

    def __init__(
        self,
        value: expr = None,
        rules: List[switchexprule] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for SwitchExp")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        self.type_args = type_args
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_args:
            yield "type_args", self.type_args
        if self.id:
            yield "id", self.id


class Constant(expr):
    """
    Represents a constant value in the Java AST.

    <value>
    """

    def __init__(self, value: literal = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("literal is required for Constant")
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value


class Name(expr):
    """
    Represents a qname value in the Java AST.

    <label>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, id: identifier = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("label is required for Name")
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id


class ClassExpr(expr):
    """
    Represents a class value in the Java AST.

    <jtype>.class
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for ClassExpr")
        self.type = type

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type


class ExplicitGenericInvocation(expr):
    """
    Represents an explicit generic invocation in the Java AST.
    """

    def __init__(
        self,
        type_args: typeargs = None,
        value: expr = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type_args is None:
            raise JASTError("type_args is required for ExplicitGenericInvocation")
        if value is None:
            raise JASTError("value is required for ExplicitGenericInvocation")
        self.type_args = type_args
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type_args", self.type_args
        yield "value", self.value


class Subscript(expr):
    """
    Represents an array access in the Java AST.

    <value>[<index>]
    """

    def __init__(self, value: expr = None, index: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for Subscript")
        if index is None:
            raise JASTError("index is required for Subscript")
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

    def __init__(self, value: expr = None, member: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for Member")
        if member is None:
            raise JASTError("member is required for Member")
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
            raise JASTError("value is required for Call")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for Reference")
        if new and id:
            raise JASTError("new and id are mutually exclusive for Reference")
        elif not new and not id:
            raise JASTError("new or id is required for Reference")
        self.type = type
        self.type_args = type_args
        self.id = id
        self.new = new

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.type_args:
            yield "type_args", self.type_args
        if self.id:
            yield "id", self.id


# Arrays


class arrayinit(JAST):
    """
    Represents an array init in the Java AST.

    { <value>, <value>, ... }
    """

    def __init__(self, values: List[Union[expr, "arrayinit"]] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for receiver")
        self.type = type
        self.identifiers = identifiers

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for param")
        if id is None:
            raise JASTError("label is required for param")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "id", self.id


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for arity")
        if id is None:
            raise JASTError("label is required for arity")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        self.receiver_param = receiver_param
        self.parameters = parameters or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.receiver_param:
            yield "receiver_param", self.receiver_param
        if self.parameters:
            yield "parameters", self.parameters


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

    def __init__(self, body: List[stmt] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


class Compound(stmt):
    """
    Represents a compound statement in the Java AST.

    <statement> <statement> ...
    """

    def __init__(self, body: List[stmt] = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body


class LocalType(stmt):
    """
    Represents a local type (class, interface, or record) decl in the Java AST.

    <decl>
    """

    def __init__(
        self, decl: Union["Class", "Interface", "Record"] = None, *vargs, **kwargs
    ):
        super().__init__(*vargs, **kwargs)
        if decl is None:
            raise JASTError("decl is required for LocalType")
        self.decl = decl

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "decl", self.decl


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for LocalVariable")
        if not declarators:
            raise JASTError("declarators is required for LocalVariable")
        self.modifiers = modifiers or []
        self.type = type
        self.declarators = declarators

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "declarators", self.declarators


class Labeled(stmt):
    """
    Represents a labeled statement in the Java AST.

    <label>: <statement>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, label: identifier = None, body: stmt = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if label is None:
            raise JASTError("label is required for Labeled")
        if body is None:
            raise JASTError("statement is required for Labeled")
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

    def __init__(self, value: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for Expression")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if test is None:
            raise JASTError("test is required for If")
        if body is None:
            raise JASTError("then_statement is required for If")
        self.test = test
        self.body = body
        self.orelse = orelse

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body
        if self.orelse:
            yield "orelse", self.orelse


class Assert(stmt):
    """
    Represents an assert statement in the Java AST.

    assert <test> [ : <msg> ];
    """

    def __init__(self, test: expr = None, msg: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if test is None:
            raise JASTError("test is required for Assert")
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
    def __init__(self, type: jtype = None, id: identifier = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for Match")
        if id is None:
            raise JASTError("id is required for Match")
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        yield "id", self.id


class Case(switchlabel):
    """
    Represents a case label for switch body in the Java AST.

    case <guard>:
    """

    def __init__(self, guard: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if not guard:
            raise JASTError("constants is required for Case")
        self.guard = guard

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "guard", self.guard


class DefaultCase(switchlabel):
    """
    Represents a default label for switch body in the Java AST.

    default:
    """


class switchgroup(JAST):
    """
    Represents a group of switch labels in the Java AST.

    <label> <label> ... <statement> <statement> ...
    """

    def __init__(
        self,
        labels: List[switchlabel] = None,
        body: List[stmt] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not labels:
            raise JASTError("labels is required for switchgroup")
        if not body:
            raise JASTError("body is required for switchgroup")
        self.labels = labels
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "labels", self.labels
        yield "body", self.body


class switchblock(JAST):
    """
    Represents a body of switch groups and labels in the Java AST.

    [<group> <group> ...] [<label> <label> ...]
    """

    def __init__(
        self,
        groups: List[switchgroup] = None,
        labels: List[switchlabel] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        self.groups = groups or []
        self.labels = labels or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "groups", self.groups
        yield "labels", self.labels


class Switch(stmt):
    """
    Represents a switch statement in the Java AST.

    switch (<value>) { <body> }
    """

    def __init__(self, value: expr = None, body: switchblock = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for Switch")
        if body is None:
            raise JASTError("body is required for Switch")
        self.value = value
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value
        yield "body", self.body


class Throw(stmt):
    """
    Represents a throw statement in the Java AST.

    throw <exc>;
    """

    def __init__(self, exc: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if exc is None:
            raise JASTError("value is required for Throw")
        self.exc = exc

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "exc", self.exc


class While(stmt):
    """
    Represents a while statement in the Java AST.

    while (<test>) <body>
    """

    def __init__(self, test: expr = None, body: stmt = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if test is None:
            raise JASTError("test is required for While")
        if body is None:
            raise JASTError("statement is required for While")
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

    def __init__(self, body: stmt = None, test: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if body is None:
            raise JASTError("statement is required for DoWhile")
        if test is None:
            raise JASTError("test is required for DoWhile")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if body is None:
            raise JASTError("statement is required for For")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for ForEach")
        if id is None:
            raise JASTError("label is required for ForEach")
        if iter is None:
            raise JASTError("value is required for ForEach")
        if body is None:
            raise JASTError("body is required for ForEach")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id
        self.iter = iter
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "id", self.id
        yield "iter", self.iter
        yield "body", self.body


class Break(stmt):
    """
    Represents a break statement in the Java AST.

    break [<label>];
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, label: identifier = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
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
    def __init__(self, label: identifier = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.label = label

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.label:
            yield "label", self.label


class Return(stmt):
    """
    Represents a return statement in the Java AST.

    return [<value>];
    """

    def __init__(self, value: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.value:
            yield "value", self.value


class Synch(stmt):
    """
    Represents a synchronized statement in the Java AST.

    synchronized (<lock>) <body>
    """

    def __init__(self, lock: expr = None, body: Block = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if lock is None:
            raise JASTError("value is required for Synchronized")
        if body is None:
            raise JASTError("body is required for Synchronized")
        self.lock = lock
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "lock", self.lock
        yield "body", self.body


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not excs:
            raise JASTError("excs is required for catch")
        if id is None:
            raise JASTError("label is required for catch")
        if body is None:
            raise JASTError("body is required for catch")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if body is None:
            raise JASTError("body is required for Try")
        if not catches and not final:
            raise JASTError("catches or final is required for Try")
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for resource")
        if variable is None:
            raise JASTError("variable is required for resource")
        self.modifiers = modifiers or []
        self.type = type
        self.variable = variable

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not resources:
            raise JASTError("resources is required for TryWithResources")
        if body is None:
            raise JASTError("body is required for TryWithResources")
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

    def __init__(self, value: expr = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if value is None:
            raise JASTError("value is required for Yield")
        self.value = value

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "value", self.value


# Declarations


# noinspection PyPep8Naming
class declaration(_JAST, abc.ABC):
    """
    Abstract base class for all body in the Java AST.
    """


class EmptyDecl(declaration):
    """
    Represents an empty decl in the Java AST.

    ;
    """


# Package decl


class Package(declaration):
    """
    Represents a package decl in the Java AST.

    package <qname>;
    """

    def __init__(
        self, annotations: List[Annotation] = None, name: qname = None, *vargs, **kwargs
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Package")
        self.annotations = annotations or []
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "name", self.name


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Import")
        self.static = static
        self.name = name
        self.on_demand = on_demand

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Requires")
        self.modifiers = modifiers
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "name", self.name


class Exports(directive):
    """
    Represents an exports directive in the Java AST.

    exports <qname> [to <qname>];
    """

    def __init__(
        self,
        name: qname = None,
        to: qname = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Exports")
        self.name = name
        self.to = to

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Opens")
        self.name = name
        self.to = to

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Uses")
        self.name = name

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name


class Provides(directive):
    """
    Represents a provides directive in the Java AST.

    provides <qname> with <qname>;
    """

    def __init__(
        self,
        name: qname = None,
        with_: qname = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("type is required for Provides")
        if with_ is None:
            raise JASTError("with_ is required for Provides")
        self.name = name
        self.with_ = with_

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        yield "with_", self.with_


class Module(declaration):
    """
    Represents a body decl in the Java AST.

    body <name> { <directive> <directive> ... }
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        open: bool = False,
        name: qname = None,
        body: List[directive] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if name is None:
            raise JASTError("qname is required for Module")
        self.open = open
        self.name = name
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        if self.body:
            yield "body", self.body


# Field Declarations


class declarator(JAST):
    """
    Represents a variable declarator in the Java AST.

    <label> [= <init>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        id: variabledeclaratorid = None,
        init: expr | arrayinit = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id_ is required for declarator")
        self.id = id
        self.init = init

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "id", self.id
        if self.init:
            yield "init", self.init


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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for Field")
        if not declarators:
            raise JASTError("declarators is required for Field")
        self.modifiers = modifiers or []
        self.type = type
        self.declarators = declarators

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if return_type is None:
            raise JASTError("return_type is required for Method")
        if id is None:
            raise JASTError("qname is required for Method")
        self.modifiers = modifiers or []
        self.type_params = type_params
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
        yield "id", self.id
        if self.parameters:
            yield "parameters", self.parameters
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

    <modifier>* <id>(<parameter>, <parameter>, ...) <body>
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        modifiers: List[modifier] = None,
        type_params: typeparams = None,
        id: identifier = None,
        parameters: params = None,
        throws: List[qname] = None,
        body: Block = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required for Constructor")
        if body is None:
            raise JASTError("body is required for Constructor")
        self.modifiers = modifiers or []
        self.type_params = type_params
        self.id = id
        self.parameters = parameters
        self.throws = throws or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_params:
            yield "type_params", self.type_params
        yield "id", self.id
        if self.parameters:
            yield "parameters", self.parameters
        if self.throws:
            yield "throws", self.throws
        if self.body:
            yield "body", self.body


# Initializers


class Initializer(declaration):
    """
    Represents an init in the Java AST.

    { <statement> <statement> ... }
    static { <statement> <statement> ... }
    """

    def __init__(self, body: Block = None, static: bool = False, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if body is None:
            raise JASTError("body is required for Initializer")
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
        extends: jtype = None,
        implements: List[jtype] = None,
        body: List[declaration] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required for Interface")
        self.modifiers = modifiers or []
        self.id = id
        self.type_params = type_params
        self.extends = extends
        self.implements = implements or []
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for AnnotationMethod")
        if id is None:
            raise JASTError("id is required for AnnotationMethod")
        self.modifiers = modifiers or []
        self.type = type
        self.id = id
        self.default = default

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "id", self.id
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
        body: List[declaration] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("qname is required for AnnotationInterfaceDeclaration")
        self.modifiers = modifiers or []
        self.id = id
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "id", self.id
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required for Class")
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


class enumconstant(JAST):
    """
    Represents an enum constant in the Java AST.

    <annotation>* <id> [(<argument>, <argument>, ...)] [<body>]
    """

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        annotations: List[Annotation] = None,
        id: identifier = None,
        args: List[expr] = None,
        body: List[declaration] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("qname is required for enumconstant")
        self.annotations = annotations or []
        self.id = id
        self.args = args
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "id", self.id
        if self.args:
            yield "args", self.args
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("qname is required for Enum")
        self.modifiers = modifiers or []
        self.id = id
        self.implements = implements or []
        self.constants = constants or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "id", self.id
        if self.implements:
            yield "implements", self.implements
        if self.constants:
            yield "constants", self.constants
        if self.body:
            yield "body", self.body


class recordcomponent(JAST):
    """
    Represents a record component in the Java AST.

    <jtype> <id>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type: jtype = None, id: identifier = None, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if type is None:
            raise JASTError("type is required for recordcomponent")
        if id is None:
            raise JASTError("id is required for recordcomponent")
        self.type = type
        self.id = id

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        yield "id", self.id


class Record(declaration):
    """
    Represents a record decl in the Java AST.

    <modifier>* record <id> (<component>, <component>, ...) [implements <jtype>, <jtype>, ...] {
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
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if id is None:
            raise JASTError("id is required for Record")
        self.modifiers = modifiers or []
        self.id = id
        self.type_params = type_params
        self.components = components or []
        self.implements = implements or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "id", self.id
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
        body: List[declaration] = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        self.package = package
        self.imports = imports or []
        self.body = body or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.package:
            yield "package", self.package
        if self.imports:
            yield "imports", self.imports
        yield "body", self.body


class ModularUnit(mod):
    """
    Represents a modular compilation unit in the Java AST.

    [<import> <import> ...] <body>
    """

    def __init__(
        self,
        imports: List[Import] = None,
        body: Module = None,
        *vargs,
        **kwargs,
    ):
        super().__init__(*vargs, **kwargs)
        if not body:
            raise JASTError("body is required for ModularUnit")
        self.imports = imports or []
        self.body = body

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.imports:
            yield "imports", self.imports
        yield "body", self.body
