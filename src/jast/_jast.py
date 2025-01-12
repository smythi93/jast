import abc
from typing import List, Any


class JAST(abc.ABC):
    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return self.__repr__()

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __iter__(self):
        pass


class _JAST(JAST, abc.ABC):
    def __init__(
        self,
        lineno: int = None,
        col_offset: int = None,
        end_lineno: int = None,
        end_col_offset: int = None,
    ):
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


class TypeIdentifier(_JAST):
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        return f"TypeIdentifier({self.name!r})"


class MethodIdentifier(_JAST):
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        return f"MethodIdentifier({self.name!r})"


# Names


class ModuleName(_JAST):
    def __init__(
        self, identifier: Identifier = None, attr: "ModuleName" = None, **kwargs
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for ModuleName")
        self.identifier = identifier
        self.attr = attr

    def __repr__(self):
        return f"ModuleName({self.identifier!r})"

    def __iter__(self):
        yield self.identifier
        if self.attr:
            yield self.attr


class PackageName(_JAST):
    def __init__(
        self, identifier: Identifier = None, attr: "PackageName" = None, **kwargs
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for PackageName")
        self.identifier = identifier
        self.attr = attr

    def __repr__(self):
        return f"PackageName({self.identifier!r})"

    def __iter__(self):
        yield self.identifier
        if self.attr:
            yield self.attr


class TypeName(_JAST):
    def __init__(
        self, package: PackageName = None, identifier: TypeIdentifier = None, **kwargs
    ):
        super().__init__(**kwargs)
        if package is None:
            raise ValueError("package is required for TypeName")
        self.package = package
        self.identifier = identifier

    def __repr__(self):
        return f"TypeName({self.package!r})"

    def __iter__(self):
        yield self.package
        if self.identifier:
            yield self.identifier


class AmbigousName(_JAST):
    def __init__(
        self, identifier: Identifier = None, attr: "AmbigousName" = None, **kwargs
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for AmbigousName")
        self.identifier = identifier
        self.attr = attr

    def __repr__(self):
        return f"AmbigousName({self.identifier!r})"

    def __iter__(self):
        yield self.identifier
        if self.attr:
            yield self.attr


class ExpressionName(_JAST):
    def __init__(
        self, attr: AmbigousName = None, identifier: Identifier = None, **kwargs
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for ExpressionName")
        self.attr = attr
        self.identifier = identifier

    def __repr__(self):
        return f"ExpressionName({self.identifier!r})"

    def __iter__(self):
        if self.attr:
            yield self.attr
        yield self.identifier


# Literals


class Literal(_JAST, abc.ABC):
    def __init__(self, value: Any, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def __repr__(self):
        return f"Literal({self.value!r})"


class IntegerLiteral(Literal):
    def __init__(self, value: int, **kwargs):
        super().__init__(value, **kwargs)


class FloatingPointLiteral(Literal):
    def __init__(self, value: float, **kwargs):
        super().__init__(value, **kwargs)


class BooleanLiteral(Literal):
    def __init__(self, value: bool, **kwargs):
        super().__init__(value, **kwargs)


class CharacterLiteral(Literal):
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


VariableModifier = Final | Annotation

FieldModifier = (
    Annotation | Public | Protected | Private | Static | Final | Transient | Volatile
)


RequiresModifier = Transitive | Static

MethodModifier = (
    Annotation
    | Public
    | Protected
    | Private
    | Abstract
    | Static
    | Final
    | Synchronized
    | Native
    | Strictfp
)

ClassModifier = (
    Annotation
    | Public
    | Protected
    | Private
    | Abstract
    | Static
    | Final
    | Sealed
    | NonSealed
    | Strictfp
)

# Types


class Type(_JAST, abc.ABC):
    pass


class Void(Type):
    def __repr__(self):
        return "void"


class PrimitiveType(Type, abc.ABC):
    def __init__(self, annotations: List[Annotation] = None, **kwargs):
        super().__init__(**kwargs)
        self.annotations = annotations or []

    def __iter__(self):
        if self.annotations:
            yield self.annotations


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


class ReferenceType(Type):
    pass


class WildcardBound(_JAST):
    def __init__(self, type_: ReferenceType = None, extends: bool = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for WildcardBound")
        if extends is None:
            raise ValueError("extends is required for WildcardBound")
        self.type = type_
        self.extends = extends

    def __repr__(self):
        return f"WildcardBound({self.type!r})"

    def __iter__(self):
        yield self.type


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

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        if self.bound:
            yield self.bound


class TypeArguments(_JAST):
    def __init__(self, types: List[ReferenceType | Wildcard] = None, **kwargs):
        super().__init__(**kwargs)
        if not types:
            raise ValueError("types is required for TypeArguments")
        self.types = types

    def __repr__(self):
        return f"TypeArguments({self.types!r})"

    def __iter__(self):
        yield self.types


class Coit(Type):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        identifier: TypeIdentifier = None,
        arguments: TypeArguments = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required")
        self.annotations = annotations or []
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        return f"Coit({self.identifier!r})"

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        yield self.identifier
        if self.arguments:
            yield self.arguments


class ClassType(ReferenceType):
    def __init__(
        self,
        package: PackageName = None,
        coits: List[Coit] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not coits:
            raise ValueError("coits is required")
        self.package = package
        self.coits = coits

    def __repr__(self):
        return f"ClassType({self.coits!r})"

    def __iter__(self):
        if self.package:
            yield self.package
        yield self.coits


class TypeVariable(Type):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        identifier: TypeIdentifier = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required")
        self.annotations = annotations or []
        self.identifier = identifier

    def __repr__(self):
        return f"TypeVariable({self.identifier!r})"

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        yield self.identifier


class Dim(_JAST):
    def __init__(self, annotations: List[Annotation] = None, **kwargs):
        super().__init__(**kwargs)
        self.annotations = annotations or []

    def __iter__(self):
        if self.annotations:
            yield self.annotations


class ArrayType(Type):
    def __init__(self, type_: Type = None, dims: List[Dim] = None, **kwargs):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required")
        self.type = type_
        self.dims = dims or []

    def __repr__(self):
        return f"ArrayType({self.type!r}{'[]' * len(self.dims)})"

    def __iter__(self):
        yield self.type
        yield self.dims


class VariableDeclaratorId(_JAST):
    def __init__(self, identifier: Identifier = None, dims: List[Dim] = None, **kwargs):
        super().__init__(**kwargs)
        if identifier is None:
            raise ValueError("identifier is required for VariableDeclaratorId")
        self.identifier = identifier
        self.dims = dims or []

    def __repr__(self):
        return f"VariableDeclaratorId({self.identifier!r})"

    def __iter__(self):
        yield self.identifier
        if self.dims:
            yield self.dims


# Type Parameters


class TypeBound(_JAST):
    def __init__(self, types: List[ClassType] = None, **kwargs):
        super().__init__(**kwargs)
        if not types:
            raise ValueError("types is required for TypeBound")
        self.types = types

    def __repr__(self):
        return f"TypeBound({self.types!r})"

    def __iter__(self):
        yield self.types


class TypeParameter(_JAST):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        identifier: TypeIdentifier = None,
        bound: TypeBound | TypeVariable = None,
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

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        yield self.identifier
        if self.bound:
            yield self.bound


# Parameters


class ReceiverParameter(_JAST):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        type_: Type = None,
        identifier: Identifier = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for ReceiverParameter")
        self.annotations = annotations or []
        self.type = type_
        self.identifier = identifier

    def __repr__(self):
        return f"ReceiverParameter({self.type!r})"

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        yield self.type
        if self.identifier:
            yield self.identifier


class Parameter(_JAST):
    def __init__(
        self,
        modifiers: List[VariableModifier] = None,
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

    def __iter__(self):
        if self.modifiers:
            yield self.modifiers
        yield self.type
        yield self.identifier


class VariableArityParameter(_JAST):
    def __init__(
        self,
        modifiers: List[VariableModifier] = None,
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

    def __iter__(self):
        if self.modifiers:
            yield self.modifiers
        yield self.type
        if self.annotations:
            yield self.annotations
        yield self.identifier


class FormalParameters(_JAST):
    def __init__(
        self,
        receiver_parameter: ReceiverParameter = None,
        parameters: List[Parameter] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.receiver_parameter = receiver_parameter
        self.parameters = parameters or []

    def __repr__(self):
        return "FormalParameters()"

    def __iter__(self):
        if self.receiver_parameter:
            yield self.receiver_parameter
        if self.parameters:
            yield self.parameters


# Declarations


class Declaration(_JAST, abc.ABC):
    pass


# Package Declaration


class PackageDeclaration(Declaration):
    def __init__(
        self, annotations: List[Annotation] = None, name: PackageName = None, **kwargs
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for PackageDeclaration")
        self.annotations = annotations or []
        self.name = name

    def __repr__(self):
        return f"PackageDeclaration({self.name!r})"

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        yield self.name


# Import Declarations


class ImportDeclaration(Declaration, abc.ABC):
    pass


class SingleTypeImportDeclaration(ImportDeclaration):
    def __init__(self, name: TypeName = None, **kwargs):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for SingleTypeImportDeclaration")
        self.name = name

    def __repr__(self):
        return f"SingleTypeImportDeclaration({self.name!r})"

    def __iter__(self):
        yield self.name


class TypeImportOnDemandDeclaration(ImportDeclaration):
    def __init__(self, name: PackageName = None, **kwargs):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for TypeImportOnDemandDeclaration")
        self.name = name

    def __repr__(self):
        return f"TypeImportOnDemandDeclaration({self.name!r})"

    def __iter__(self):
        yield self.name


class SingleStaticImportDeclaration(ImportDeclaration):
    def __init__(self, name: TypeName = None, identifier: Identifier = None, **kwargs):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for SingleStaticImportDeclaration")
        if identifier is None:
            raise ValueError("identifier is required for SingleStaticImportDeclaration")
        self.name = name
        self.identifier = identifier

    def __repr__(self):
        return f"SingleStaticImportDeclaration({self.name!r}.{self.identifier!r})"

    def __iter__(self):
        yield self.name
        yield self.identifier


class StaticImportOnDemandDeclaration(ImportDeclaration):
    def __init__(self, name: TypeName = None, **kwargs):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for StaticImportOnDemandDeclaration")
        self.name = name

    def __repr__(self):
        return f"StaticImportOnDemandDeclaration({self.name!r})"

    def __iter__(self):
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
        modifiers: List[RequiresModifier] = None,
        name: ModuleName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for RequiresDirective")
        self.modifiers = modifiers
        self.name = name

    def __repr__(self):
        return f"RequiresDirective({self.name!r})"

    def __iter__(self):
        if self.modifiers:
            yield self.modifiers
        yield self.name


class ExportsDirective(ModuleDirective):
    def __init__(
        self,
        name: PackageName = None,
        to: List[ModuleName] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for ExportsDirective")
        self.name = name
        self.to = to or []

    def __repr__(self):
        return f"ExportsDirective({self.name!r})"

    def __iter__(self):
        yield self.name
        if self.to:
            yield self.to


class OpensDirective(ModuleDirective):
    def __init__(
        self,
        name: PackageName = None,
        to: List[ModuleName] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for OpensDirective")
        self.name = name
        self.to = to or []

    def __repr__(self):
        return f"OpensDirective({self.name!r})"

    def __iter__(self):
        yield self.name
        if self.to:
            yield self.to


class UsesDirective(ModuleDirective):
    def __init__(
        self,
        type_: TypeName = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for UsesDirective")
        self.type = type_

    def __repr__(self):
        return f"UsesDirective({self.type!r})"

    def __iter__(self):
        yield self.type


class ProvidesDirective(ModuleDirective):
    def __init__(
        self,
        type_: TypeName = None,
        with_: List[TypeName] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for ProvidesDirective")
        if not with_:
            raise ValueError("with_ is required for ProvidesDirective")
        self.type = type_
        self.with_ = with_

    def __repr__(self):
        return f"ProvidesDirective({self.type!r})"

    def __iter__(self):
        yield self.type
        yield self.with_


class ModuleDeclaration(Declaration):
    def __init__(
        self,
        annotations: List[Annotation] = None,
        open_: bool = None,
        identifiers: List[Identifier] = None,
        directives: List[ModuleDirective] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if not identifiers:
            raise ValueError("identifiers is required for ModuleDeclaration")
        self.annotations = annotations or []
        self.open_ = open_
        self.identifiers = identifiers
        self.directives = directives or []

    def __repr__(self):
        return "ModuleDeclaration()"

    def __iter__(self):
        if self.annotations:
            yield self.annotations
        yield self.identifiers
        if self.directives:
            yield self.directives


# Field Declarations


class VariableDeclarator(_JAST):
    def __init__(
        self,
        id_: VariableDeclaratorId = None,
        initializer: Expression | ArrayInitializer = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if id_ is None:
            raise ValueError("id_ is required for VariableDeclarator")
        self.id = id_
        self.initializer = initializer

    def __repr__(self):
        return f"VariableDeclarator({self.id!r})"

    def __iter__(self):
        yield self.id
        if self.initializer:
            yield self.initializer


class FieldDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[FieldModifier] = None,
        type_: Type = None,
        declarators: List[VariableDeclarator] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for FieldDeclaration")
        if not declarators:
            raise ValueError("declarators is required for FieldDeclaration")
        self.modifiers = modifiers or []
        self.type = type_
        self.declarators = declarators

    def __repr__(self):
        return f"FieldDeclaration({self.type!r})"

    def __iter__(self):
        if self.modifiers:
            yield self.modifiers
        yield self.type
        yield self.declarators


# Method Declarations


class MethodHeader:
    """
    For carrying the header of a method declaration during AST construction.
    """

    def __init__(
        self,
        type_parameters: List[TypeParameter] = None,
        annotations: List[Annotation] = None,
        type_: Type = None,
        name: MethodIdentifier = None,
        parameters: FormalParameters = None,
        dims: List[Dim] = None,
        throws: List[ClassType | TypeVariable] = None,
    ):
        self.type_parameters = type_parameters
        self.annotations = annotations
        self.type = type_
        self.name = name
        self.parameters = parameters
        self.dims = dims
        self.throws = throws


class MethodDeclarator:
    """
    For carrying the declarator of a method declaration during AST construction.
    """

    def __init__(
        self,
        id_: MethodIdentifier = None,
        parameters: FormalParameters = None,
        dims: List[Dim] = None,
    ):
        self.id = id_
        self.parameters = parameters
        self.dims = dims


class MethodDeclaration(Declaration):
    def __init__(
        self,
        modifiers: List[MethodModifier] = None,
        type_parameters: List[TypeParameter] = None,
        annotations: List[Annotation] = None,
        type_: Type = None,
        name: MethodIdentifier = None,
        parameters: FormalParameters = None,
        dims: List[Dim] = None,
        throws: List[ClassType | TypeVariable] = None,
        body: List[BlockStatement] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if type_ is None:
            raise ValueError("type_ is required for MethodDeclaration")
        if name is None:
            raise ValueError("name is required for MethodDeclaration")
        self.modifiers = modifiers or []
        self.type_parameters = type_parameters or []
        self.annotations = annotations or []
        self.type = type_
        self.name = name
        self.parameters = parameters
        self.dims = dims or []
        self.throws = throws or []
        self.body = body or []

    def __repr__(self):
        return f"MethodDeclaration({self.name!r})"

    def __iter__(self):
        if self.modifiers:
            yield self.modifiers
        if self.type_parameters:
            yield self.type_parameters
        if self.annotations:
            yield self.annotations
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


# Class Declarations


class ClassDeclaration(TopLevelDeclaration, abc.ABC):
    pass


ClassMemberDeclaration = (
    FieldDeclaration
    | MethodDeclaration
    | ClassDeclaration
    | InterfaceDeclaration
    | EmptyDeclaration
)


class InstanceInitializer(Declaration):
    def __init__(self, body: List[BlockStatement] = None, **kwargs):
        super().__init__(**kwargs)
        if not body:
            raise ValueError("body is required for InstanceInitializer")
        self.body = body

    def __repr__(self):
        return "InstanceInitializer()"

    def __iter__(self):
        yield self.body


class StaticInitializer(Declaration):
    def __init__(self, body: List[BlockStatement] = None, **kwargs):
        super().__init__(**kwargs)
        if not body:
            raise ValueError("body is required for StaticInitializer")
        self.body = body

    def __repr__(self):
        return "StaticInitializer()"

    def __iter__(self):
        yield self.body


ClassBodyDeclaration = (
    ClassMemberDeclaration
    | InstanceInitializer
    | StaticInitializer
    | ConstructorDeclaration
)


class NormalClassDeclaration(ClassDeclaration):
    def __init__(
        self,
        modifiers: List[ClassModifier] = None,
        name: TypeIdentifier = None,
        type_parameters: List[TypeParameter] = None,
        extends: ClassType = None,
        implements: List[ClassType] = None,
        permits: List[TypeName] = None,
        body: List[ClassBodyDeclaration] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if name is None:
            raise ValueError("name is required for NormalClassDeclaration")
        self.modifiers = modifiers or []
        self.name = name
        self.type_parameters = type_parameters or []
        self.extends = extends
        self.implements = implements or []
        self.permits = permits or []
        self.body = body or []

    def __repr__(self):
        return f"NormalClassDeclaration({self.name!r})"

    def __iter__(self):
        if self.modifiers:
            yield self.modifiers
        yield self.name
        if self.type_parameters:
            yield self.type_parameters
        if self.extends:
            yield self.extends
        if self.implements:
            yield self.implements
        if self.permits:
            yield self.permits
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

    def __iter__(self):
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

    def __iter__(self):
        if self.imports:
            yield self.imports
        yield self.module
