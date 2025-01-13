import abc
from typing import List, Any, Iterator, Tuple, Union


class JAST(abc.ABC):
    def __init__(self, **kwargs):
        pass

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return self.__repr__()

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __iter__(self) -> Iterator[Tuple[str, "JAST" | List["JAST"]]]:
        pass


class _JAST(JAST, abc.ABC):
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
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name!r})"


# Names


class QualifiedName(_JAST):
    def __init__(self, identifiers: List[Identifier] = None, **kwargs):
        super().__init__(**kwargs)
        if not identifiers:
            raise ValueError("identifier is required for QualifiedName")
        self.identifiers = identifiers

    def __repr__(self):
        return f"QualifiedName({self.identifiers!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifiers", self.identifiers


# Literals


class Literal(_JAST, abc.ABC):
    def __init__(self, value: Any, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def __repr__(self):
        return f"Literal({self.value!r})"


class IntegerLiteral(Literal):
    def __init__(self, value: int, long: bool = False, **kwargs):
        super().__init__(value, **kwargs)
        self.long = long


class FloatLiteral(Literal):
    def __init__(self, value: float, double: bool = False, **kwargs):
        super().__init__(value, **kwargs)
        self.double = double


class BoolLiteral(Literal):
    def __init__(self, value: bool, **kwargs):
        super().__init__(value, **kwargs)


class CharLiteral(Literal):
    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)


class StringLiteral(Literal):
    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)


class TextBlock(Literal):
    def __init__(self, value: str, **kwargs):
        super().__init__(value, **kwargs)


class NullLiteral(Literal):
    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)


# Modifiers


class Modifier(_JAST, abc.ABC):
    pass


class Transitive(Modifier):
    def __repr__(self):
        return "Transitive()"


class Static(Modifier):
    def __repr__(self):
        return "Static()"


class Public(Modifier):
    def __repr__(self):
        return "Public()"


class Protected(Modifier):
    def __repr__(self):
        return "Protected()"


class Private(Modifier):
    def __repr__(self):
        return "Private()"


class Abstract(Modifier):
    def __repr__(self):
        return "Abstract()"


class Final(Modifier):
    def __repr__(self):
        return "Final()"


class Sealed(Modifier):
    def __repr__(self):
        return "Sealed()"


class NonSealed(Modifier):
    def __repr__(self):
        return "NonSealed()"


class Strictfp(Modifier):
    def __repr__(self):
        return "Strictfp()"


class Transient(Modifier):
    def __repr__(self):
        return "Transient()"


class Volatile(Modifier):
    def __repr__(self):
        return "Volatile()"


class Synchronized(Modifier):
    def __repr__(self):
        return "Synchronized()"


class Native(Modifier):
    def __repr__(self):
        return "Native()"


class Default(Modifier):
    def __repr__(self):
        return "Default()"


class ElementValuePair(_JAST):
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

    def __repr__(self):
        return f"ElementValuePair({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
        yield "value", self.value


class ElementValueArrayInitializer(_JAST):
    def __init__(self, values: List["ElementValue"] = None, **kwargs):
        super().__init__(**kwargs)
        self.values = values or []

    def __repr__(self):
        return f"ElementValueArrayInitializer({self.values!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "values", self.values


class Annotation(Modifier):
    def __init__(
        self,
        name: QualifiedName = None,
        elements: List[ElementValuePair | "ElementValue"] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for Annotation")
        self.name = name
        self.elements = elements

    def __repr__(self):
        return f"Annotation({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "name", self.name
        if self.elements:
            yield "elements", self.elements


ElementValue = ElementValueArrayInitializer | Annotation | "Expr"


# Types


class Type(_JAST, abc.ABC):
    pass


class Void(Type):
    def __repr__(self):
        return "void"


class Var(Type):
    def __repr__(self):
        return "var"


class PrimitiveType(Type, abc.ABC):
    def __init__(self, annotations: List[Annotation] = None, **kwargs):
        super().__init__(**kwargs)
        self.annotations = annotations or []

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations


class Boolean(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "boolean"


class Byte(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "byte"


class Short(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "short"


class Int(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "int"


class Long(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "long"


class Char(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "char"


class Float(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "float"


class Double(PrimitiveType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "double"


class ReferenceType(Type, abc.ABC):
    pass


class WildcardBound(_JAST):
    def __init__(
        self,
        type_: ReferenceType = None,
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

    def __repr__(self):
        return f"WildcardBound({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type


class Wildcard(_JAST):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        bound: WildcardBound = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.annotations = annotations or []
        self.bound = bound

    def __repr__(self):
        return "Wildcard()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        if self.bound:
            yield "bound", self.bound


class TypeArguments(_JAST):
    def __init__(self, types: List[ReferenceType | Wildcard] = None, **kwargs):
        super().__init__(**kwargs)
        if types is None:
            raise ValueError("types is required for TypeArguments")
        self.types = types

    def __repr__(self):
        return f"TypeArguments({self.types!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "types", self.types


class Coit(Type):
    def __init__(
        self,
        identifier: Identifier = None,
        arguments: TypeArguments = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required")
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        return f"Coit({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
        if self.arguments:
            yield "arguments", self.arguments


class ClassType(ReferenceType):
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

    def __repr__(self):
        return f"ClassType({self.coits!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "coits", self.coits


class Dim(_JAST):
    def __init__(self, annotations: List[Annotation] = None, **kwargs):
        super().__init__(**kwargs)
        self.annotations = annotations or []

    def __repr__(self):
        return "Dim()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations


class ArrayType(Type):
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

    def __repr__(self):
        return f"ArrayType({self.type!r}{'[]' * len(self.dims)})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "type", self.type
        if self.dims:
            yield "dims", self.dims


class VariableDeclaratorId(_JAST):
    def __init__(self, identifier: Identifier = None, dims: List[Dim] = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for VariableDeclaratorId")
        self.identifier = identifier
        self.dims = dims or []

    def __repr__(self):
        return f"VariableDeclaratorId({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
        if self.dims:
            yield "dims", self.dims


# Type Parameters


class TypeBound(_JAST):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        types: List[ReferenceType] = None,
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

    def __repr__(self):
        return f"TypeParameter({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier
        if self.bound:
            yield "bound", self.bound


class TypeParameters(_JAST):
    def __init__(self, parameters: List[TypeParameter] = None, **kwargs):
        super().__init__(**kwargs)
        if not parameters:
            raise ValueError("parameters is required for TypeParameters")
        self.parameters = parameters

    def __repr__(self):
        return f"TypeParameters({self.parameters!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "parameters", self.parameters


# Pattern


class Pattern(_JAST):
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

    def __repr__(self):
        return f"Pattern({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier


class GuardedPattern(_JAST):
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

    def __repr__(self):
        return f"GuardedPattern({self.pattern!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "pattern", self.pattern
        yield "conditions", self.conditions


# Operators


class OP(JAST, abc.ABC):
    pass


class AssignmentOP(JAST, abc.ABC):
    pass


class Assign(AssignmentOP):
    def __repr__(self):
        return "Assign()"


class AddAssign(AssignmentOP):
    def __repr__(self):
        return "AddAssign()"


class SubAssign(AssignmentOP):
    def __repr__(self):
        return "SubAssign()"


class MulAssign(AssignmentOP):
    def __repr__(self):
        return "MulAssign()"


class DivAssign(AssignmentOP):
    def __repr__(self):
        return "DivAssign()"


class ModAssign(AssignmentOP):
    def __repr__(self):
        return "ModAssign()"


class AndAssign(AssignmentOP):
    def __repr__(self):
        return "AndAssign()"


class OrAssign(AssignmentOP):
    def __repr__(self):
        return "OrAssign()"


class XorAssign(AssignmentOP):
    def __repr__(self):
        return "XorAssign()"


class LShiftAssign(AssignmentOP):
    def __repr__(self):
        return "LShiftAssign()"


class RShiftAssign(AssignmentOP):
    def __repr__(self):
        return "RShiftAssign()"


class URShiftAssign(AssignmentOP):
    def __repr__(self):
        return "RShiftAssign()"


class Operator(OP, abc.ABC):
    pass


class Or(Operator):
    def __repr__(self):
        return "Or()"


class And(Operator):
    def __repr__(self):
        return "And()"


class BitOr(Operator):
    def __repr__(self):
        return "BinOr()"


class BitXor(Operator):
    def __repr__(self):
        return "ExclusiveOr()"


class BitAnd(Operator):
    def __repr__(self):
        return "And()"


class Eq(Operator):
    def __repr__(self):
        return "Eq()"


class NotEq(Operator):
    def __repr__(self):
        return "NotEq()"


class Lt(Operator):
    def __repr__(self):
        return "Lt()"


class LtE(Operator):
    def __repr__(self):
        return "LtE()"


class Gt(Operator):
    def __repr__(self):
        return "Gt()"


class GtE(Operator):
    def __repr__(self):
        return "GtE()"


class LShift(Operator):
    def __repr__(self):
        return "LShift()"


class RShift(Operator):
    def __repr__(self):
        return "RShift()"


class URShift(Operator):
    def __repr__(self):
        return "URShift()"


class Add(Operator):
    def __repr__(self):
        return "Add()"


class Sub(Operator):
    def __repr__(self):
        return "Sub()"


class Mul(Operator):
    def __repr__(self):
        return "Mul()"


class Div(Operator):
    def __repr__(self):
        return "Div()"


class Mod(Operator):
    def __repr__(self):
        return "Mod()"


class UnaryOperator(OP, abc.ABC):
    pass


class PreInc(UnaryOperator):
    def __repr__(self):
        return "PreInc()"


class PreDec(UnaryOperator):
    def __repr__(self):
        return "PreDec()"


class UAdd(UnaryOperator):
    def __repr__(self):
        return "UAdd()"


class USub(UnaryOperator):
    def __repr__(self):
        return "USub()"


class Invert(UnaryOperator):
    def __repr__(self):
        return "Invert()"


class Not(UnaryOperator):
    def __repr__(self):
        return "Not()"


class PostOperator(OP, abc.ABC):
    pass


class PostInc(PostOperator):
    def __repr__(self):
        return "PostInc()"


class PostDec(PostOperator):
    def __repr__(self):
        return "PostDec()"


# Expressions


class Expr(_JAST, abc.ABC):
    def __init__(self, level: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.level = level


class Call(Expr):
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

    def __repr__(self):
        return "Call()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "function", self.function
        if self.arguments:
            yield "arguments", self.arguments


class Lambda(Expr):
    def __init__(
        self,
        parameters: Identifier
        | List[Identifier]
        | List[Union["Parameter", "VariableArityParameter"]] = None,
        body: Expr | "Block" = None,
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

    def __repr__(self):
        return "Lambda()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "parameters", self.parameters
        yield "body", self.body


class Assignment(Expr):
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

    def __repr__(self):
        return "Assignment()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "target", self.target
        yield "op", self.op
        yield "value", self.value


class IfExp(Expr):
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

    def __repr__(self):
        return "IfExp()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body
        yield "orelse", self.orelse


class BinOp(Expr):
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

    def __repr__(self):
        return "BinOp()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "left", self.left
        yield "op", self.op
        yield "right", self.right


class InstanceOf(Expr):
    def __init__(
        self, expr: Expr = None, type_: ReferenceType | Pattern = None, **kwargs
    ):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for InstanceOf")
        if type_ is None:
            raise ValueError("type_ is required for InstanceOf")
        self.expr = expr
        self.type = type_

    def __repr__(self):
        return "InstanceOf()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "type", self.type


class UnaryOp(Expr):
    def __init__(self, op: UnaryOperator = None, expr: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if op is None:
            raise ValueError("op is required for UnaryOp")
        if expr is None:
            raise ValueError("expr is required for UnaryOp")
        self.op = op
        self.expr = expr

    def __repr__(self):
        return "UnaryOp()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "op", self.op
        yield "expr", self.expr


class PostUnaryOp(Expr):
    def __init__(self, expr: Expr = None, op: PostOperator = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for PostUnaryOp")
        if op is None:
            raise ValueError("op is required for PostUnaryOp")
        self.expr = expr
        self.op = op

    def __repr__(self):
        return "PostUnaryOp()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "op", self.op


class Cast(Expr):
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

    def __repr__(self):
        return "Cast()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "type", self.type
        yield "expr", self.expr


class ObjectCreation(Expr):
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

    def __repr__(self):
        return "ObjectCreation()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "type", self.type
        if self.arguments:
            yield "arguments", self.arguments
        if self.body:
            yield "body", self.body


class DimExpr(_JAST):
    def __init__(
        self, annotations: List[Annotation] = None, expr: Expr = None, **kwargs
    ):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for DimExpr")
        self.annotations = annotations or []
        self.expr = expr

    def __repr__(self):
        return "DimExpr()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.annotations:
            yield "annotations", self.annotations
        yield "expr", self.expr


class ArrayCreation(Expr):
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

    def __repr__(self):
        return "ArrayCreation()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.expr_dims:
            yield "expr_dims", self.expr_dims
        if self.dims:
            yield "dims", self.dims
        if self.initializer:
            yield "initializer", self.initializer


class SwitchExprLabel(_JAST, abc.ABC):
    pass


class ExprCase(SwitchExprLabel):
    def __init__(self, expr: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for ExprCase")
        self.expr = expr

    def __repr__(self):
        return "ExprCase()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr


class SwitchExprRule(_JAST):
    def __init__(
        self,
        label: "SwitchLabel" = None,
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
    def __init__(
        self,
        arguments: List[Expr] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.arguments = arguments

    def __repr__(self):
        return "This()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.arguments:
            yield "arguments", self.arguments


class Super(Expr):
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

    def __repr__(self):
        return "Super()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        if self.identifier:
            yield "identifier", self.identifier
        if self.arguments:
            yield "arguments", self.arguments


class Constant(Expr):
    def __init__(self, value: Literal = None, **kwargs):
        super().__init__(**kwargs)
        if value is None:
            raise ValueError("literal is required for Constant")
        self.literal = value

    def __repr__(self):
        return "Constant()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "literal", self.literal


class Name(Expr):
    def __init__(self, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for Name")
        self.identifier = identifier

    def __repr__(self):
        return "Name()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier


class Class(Expr):
    def __init__(self, type_: Type = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Class")
        self.type = type_

    def __repr__(self):
        return "Class()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type


class ExplictGenericInvocation(Expr):
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

    def __repr__(self):
        return "ExplicitGenericInvocation()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        yield "expr", self.expr


class ArrayAccess(Expr):
    def __init__(self, expr: Expr = None, index: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for ArrayAccess")
        if index is None:
            raise ValueError("index is required for ArrayAccess")
        self.expr = expr
        self.index = index

    def __repr__(self):
        return "ArrayAccess()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "index", self.index


class Member(Expr):
    def __init__(self, expr: Expr = None, member: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expr is None:
            raise ValueError("expr is required for Member")
        if member is None:
            raise ValueError("member is required for Member")
        self.expr = expr
        self.member = member

    def __repr__(self):
        return "Member()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expr", self.expr
        yield "member", self.member


class Reference(Expr):
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

    def __repr__(self):
        return "Reference()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        if self.type_arguments:
            yield "type_arguments", self.type_arguments
        if self.identifier:
            yield "identifier", self.identifier


# Arrays


class ArrayInitializer(_JAST):
    def __init__(self, values: List[Expr | "ArrayInitializer"] = None, **kwargs):
        super().__init__(**kwargs)
        self.values = values or []

    def __repr__(self):
        return f"ArrayInitializer({self.values!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "values", self.values


# Parameters


class ReceiverParameter(_JAST):
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

    def __repr__(self):
        return f"Parameter({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "identifier", self.identifier


class VariableArityParameter(_JAST):
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

    def __repr__(self):
        return f"VariableArityParameter({self.type!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        if self.annotations:
            yield "annotations", self.annotations
        yield "identifier", self.identifier


class FormalParameters(_JAST):
    def __init__(
        self,
        receiver_parameter: ReceiverParameter = None,
        parameters: List[Parameter | VariableArityParameter] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.receiver_parameter = receiver_parameter
        self.parameters = parameters or []

    def __repr__(self):
        return "FormalParameters()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.receiver_parameter:
            yield "receiver_parameter", self.receiver_parameter
        if self.parameters:
            yield "parameters", self.parameters


# Statements


class Statement(_JAST, abc.ABC):
    pass


class LocalClassDeclaration(Statement):
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
    def __init__(self, declaration: "InterfaceDeclaration" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalInterfaceDeclaration")
        self.declaration = declaration

    def __repr__(self):
        return "LocalInterfaceDeclaration()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalRecordDeclaration(Statement):
    def __init__(self, declaration: "RecordDeclaration" = None, **kwargs):
        super().__init__(**kwargs)
        if declaration is None:
            raise ValueError("declaration is required for LocalRecordDeclaration")
        self.declaration = declaration

    def __repr__(self):
        return "LocalRecordDeclaration()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "declaration", self.declaration


class LocalVariableDeclaration(Statement):
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

    def __repr__(self):
        return "LocalVariableDeclaration()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "declarators", self.declarators


class Block(Statement):
    def __init__(self, statements: List[Statement] = None, **kwargs):
        super().__init__(**kwargs)
        self.statements = statements or []

    def __repr__(self):
        return "Block()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "statements", self.statements


class Empty(Statement):
    def __repr__(self):
        return "EmptyStatement()"


class Labeled(Statement):
    def __init__(self, identifier: Identifier = None, body: Statement = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for LabeledStatement")
        if body is None:
            raise ValueError("statement is required for LabeledStatement")
        self.identifier = identifier
        self.body = body

    def __repr__(self):
        return f"LabeledStatement({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "identifier", self.identifier
        yield "body", self.body


class Expression(Statement):
    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for ExpressionStatement")
        self.expression = expression

    def __repr__(self):
        return f"ExpressionStatement({self.expression!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


class If(Statement):
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

    def __repr__(self):
        return "IfStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        yield "body", self.body
        if self.orelse:
            yield "else_statement", self.orelse


class Assert(Statement):
    def __init__(self, test: Expr = None, message: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if test is None:
            raise ValueError("condition is required for AssertStatement")
        self.test = test
        self.message = message

    def __repr__(self):
        return "AssertStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "test", self.test
        if self.message:
            yield "message", self.message


class SwitchLabel(_JAST, abc.ABC):
    pass


class Match(Expr):
    def __init__(self, type_: Type = None, ident: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for Match")
        if ident is None:
            raise ValueError("ident is required for Match")
        self.type = type_
        self.ident = ident

    def __repr__(self):
        return "Match()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "type", self.type
        yield "ident", self.ident


class Case(SwitchLabel):
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
    def __repr__(self):
        return "DefaultCase()"


class Throw(Statement):
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

    def __repr__(self):
        return "SwitchGroup()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "labels", self.labels
        yield "statements", self.statements


class SwitchBlock(_JAST):
    def __init__(
        self,
        groups: List[SwitchGroup] = None,
        labels: List[SwitchLabel] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.groups = groups or []
        self.labels = labels or []

    def __repr__(self):
        return "SwitchGroupBlock()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "groups", self.groups
        yield "labels", self.labels


class Switch(Statement):
    def __init__(self, expression: Expr = None, block: SwitchBlock = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for SwitchStatement")
        if not block:
            raise ValueError("blocks is required for SwitchStatement")
        self.expression = expression
        self.block = block

    def __repr__(self):
        return "SwitchStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression
        yield "block", self.block


class While(Statement):
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

    def __repr__(self):
        return "ForStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.init:
            yield "init", self.init
        if self.test:
            yield "test", self.test
        if self.update:
            yield "update", self.update
        yield "body", self.body


class ForEach(Statement):
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

    def __repr__(self):
        return "ForEachStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "type", self.type
        yield "identifier", self.identifier
        yield "expression", self.expression
        yield "body", self.body


class Break(Statement):
    def __init__(self, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        self.identifier = identifier

    def __repr__(self):
        return f"BreakStatement({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.identifier:
            yield "identifier", self.identifier


class Continue(Statement):
    def __init__(self, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        self.identifier = identifier

    def __repr__(self):
        return f"ContinueStatement({self.identifier!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.identifier:
            yield "identifier", self.identifier


class Return(Statement):
    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        self.expression = expression

    def __repr__(self):
        return f"ReturnStatement({self.expression!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.expression:
            yield "expression", self.expression


class Synch(Statement):
    def __init__(self, expression: Expr = None, block: Block = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for SynchronizedStatement")
        if block is None:
            raise ValueError("block is required for SynchronizedStatement")
        self.expression = expression
        self.block = block

    def __repr__(self):
        return "SynchronizedStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression
        yield "block", self.block


class CatchClause(_JAST):
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

    def __repr__(self):
        return f"CatchClause()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        yield "exceptions", self.exceptions
        yield "identifier", self.identifier
        yield "body", self.body


class Try(Statement):
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

    def __repr__(self):
        return "TryStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "body", self.body
        if self.catches:
            yield "catches", self.catches
        if self.final:
            yield "final", self.final


class Resource(_JAST):
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

    def __repr__(self):
        return "TryWithResourcesStatement()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "resources", self.resources
        yield "body", self.body
        if self.catches:
            yield "catches", self.catches
        if self.final:
            yield "final", self.final


class Yield(Statement):
    def __init__(self, expression: Expr = None, **kwargs):
        super().__init__(**kwargs)
        if expression is None:
            raise ValueError("expression is required for YieldStatement")
        self.expression = expression

    def __repr__(self):
        return f"YieldStatement({self.expression!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield "expression", self.expression


# Declarations


class Declaration(_JAST, abc.ABC):
    pass


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
            yield self.annotations
        yield self.name


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
        yield self.name


# Top Level Declarations


class TopLevelDeclaration(Declaration, abc.ABC):
    pass


class EmptyDeclaration(TopLevelDeclaration):
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
            yield self.modifiers
        yield self.name


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
        yield self.name
        if self.to:
            yield self.to


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
        yield self.name
        if self.to:
            yield self.to


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
        yield self.name


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
        yield self.name
        yield self.with_


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
        yield self.name
        if self.directives:
            yield self.directives


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
        yield self.id
        if self.initializer:
            yield self.initializer


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
            yield self.modifiers
        yield self.type
        yield self.declarators


# Method Declarations


class MethodDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        type_parameters: TypeParameters = None,
        type_: Type = None,
        identifier: Identifier = None,
        parameters: FormalParameters = None,
        dims: List[Dim] = None,
        throws: List[QualifiedName] = None,
        body: Block = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for MethodDeclaration")
        if identifier is None:
            raise ValueError("name is required for MethodDeclaration")
        self.modifiers = modifiers or []
        self.type_parameters = type_parameters or []
        self.type = type_
        self.name = identifier
        self.parameters = parameters
        self.dims = dims or []
        self.throws = throws or []
        self.body = body or []

    def __repr__(self):
        return f"MethodDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield self.modifiers
        if self.type_parameters:
            yield self.type_parameters
        yield self.type
        yield self.name
        if self.parameters:
            yield self.parameters
        if self.dims:
            yield self.dims
        if self.throws:
            yield self.throws
        if self.body:
            yield self.body


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
        self.name = identifier
        self.parameters = parameters
        self.dims = dims or []
        self.throws = throws or []
        self.body = body or []

    def __repr__(self):
        return f"InterfaceMethodDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield "modifiers", self.modifiers
        if self.type_parameters:
            yield "type_parameters", self.type_parameters
        if self.annotations:
            yield "annotations", self.annotations
        yield "return_type", self.return_type
        yield "name", self.name


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
        yield self.body


class StaticInitializer(Declaration):
    def __init__(self, body: Block = None, **kwargs):
        super().__init__(**kwargs)
        if not body:
            raise ValueError("body is required for StaticInitializer")
        self.body = body

    def __repr__(self):
        return "StaticInitializer()"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        yield self.body


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
            yield self.modifiers
        if self.type_parameters:
            yield self.type_parameters
        yield self.identifier
        if self.parameters:
            yield self.parameters
        if self.body:
            yield self.body


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
            yield self.modifiers
        yield self.identifier
        if self.body:
            yield self.body


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
            yield self.modifiers
        yield self.type
        yield self.declarators


# InterfaceDeclaration


class InterfaceDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        type_parameters: TypeParameters = None,
        extends: List[ReferenceType] = None,
        permits: List[ReferenceType] = None,
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
            yield self.modifiers
        yield self.identifier
        if self.type_parameters:
            yield self.type_parameters
        if self.extends:
            yield self.extends
        if self.permits:
            yield self.permits
        if self.body:
            yield self.body


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
        self.name = identifier
        self.default = default

    def __repr__(self):
        return f"AnnotationMethodDeclaration({self.name!r})"

    def __iter__(self) -> Iterator[Tuple[str, JAST | List[JAST]]]:
        if self.modifiers:
            yield self.modifiers
        yield self.type
        yield self.name
        if self.default:
            yield self.default


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
            yield self.modifiers
        yield self.type
        yield self.declarators


class AnnotationDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        extends: List[ReferenceType] = None,
        permits: List[ReferenceType] = None,
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
            yield self.modifiers
        yield self.name
        if self.extends:
            yield self.extends
        if self.permits:
            yield self.permits
        if self.body:
            yield self.body


# Class Declarations


class ClassDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[Modifier] = None,
        identifier: Identifier = None,
        type_parameters: TypeParameters = None,
        extends: ReferenceType = None,
        implements: List[ReferenceType] = None,
        permits: List[ReferenceType] = None,
        body: List[Declaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("name is required for NormalClassDeclaration")
        self.modifiers = modifiers or []
        self.identifier = identifier
        self.type_parameters = type_parameters or []
        self.extends = extends
        self.implements = implements or []
        self.permits = permits or []
        self.body = body or []

    def __repr__(self):
        return f"NormalClassDeclaration({self.identifier!r})"

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
            yield self.annotations
        yield self.name
        if self.arguments:
            yield self.arguments
        if self.body:
            yield self.body


class EnumDeclaration(ClassDeclaration):
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
            yield self.modifiers
        yield self.name
        if self.implements:
            yield self.implements
        if self.body:
            yield self.body


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
        yield self.type
        yield self.identifier


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
            yield self.modifiers
        yield self.name
        if self.components:
            yield self.components
        if self.body:
            yield self.body


# Compilation Unit


class CompilationUnit(JAST, abc.ABC):
    pass


class OrdinaryCompilationUnit(CompilationUnit):
    def __init__(
        self,
        package: PackageDeclaration = None,
        imports: List[ImportDeclaration] = None,
        declarations: List[TopLevelDeclaration] = None,
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
            yield self.package
        if self.imports:
            yield self.imports
        if self.declarations:
            yield self.declarations


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
            yield self.imports
        yield self.module
