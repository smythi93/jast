from contextlib import contextmanager, nullcontext
from enum import IntEnum, auto

import jast._jast as jast

from jast._visitors import JNodeVisitor


class _Precedence(IntEnum):
    """
    Precedence levels for Java operators.
    """

    LAMBDA = auto()  # <params> -> <body>
    ASSIGN = auto()  # <target> <op>= <value>
    TERNARY = auto()  # <test> ? <body> : <orelse>
    OR = auto()  # ||
    AND = auto()  # &&
    BIT_OR = auto()  # |
    BIT_XOR = auto()  # ^
    BIT_AND = auto()  # &
    EQ = auto()  # ==, !=
    COMPARE = auto()  # <, <=, >, >=, instanceof
    SHIFT = auto()  # <<, >>, >>>
    ADD = auto()  # +, -
    MULT = auto()  # *, /, %
    TYPE = auto()  # (type) <value>, new <type>(...), new <type>[]...
    UNARY = auto()  # +, -, !, ~, ++, --
    POSTFIX = auto()  # ++, --
    PRIMARY = auto()  # everything else

    def next(self):
        try:
            return self.__class__(self + 1)
        except ValueError:
            return self


class _Unparser(JNodeVisitor):
    def __init__(self, indent=4):
        self._source = []
        self._indent_spaces = indent
        self._indent = 0
        self._current_expr_level = -1
        self._precedences = {}
        self._context_newline = False

    def unparse(self, node: jast.JAST):
        """
        Unparse a JAST node.
        :param node:    The node to unparse.
        :return:        The unparsed source code.
        """
        self.visit(node)
        return "".join(self._source)

    def visit(self, node):
        if node is not None:
            super().visit(node)

    def write(self, *text):
        """
        Write text to the source.
        :param text:    The text to write.
        """
        self._source.extend(filter(None, text))

    def seperator(self):
        """
        :return:   A newline or a space depending on the indent.
        """
        if self._indent_spaces >= 0:
            self.write("\n")
        else:
            self.write(" ")

    def maybe_newline(self, force_newline: bool = False):
        """
        Add a newline if it isn't the start of the generated source and the indent is not negative.
        :param force_newline:   If True, a newline is always added.
        """
        if self._source:
            if force_newline:
                self.write("\n")
            else:
                self.write(self.seperator())

    def fill(self, text="", force_newline: bool = False):
        """
        Indent a piece of text and write it to the source.
        :param text:           The text to indent.
        :param force_newline:  If True, a newline is always added.
        """
        self.maybe_newline(force_newline)
        if self._indent_spaces >= 0:
            self.write(" " * self._indent_spaces * self._indent)
        self.write(text)

    def interleave(self, items, sep, start="", end=""):
        """
        Interleave a list of items with a separator.
        :param items:   The items to interleave.
        :param sep:     The separator.
        :param start:   A text to add at the start.
        :param end:     A text to add at the end.
        """
        if items:
            self.write(start)
            seq = iter(items)
            try:
                self.visit(next(seq))
            except StopIteration:
                pass
            else:
                for item in seq:
                    self.write(sep)
                    self.visit(item)
            self.write(end)

    def traverse(self, items, start="", end=""):
        if items:
            self.write(start)
            for item in items:
                self.visit(item)
            self.write(end)

    def items_view(self, items):
        self.interleave(items, ", ")

    @contextmanager
    def block(self):
        if self._indent >= 0:
            self._indent += 1
            yield
            self._indent -= 1
        else:
            yield

    def optional_block(self, node):
        if isinstance(node, jast.Block):
            self.write(" ")
            return nullcontext()
        else:
            return self.block()

    def block_end(self):
        return self._source[-1].endswith("}")

    def braced_block(self, elements):
        self.write("{")
        with self.block():
            self.traverse(elements)
        self.fill("}")

    @contextmanager
    def buffered(self):
        self._source, original = [], self._source
        yield
        self._source = original + self._source

    @contextmanager
    def delimit(self, start, end):
        self.write(start)
        yield
        self.write(end)

    def delimit_if(self, start, end, condition):
        if condition:
            return self.delimit(start, end)
        return nullcontext()

    def require_parens(self, precedence, node):
        return self.delimit_if("(", ")", self.get_precedence(node) > precedence)

    def get_precedence(self, node):
        return self._precedences.get(node, _Precedence.LAMBDA)

    def set_precedence(self, precedence, *nodes):
        for node in nodes:
            self._precedences[node] = precedence

    def parens(self):
        return self.delimit("(", ")")

    def diamond(self):
        return self.delimit("<", ">")

    def braces(self):
        return self.delimit("{", "}")

    def brackets(self):
        return self.delimit("[", "]")

    def visit_identifier(self, node: jast.identifier):
        self.write(node)

    def visit_qname(self, node: jast.qname):
        self.interleave(node.identifiers, ".")

    def visit_IntLiteral(self, node: jast.IntLiteral):
        self.write(str(node.value))
        if node.long:
            self.write("l")

    def visit_FloatLiteral(self, node: jast.FloatLiteral):
        self.write(str(node.value))
        if node.double:
            self.write("d")

    def visit_BoolLiteral(self, node: jast.BoolLiteral):
        if node.value:
            self.write("true")
        else:
            self.write("false")

    def visit_CharLiteral(self, node: jast.CharLiteral):
        self.write(f"'{node.value}'")

    def visit_StringLiteral(self, node: jast.StringLiteral):
        self.write(f'"{node.value}"')

    def visit_TextBlock(self, node: jast.TextBlock):
        with self.delimit('"""', '"""'):
            with self.block():
                for line in node.value:
                    self.fill(line, force_newline=True)

    def visit_NullLiteral(self, node: jast.NullLiteral):
        self.write("null")

    def visit_Abstract(self, node: jast.Abstract):
        self.write("abstract")

    def visit_Default(self, node: jast.Default):
        self.write("default")

    def visit_Final(self, node: jast.Final):
        self.write("final")

    def visit_Native(self, node: jast.Native):
        self.write("native")

    def visit_NonSealed(self, node: jast.NonSealed):
        self.write("non-sealed")

    def visit_Private(self, node: jast.Private):
        self.write("private")

    def visit_Protected(self, node: jast.Protected):
        self.write("protected")

    def visit_Public(self, node: jast.Public):
        self.write("public")

    def visit_Sealed(self, node: jast.Sealed):
        self.write("sealed")

    def visit_Static(self, node: jast.Static):
        self.write("static")

    def visit_Strictfp(self, node: jast.Strictfp):
        self.write("strictfp")

    def visit_Synchronized(self, node: jast.Synchronized):
        self.write("synchronized")

    def visit_Transient(self, node: jast.Transient):
        self.write("transient")

    def visit_Transitive(self, node: jast.Transitive):
        self.write("transitive")

    def visit_Volatile(self, node: jast.Volatile):
        self.write("volatile")

    def visit_elementvaluepair(self, node: jast.elementvaluepair):
        self.visit_identifier(node.id)
        self.write("=")
        (self.visit(node.value))

    def visit_elementarrayinit(self, node: jast.elementarrayinit):
        with self.braces():
            self.items_view(node.values)

    def visit_Annotation(self, node: jast.Annotation):
        self.write("@")
        (self.visit(node.name))
        if node.elements:
            with self.parens():
                self.items_view(node.elements)

    def visit_Void(self, node: jast.Void):
        self.write("void")

    def visit_Var(self, node: jast.Var):
        self.write("var")

    def visit_Boolean(self, node: jast.Boolean):
        self.write("boolean")

    def visit_Byte(self, node: jast.Byte):
        self.write("byte")

    def visit_Short(self, node: jast.Short):
        self.write("short")

    def visit_Int(self, node: jast.Int):
        self.write("int")

    def visit_Long(self, node: jast.Long):
        self.write("long")

    def visit_Char(self, node: jast.Char):
        self.write("char")

    def visit_Float(self, node: jast.Float):
        self.write("float")

    def visit_Double(self, node: jast.Double):
        self.write("double")

    def visit_wildcardbound(self, node: jast.wildcardbound):
        if node.super_:
            self.write(" super ")
        elif node.extends:
            self.write(" extends ")
        else:
            raise ValueError("wildcardbound must have either super or extends")
        self.visit(node.type)

    def visit_Wildcard(self, node: jast.Wildcard):
        self.traverse(node.annotations, end=" ")
        self.write("?")
        self.visit(node.bound)

    def visit_typeargs(self, node: jast.typeargs):
        with self.diamond():
            self.items_view(node.types)

    def visit_Coit(self, node: jast.Coit):
        self.traverse(node.annotations, end=" ")
        self.visit_identifier(node.id)
        self.visit(node.type_args)

    def visit_ClassType(self, node: jast.ClassType):
        self.traverse(node.annotations, end=" ")
        self.interleave(
            node.coits,
            ".",
        )

    def visit_ArrayType(self, node: jast.ArrayType):
        self.traverse(node.annotations, end=" ")
        self.visit(node.type)
        self.traverse(node.dims)

    def visit_dim(self, node: jast.dim):
        self.traverse(node.annotations)
        self.write("[]")

    def visit_variabledeclaratorid(self, node):
        self.visit_identifier(node.id)
        self.traverse(node.dims)

    def visit_typebound(self, node: jast.typebound):
        self.traverse(node.annotations, end=" ")
        self.interleave(node.types, " & ")

    def visit_typeparam(self, node: jast.typeparam):
        self.traverse(node.annotations, end=" ")
        self.visit_identifier(node.id)
        if node.bound:
            self.write(" extends ")
            self.visit(node.bound)

    def visit_typeparams(self, node: jast.typeparams):
        with self.diamond():
            self.items_view(node.parameters)

    def visit_pattern(self, node: jast.pattern):
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.type)
        self.write(" ")
        self.traverse(node.annotations, end=" ")
        self.visit_identifier(node.id)

    def visit_guardedpattern(self, node: jast.guardedpattern):
        if node.conditions:
            for _ in node.conditions[:-1]:
                self.write("(")
        self.visit(node.value)
        if node.conditions:
            self.write(" && ")
        self.interleave(node.conditions, ") && ")

    def visit_Or(self, node: jast.Or):
        self.write("||")

    def visit_And(self, node: jast.And):
        self.write("&&")

    def visit_BitOr(self, node: jast.BitOr):
        self.write("|")

    def visit_BitAnd(self, node: jast.BitAnd):
        self.write("&")

    def visit_BitXor(self, node: jast.BitXor):
        self.write("^")

    def visit_Eq(self, node: jast.Eq):
        self.write("==")

    def visit_NotEq(self, node: jast.NotEq):
        self.write("!=")

    def visit_Lt(self, node: jast.Lt):
        self.write("<")

    def visit_LtE(self, node: jast.LtE):
        self.write("<=")

    def visit_Gt(self, node: jast.Gt):
        self.write(">")

    def visit_GtE(self, node: jast.GtE):
        self.write(">=")

    def visit_LShift(self, node: jast.LShift):
        self.write("<<")

    def visit_RShift(self, node: jast.RShift):
        self.write(">>")

    def visit_URShift(self, node: jast.URShift):
        self.write(">>>")

    def visit_Add(self, node: jast.Add):
        self.write("+")

    def visit_Sub(self, node: jast.Sub):
        self.write("-")

    def visit_Mult(self, node: jast.Mult):
        self.write("*")

    def visit_Div(self, node: jast.Div):
        self.write("/")

    def visit_Mod(self, node: jast.Mod):
        self.write("%")

    def visit_PreInc(self, node: jast.PreInc):
        self.write("++")

    def visit_PreDec(self, node: jast.PreDec):
        self.write("--")

    def visit_UAdd(self, node: jast.UAdd):
        self.write("+")

    def visit_USub(self, node: jast.USub):
        self.write("-")

    def visit_Not(self, node: jast.Not):
        self.write("!")

    def visit_Invert(self, node: jast.Invert):
        self.write("~")

    def visit_PostInc(self, node: jast.PostInc):
        self.write("++")

    def visit_PostDec(self, node: jast.PostDec):
        self.write("--")

    def visit_Lambda(self, node: jast.Lambda):
        with self.require_parens(_Precedence.LAMBDA, node):
            if isinstance(node.args, list):
                with self.parens():
                    self.items_view(node.args)
            elif isinstance(node.args, jast.params):
                with self.parens():
                    self.visit_params(node.args)
            else:
                self.visit_identifier(node.args)
            self.write(" -> ")
            self.visit(node.body)

    def visit_Assign(self, node: jast.Assign):
        with self.require_parens(_Precedence.ASSIGN, node):
            self.set_precedence(_Precedence.ASSIGN.next(), node.target)
            self.visit(node.target)
            self.write(" ")
            self.visit(node.op)
            self.write("= ")
            self.set_precedence(_Precedence.ASSIGN, node.value)
            self.visit(node.value)

    def visit_IfExp(self, node: jast.IfExp):
        with self.require_parens(_Precedence.TERNARY, node):
            self.set_precedence(_Precedence.TERNARY.next(), node.test)
            self.visit(node.test)
            self.write(" ? ")
            self.set_precedence(_Precedence.LAMBDA, node.body)
            self.visit(node.body)
            self.write(" : ")
            self.set_precedence(_Precedence.LAMBDA, node.orelse)
            self.visit(node.orelse)

    binop_precedence = {
        jast.Or: _Precedence.OR,
        jast.And: _Precedence.AND,
        jast.BitOr: _Precedence.BIT_OR,
        jast.BitXor: _Precedence.BIT_XOR,
        jast.BitAnd: _Precedence.BIT_AND,
        jast.Eq: _Precedence.EQ,
        jast.NotEq: _Precedence.EQ,
        jast.Lt: _Precedence.COMPARE,
        jast.LtE: _Precedence.COMPARE,
        jast.Gt: _Precedence.COMPARE,
        jast.GtE: _Precedence.COMPARE,
        jast.LShift: _Precedence.SHIFT,
        jast.RShift: _Precedence.SHIFT,
        jast.URShift: _Precedence.SHIFT,
        jast.Add: _Precedence.ADD,
        jast.Sub: _Precedence.ADD,
        jast.Mult: _Precedence.MULT,
        jast.Div: _Precedence.MULT,
        jast.Mod: _Precedence.MULT,
    }

    def visit_BinOp(self, node: jast.BinOp):
        operator_precedence = self.binop_precedence[type(node.op)]
        with self.require_parens(operator_precedence, node):
            self.set_precedence(operator_precedence, node.left)
            self.visit(node.left)
            self.write(" ")
            self.visit(node.op)
            self.write(" ")
            self.set_precedence(operator_precedence.next(), node.right)
            self.visit(node.right)

    def visit_InstanceOf(self, node: jast.InstanceOf):
        with self.require_parens(_Precedence.COMPARE, node):
            self.set_precedence(_Precedence.COMPARE, node.value)
            self.visit(node.value)
            self.write(" instanceof ")
            self.visit(node.type)

    def visit_NewObject(self, node: jast.NewObject):
        with self.require_parens(_Precedence.TYPE, node):
            self.write("new")
            self.visit(node.type_args)
            self.write(" ")
            self.visit(node.type)
            with self.parens():
                self.items_view(node.args)
            if node.body:
                self.write(" ")
                self.braced_block(node.body)

    def visit_NewArray(self, node: jast.NewArray):
        with self.require_parens(_Precedence.TYPE, node):
            self.write("new ")
            self.visit(node.type)
            self.interleave(node.expr_dims, "][", "[", "]")
            self.traverse(node.dims)
            if node.init:
                self.write(" ")
                self.visit_arrayinit(node.init)

    def visit_Cast(self, node: jast.Cast):
        with self.require_parens(_Precedence.TYPE, node):
            with self.parens():
                self.traverse(node.annotations, end=" ")
                self.visit(node.type)
            self.write(" ")
            self.set_precedence(_Precedence.TYPE, node.value)
            self.visit(node.value)

    def visit_UnaryOp(self, node: jast.UnaryOp):
        with self.require_parens(_Precedence.UNARY, node):
            self.visit(node.op)
            self.set_precedence(_Precedence.UNARY, node.operand)
            self.visit(node.operand)

    def visit_PostOp(self, node: jast.PostOp):
        with self.require_parens(_Precedence.POSTFIX, node):
            self.set_precedence(_Precedence.POSTFIX, node.operand)
            self.visit(node.operand)
            self.visit(node.op)

    def visit_SwitchExp(self, node: jast.SwitchExp):
        self.write("switch ")
        with self.parens():
            self.visit(node.value)
        self.write(" ")
        self.braced_block(node.rules)

    def visit_Reference(self, node: jast.Reference):
        self.visit(node.type)
        self.write("::")
        self.visit(node.type_args)
        self.visit(node.id)
        if node.new:
            self.write("new")

    def visit_Call(self, node: jast.Call):
        self.set_precedence(_Precedence.PRIMARY, node.func)
        self.visit(node.func)
        with self.parens():
            self.items_view(node.args)

    def visit_Member(self, node: jast.Member):
        self.set_precedence(_Precedence.PRIMARY, node.value)
        self.visit(node.value)
        self.write(".")
        self.visit(node.member)

    def visit_Subscript(self, node: jast.Subscript):
        self.set_precedence(_Precedence.PRIMARY, node.value)
        self.visit(node.value)
        with self.brackets():
            self.visit(node.index)

    def visit_This(self, node: jast.This):
        self.write("this")

    def visit_Super(self, node: jast.Super):
        self.write("super")
        if node.id:
            self.write(".")
            self.visit(node.type_args)
            self.visit_identifier(node.id)

    def visit_Constant(self, node: jast.Constant):
        self.visit(node.value)

    def visit_Name(self, node: jast.Name):
        self.visit_identifier(node.id)

    def visit_ClassExpr(self, node: jast.ClassExpr):
        self.visit(node.type)
        self.write(".class")

    def visit_ExplicitGenericInvocation(self, node):
        self.visit(node.type_args)
        self.visit(node.value)

    def visit_ExpCase(self, node: jast.ExpCase):
        self.write("case")

    def visit_ExpDefault(self, node: jast.ExpDefault):
        self.write("default")

    def visit_switchexprule(self, node: jast.switchexprule):
        self.fill()
        self.visit(node.label)
        if node.cases:
            self.write(" ")
            self.items_view(node.cases)
        if node.arrow:
            self.write(" ->")
        else:
            self.write(":")
        if node.body:
            if len(node.body) == 1 and isinstance(node.body[0], jast.Block):
                self.write(" ")
                self.traverse(node.body)
            else:
                with self.block():
                    self.traverse(node.body)

    def visit_arrayinit(self, node: jast.arrayinit):
        with self.braces():
            self.items_view(node.values)

    def visit_receiver(self, node: jast.receiver):
        self.visit(node.type)
        self.write(" ")
        self.interleave(node.identifiers, ".", end=".")
        self.write("this")

    def visit_param(self, node: jast.param):
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.type)
        self.write(" ")
        self.visit_variabledeclaratorid(node.id)

    def visit_arity(self, node: jast.arity):
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.type)
        self.write(" ")
        self.traverse(node.annotations, end=" ")
        self.write("... ")
        self.visit_variabledeclaratorid(node.id)

    def visit_params(self, node: jast.params):
        self.items_view(filter(None, [node.receiver_param] + node.parameters))

    def visit_LocalType(self, node: jast.LocalType):
        self.visit(node.decl)

    def visit_LocalVariable(self, node: jast.LocalVariable):
        self.fill()
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.type)
        self.write(" ")
        self.items_view(node.declarators)
        self.write(";")

    def visit_Block(self, node: jast.Block):
        self.braced_block(node.body)

    def visit_Compound(self, node: jast.Compound):
        self.traverse(node.body)

    def visit_Empty(self, node: jast.Empty):
        self.fill(";")

    def visit_Labeled(self, node: jast.Labeled):
        self.fill()
        self.visit_identifier(node.label)
        self.write(":")
        self.visit(node.body)

    def visit_Expression(self, node: jast.Expression):
        self.fill()
        self.visit(node.value)
        self.write(";")

    def visit_If(self, node: jast.If):
        self.fill("if ")
        with self.parens():
            self.visit(node.test)
        with self.optional_block(node.body):
            self.visit(node.body)
        if node.orelse:
            if self.block_end():
                self.write(" else")
            else:
                self.fill("else")
            with self.optional_block(node.orelse):
                self.visit(node.orelse)

    def visit_Assert(self, node: jast.Assert):
        self.fill("assert ")
        self.visit(node.test)
        if node.msg:
            self.write(" : ")
            self.visit(node.msg)
        self.write(";")

    def visit_Throw(self, node: jast.Throw):
        self.fill("throw ")
        self.visit(node.exc)
        self.write(";")

    def visit_Switch(self, node: jast.Switch):
        self.fill("switch ")
        with self.parens():
            self.visit(node.value)
        self.write(" ")
        self.visit_switchblock(node.body)

    def visit_While(self, node: jast.While):
        self.fill("while ")
        with self.parens():
            self.visit(node.test)
        with self.optional_block(node.body):
            self.visit(node.body)

    def visit_DoWhile(self, node: jast.DoWhile):
        self.fill("do")
        with self.optional_block(node.body):
            self.visit(node.body)
        if self.block_end():
            self.write(" while ")
        else:
            self.fill("while ")
        with self.parens():
            self.visit(node.test)
        self.write(";")

    def visit_For(self, node: jast.For):
        self.fill("for ")
        with self.parens():
            if isinstance(node.init, list):
                self.items_view(node.init)
                self.write("; ")
            else:
                with self.buffered():
                    self.visit_LocalVariable(node.init)
                self.write(" ")
            self.visit(node.test)
            self.write("; ")
            self.items_view(node.update)
        with self.optional_block(node.body):
            self.visit(node.body)

    def visit_ForEach(self, node: jast.ForEach):
        self.fill("for ")
        with self.parens():
            self.interleave(node.modifiers, " ", end=" ")
            self.visit(node.type)
            self.write(" ")
            self.visit_variabledeclaratorid(node.id)
            self.write(" : ")
            self.visit(node.iter)
        with self.optional_block(node.body):
            self.visit(node.body)

    def visit_Break(self, node: jast.Break):
        self.fill("break")
        if node.label:
            self.write(" ")
            self.visit(node.label)
        self.write(";")

    def visit_Continue(self, node: jast.Continue):
        self.fill("continue")
        if node.label:
            self.write(" ")
            self.visit(node.label)
        self.write(";")

    def visit_Return(self, node: jast.Return):
        self.fill("return")
        if node.value:
            self.write(" ")
            self.visit(node.value)
        self.write(";")

    def visit_Synch(self, node: jast.Synch):
        self.fill("synchronized ")
        with self.parens():
            self.visit(node.lock)
        self.write(" ")
        self.visit(node.body)

    def visit_Try(self, node: jast.Try):
        self.fill("try ")
        self.visit(node.body)
        self.interleave(node.catches, " ", start=" ")
        if node.final:
            self.write(" finally ")
            self.visit(node.final)

    def visit_TryWithResources(self, node: jast.TryWithResources):
        self.fill("try ")
        with self.parens():
            self.interleave(node.resources, "; ")
        self.write(" ")
        self.visit(node.body)
        self.interleave(node.catches, " ", start=" ")
        if node.final:
            self.write(" finally ")
            self.visit(node.final)

    def visit_Yield(self, node: jast.Yield):
        self.fill("yield ")
        self.visit(node.value)
        self.write(";")

    def visit_Match(self, node: jast.Match):
        self.visit(node.type)
        self.write(" ")
        self.visit_identifier(node.id)

    def visit_Case(self, node: jast.Case):
        self.fill("case ")
        self.visit(node.guard)
        self.write(":")

    def visit_DefaultCase(self, node: jast.DefaultCase):
        self.fill("default:")

    def visit_switchgroup(self, node: jast.switchgroup):
        self.traverse(node.labels)
        with self.block():
            self.traverse(node.body)

    def visit_switchblock(self, node: jast.switchblock):
        self.braced_block(node.groups + node.labels)

    def visit_catch(self, node: jast.catch):
        self.write("catch ")
        with self.parens():
            self.interleave(node.modifiers, " ", end=" ")
            self.interleave(node.excs, " | ", end=" ")
            self.visit_identifier(node.id)
        self.write(" ")
        self.visit(node.body)

    def visit_resource(self, node: jast.resource):
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.type)
        self.write(" ")
        self.visit_declarator(node.variable)

    def visit_declarator(self, node):
        self.visit(node.id)
        if node.init:
            self.write(" = ")
            self.visit(node.init)

    def visit_Package(self, node: jast.Package):
        self.fill("package ")
        self.visit_qname(node.name)
        self.write(";")

    def visit_Import(self, node: jast.Import):
        self.fill("import ")
        if node.static:
            self.write("static ")
        self.visit(node.name)
        if node.on_demand:
            self.write(".*")
        self.write(";")

    def visit_EmptyDecl(self, node: jast.EmptyDecl):
        self.fill(";")

    def visit_Module(self, node: jast.Module):
        pass

    def visit_Field(self, node: jast.Field):
        self.fill()
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.type)
        self.write(" ")
        self.items_view(node.declarators)
        self.write(";")

    def visit_Method(self, node: jast.Method):
        self.fill()
        self.fill()
        self.interleave(node.modifiers, " ", end=" ")
        self.visit(node.return_type)
        self.write(" ")
        self.visit_identifier(node.id)
        with self.parens():
            self.visit_params(node.parameters)
        self.traverse(node.dims)
        if node.throws:
            self.write(" throws ")
            self.items_view(node.throws)
        self.write(" ")
        if node.body:
            self.visit(node.body)
        else:
            self.write(";")

    def visit_Class(self, node: jast.Class):
        self.fill()
        self.fill()
        self.interleave(node.modifiers, " ", end=" ")
        self.write("class ")
        self.visit_identifier(node.id)
        self.visit(node.type_params)
        if node.extends:
            self.write(" extends ")
            self.visit(node.extends)
        if node.implements:
            self.write(" implements ")
            self.items_view(node.implements)
        if node.permits:
            self.write(" permits ")
            self.items_view(node.permits)
        self.write(" ")
        self.braced_block(node.body)

    def visit_Interface(self, node: jast.Interface):
        self.fill()
        self.fill()
        self.interleave(node.modifiers, " ", end=" ")
        self.write("interface ")
        self.visit_identifier(node.id)
        self.visit(node.type_params)
        if node.extends:
            self.write(" extends ")
            self.items_view(node.extends)
        if node.permits:
            self.write(" permits ")
            self.items_view(node.permits)
        self.write(" ")
        self.braced_block(node.body)

    def visit_Record(self, node: jast.Record):
        self.fill()
        self.fill()
        self.interleave(node.modifiers, " ", end=" ")
        self.write("record ")
        self.visit_identifier(node.id)
        self.visit(node.type_params)
        with self.parens():
            self.items_view(node.components)
        if node.implements:
            self.write(" implements ")
            self.items_view(node.implements)
        self.write(" ")
        self.braced_block(node.body)


def unparse(node, indent=4):
    return _Unparser(indent).unparse(node)
