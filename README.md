# jAST: Analyzing and Modifying Java ASTs with Python

[![Python Version](https://img.shields.io/pypi/pyversions/java-ast)](https://pypi.org/project/java-ast/)
[![GitHub release](https://img.shields.io/github/v/release/smythi93/jast)](https://img.shields.io/github/v/release/smythi93/jast)
[![PyPI](https://img.shields.io/pypi/v/java-ast)](https://pypi.org/project/java-ast/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/smythi93/jast/test-jast.yml?branch=main)](https://img.shields.io/github/actions/workflow/status/smythi93/fixkit/test-jast.yml?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/smythi93/jast/badge.svg?branch=main)](https://coveralls.io/github/smythi93/jast?branch=main)
[![Licence](https://img.shields.io/github/license/smythi93/jast)](https://img.shields.io/github/license/smythi93/jast)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The `jast` module helps Python applications to process trees of the Java
abstract syntax grammar.

An abstract syntax tree can be generated by using the `parse()`
function from this module.  The result will be a tree of objects whose
classes all inherit from `jast.JAST`.

A modified abstract syntax tree can be written back to Java source code
by using the `unparse()` function.  This function takes a tree of objects
and returns a string with the Java source code.

Additionally various helper functions are provided that make working with
the trees simpler. The main intention of the helper functions and this
module in general is to provide an easy-to-use interface for libraries
that work tightly with Java.

## Formal Specification

A formal specification of the Java abstract syntax tree can be represented in 
abstract syntax description language (ASDL) as follows:

```asdl
-- builtin types are:
-- identifier, int, float, bool, char, string

module Java
{
    mod = CompilationUnit(Package? package, Import* imports, declaration* body)
        | ModularUnit(Import* imports, Module body)

    declaration = EmptyDecl()
        | CompoundDecl(declaration* body)
        | Package(Annotation* annotations, qname name)
        | Import(bool? static, qname name, bool? on_demand)
        | Module(bool? open, qname name, directive* directives)
        | Field(modifier* modifiers, jtype type, declarator+ declarators)
        | Method(modifier* modifiers, typeparams? type_params, Annotation* annotations,
                 jtype return_type, identifier id, params? parameters, dim* dims,
                 qname* throws, Block? body)
        | Constructor(modifier* modifiers, typeparams? type_params, identifier id,
                      params? parameters, Block body)
        | AnnotationMethod(modifier* modifiers, jtype type, identifier id,
                           (elementarrayinit | Annotation | expr)? default_value)
        | Initializer(Block body, bool? static)
        | Class(modifier* modifiers, identifier id, typeparams? type_params,
                jtype? extends, jtype* implements, jtype* permits, declaration* body)
        | Enum(modifier* modifiers, identifier id, jtype* implements,
               enumconstant* constants, declaration* body)
        | Interface(modifier* modifiers, identifier id, typeparams? type_params,
                    jtype? extends, jtype* implements, declaration* body)
        | AnnotationDecl(modifier* modifiers, identifier id, declaration* body)
        | Record(modifier* modifiers, identifier id, typeparams? type_params,
                 recordcomponent* components, jtype* implements, declaration* body)
        attributes (int lineno, int col_offset, int end_lineno, int end_col_offset)

    directive = Requires(modifier* modifiers, qname name)
        | Exports(qname name, qname to)
        | Opens(qname name, qname to)
        | Uses(qname name)
        | Provides(qname name, qname with_)
        attributes (int lineno, int col_offset, int end_lineno, int end_col_offset)

    stmt = Empty()
        | Block(stmt* body)
        | Compound(stmt* body)

        | LocalType((Class | Interface | Record) decl)
        | LocalVariable(modifier* modifiers, jtype type, declarator+ variables)

        | Labeled(identifier label, stmt body)

        | If(expr test, stmt body, stmt? orelse)
        | Switch(expr value, switchblock body)
        | While(expr test, stmt body)
        | DoWhile(stmt body, expr test)
        | For((expr* | LocalVariable?) init, expr? test, expr* update, stmt body)
        | ForEach(modifier* modifiers, jtype type,
                  identifier id, expr iter, stmt body)
        | Try(Block body, catch* catches, Block? final)
        | TryWithResources((resource | qname)+ resources,
                           Block body, catch* catches, Block? final)
        | Assert(expr test, expr? msg)
        | Throw(expr exc)
        | Expr(expr value)
        | Return(expr? value)
        | Yield(expr value)
        | Break(identifier? label)
        | Continue(identifier? label)
        | Synch(expr lock, Block body)
        attributes (int lineno, int col_offset, int end_lineno, int end_col_offset)

    expr = Lambda((identifier | identifier* | params) args, (expr | Block) body)
        | Assign(expr target, operator? op, expr value)
        | IfExp(expr test, expr body, expr orelse)
        | BinOp(expr left, operator op, expr right)
        | InstanceOf(expr value, (jtype | pattern) type)
        | UnaryOp(unaryop op, expr operand)
        | PostOp(expr operand, operator op)
        | Cast(Annotation* annotations, typebound type, expr value)
        | NewObject(typeargs? type_args, jtype type, expr* args, declaration* body)
        | NewArray(jtype type, expr* expr_dims, dim* dims, arrayinit? initializer)
        | SwitchExp(expr value, switchexprule* rules)
        | This()
        | Super(typeargs? type_args, identifier? id)
        | Constant(literal value)
        | Name(identifier id)
        | ClassExpr(jtype type)
        | ExplicitGenericInvocation(typeargs? type_args, expr value)
        | Subscript(expr value, expr index)
        | Member(expr value, expr member)
        | Call(expr func, expr* args)
        | Reference((expr | jtype ) type, typeargs? type_args, identifier? id, bool? new)
        | Match(jtype type, identifier id)
        attributes (int lineno, int col_offset, int end_lineno, int end_col_offset)

    operator = Or() | And() | BitOr() | BitXor() | BitAnd() | Eq() | NotEq()
        | Lt() | LtE() | Gt() | GtE() | LShift() | RShift() | URShift()
        | Add() | Sub() | Mult() | Div() | Mod()

    unaryop = PreInc() | PreDec() | UAdd() | USub() | Invert() | Not()

    postop = PostInc() | PostDec()

    enumconstant = (Annotation* annotations, identifier id, expr* args, declaration* body)

    recordcomponent = (jtype type, identifier id)

    switchlabel = Case(expr guard) | DefaultCase()
    switchgroup = (switchlabel* labels, stmt* body)
    switchblock = (switchgroup* groups, switchlabel* labels)

    catch = (modifier* modifiers, qname+ excs, identifier id, Block body)

    resource = (modifier* modifiers, jtype type, declarator variable)

    switchexplabel = ExpCase() | ExpDefault()
    switchexprule = (switchexplabel label, (expr | guardedpattern)* cases,
                     bool arrow, stmt* body)

    arrayinit = ((expr | arrayinit)* values)

    receiver = (jtype type, identifier* identifiers)
    param = (modifier* modifiers, jtype type, variabledeclaratorid id)
    arity = (modifier* modifiers, jtype type, Annotation* annotations, variabledeclaratorid id)
    params = (receiver? receiver_param, (param | arity)* parameters)

    literal = IntLiteral(int value, bool? long) | FloatLiteral(float value, bool? double)
        | BoolLiteral(bool value) | CharLiteral(char value) | StringLiteral(string value)
        | TextBlock(string* value) | NullLiteral()

    modifier = Abstract() | Default() | Final() | Native() | NonSealed() | Private()
        | Protected() | Public() | Sealed() | Static() | Strictfp() | Synchronized()
        | Transient() | Transitive() | Volatile()
        | Annotation(qname name, (elementvaluepair | elementarrayinit | Annotation | expr)* elements)


    elementvaluepair = (identifier id, (elementarrayinit | Annotation | expr) value)
    elementarrayinit = ((elementarrayinit | Annotation | expr)* values)

    jtype = Void() | Var() | Boolean() | Byte() | Short()
        | Int() | Long() | Char() | Float() | Double()
        | Wildcard(Annotation* annotations, wildcardbound? bound)
        | Coit(Annotation* annotations, identifier id, typeargs? type_args)
        | ClassType(Annotation* annotations, Coit+ coits)
        | ArrayType(Annotation* annotations, jtype type, dim* dims)


    wildcardbound = (jtype type, bool? extends, bool? super_)

    typeargs = (jtype+ types)

    dim = (Annotation* annotations)

    variabledeclaratorid = (identifier id, dim* dims)
    declarator = (variabledeclaratorid id, expr? init)

    typebound = (Annotation* annotations, jtype+ types)
    typeparam = (Annotation* annotations, identifier id, typebound? bound)
    typeparams = (typeparam* parameters)

    pattern = (modifier* modifiers, jtype type, Annotation* annotations, identifier id)
    guardedpattern = (pattern value, expr* conditions)

    qname = (identifier+ identifiers)
}
``` 

## Installation

The `jast` module can be installed from the Python Package Index (PyPI)
by running the following command:

```bash
pip install java-ast
```

Depending on your system configuration you might need to use `pip3`:

```bash
pip3 install java-ast
```

## Usage

`jast` provides a simple interface to parse Java source code and work with
the resulting abstract syntax tree. 

### Parsing Java Source Code

The following example demonstrates how
to parse a Java source file and print the names of all classes:

```python
import jast

# Parse the Java source file
with open("HelloWorld.java") as file:
    tree = jast.parse(file.read())
```

The `tree` object is now a tree of objects that represent the Java source as an abstract syntax tree. 

### Visiting Nodes
The following code snippet demonstrates how to print the names of all classes in the tree:

```python
# Print the names of all classes
class NameVisitor(jast.JNodeVisitor):
    def visit_identifier(self, node):
        print(node)


visitor = NameVisitor()
visitor.visit(tree)
```

The `NameVisitor` class is a simple visitor that prints the name of all `Identifier` nodes in the tree.
The `visit()` method is called with the root node of the tree to start the traversal.

### Modifying Nodes

The following code snippet demonstrates how to modify the tree:

```python
# Modify the tree
class NameModifier(jast.JNodeTransformer):
    def visit_identifier(self, node):
        if node == "HelloWorld":
            return jast.identifier("HelloWorld2")
        return node


modifier = NameModifier()
tree = modifier.visit(tree)
```

The `NameModifier` class is a simple transformer that changes the name of the class `HelloWorld` to `HelloWorld2`.
The `visit()` method is called with the root node of the tree to start the transformation.

### Writing Java Source Code

The following code snippet demonstrates how to write the modified tree back to Java source code:

```python
# Write the modified tree back to Java source code
with open("HelloWorld2.java", "w") as file:
    file.write(jast.unparse(tree))
```

The `unparse()` function takes the modified tree and returns a string with the Java source code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
