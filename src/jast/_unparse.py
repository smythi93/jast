import jast._jast as jast

from jast._visitors import JNodeVisitor


class _Unparser(JNodeVisitor):
    def __init__(self, indent=4):
        self._indent = indent
        self._current_level = 0
        self._current_expr_level = -1
        self._level_can_be_equal = True
        self._ignore_indent_block = False

    def _check_level(self, level) -> bool:
        if level < self._current_expr_level:
            return True
        elif not self._level_can_be_equal and level == self._current_expr_level:
            return True
        return False

    def visit_identifier(self, node: jast.identifier) -> str:
        return node

    def visit_qname(self, node: jast.qname) -> str:
        return ".".join([self.visit(identifier) for identifier in node.identifiers])

    def visit_IntLiteral(self, node: jast.IntLiteral) -> str:
        return str(node.value) + ("l" if node.long else "")

    def visit_FloatLiteral(self, node: jast.FloatLiteral) -> str:
        return str(node.value) + ("d" if node.double else "")

    def visit_BoolLiteral(self, node: jast.BoolLiteral) -> str:
        return "true" if node.value else "false"

    def visit_CharLiteral(self, node: jast.CharLiteral) -> str:
        return f"'{node.value}'"

    def visit_StringLiteral(self, node: jast.StringLiteral) -> str:
        return f'"{node.value}"'

    def visit_TextBlock(self, node: jast.TextBlock) -> str:
        return f'"""{node.value}"""'

    def visit_NullLiteral(self, node: jast.NullLiteral) -> str:
        return "null"

    def visit_Abstract(self, node: jast.Abstract) -> str:
        return "abstract"

    def visit_Default(self, node: jast.Default) -> str:
        return "default"

    def visit_Final(self, node: jast.Final) -> str:
        return "final"

    def visit_Native(self, node: jast.Native) -> str:
        return "native"

    def visit_NonSealed(self, node: jast.NonSealed) -> str:
        return "non-sealed"

    def visit_Private(self, node: jast.Private) -> str:
        return "private"

    def visit_Protected(self, node: jast.Protected) -> str:
        return "protected"

    def visit_Public(self, node: jast.Public) -> str:
        return "public"

    def visit_Sealed(self, node: jast.Sealed) -> str:
        return "sealed"

    def visit_Static(self, node: jast.Static) -> str:
        return "static"

    def visit_Strictfp(self, node: jast.Strictfp) -> str:
        return "strictfp"

    def visit_Synchronized(self, node: jast.Synchronized) -> str:
        return "synchronized"

    def visit_Transient(self, node: jast.Transient) -> str:
        return "transient"

    def visit_Transitive(self, node: jast.Transitive) -> str:
        return "transitive"

    def visit_Volatile(self, node: jast.Volatile) -> str:
        return "volatile"

    def visit_elementvaluepair(self, node: jast.elementvaluepair) -> str:
        return f"{self.visit(node.id)} = {self.visit(node.value)}"

    def visit_elementarrayinit(self, node: jast.elementarrayinit) -> str:
        return f"{{{', '.join([self.visit(value) for value in node.values])}}}"

    def visit_Annotation(self, node: jast.Annotation) -> str:
        return f"@{self.visit(node.name)}({', '.join([self.visit(value) for value in node.elements])})"

    def visit_Void(self, node: jast.Void) -> str:
        return "void"

    def visit_Var(self, node: jast.Var) -> str:
        return "var"

    def visit_Boolean(self, node: jast.Boolean) -> str:
        return "boolean"

    def visit_Byte(self, node: jast.Byte) -> str:
        return "byte"

    def visit_Short(self, node: jast.Short) -> str:
        return "short"

    def visit_Int(self, node: jast.Int) -> str:
        return "int"

    def visit_Long(self, node: jast.Long) -> str:
        return "long"

    def visit_Char(self, node: jast.Char) -> str:
        return "char"

    def visit_Float(self, node: jast.Float) -> str:
        return "float"

    def visit_Double(self, node: jast.Double) -> str:
        return "double"

    def visit_wildcardbound(self, node: jast.wildcardbound) -> str:
        if node.super_:
            return "super " + self.visit(node.type)
        elif node.extends:
            return "extends " + self.visit(node.type)
        else:
            raise ValueError("wildcardbound must have either super or extends")

    def visit_Wildcard(self, node: jast.Wildcard) -> str:
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        bound = self.visit(node.bound) if node.bound else ""
        if annotations:
            return f"{annotations} ?{bound}"
        return f"?{bound}"

    def visit_typeargs(self, node: jast.typeargs) -> str:
        return f"<{', '.join([self.visit(type_arg) for type_arg in node.types])}>"

    def visit_ArrayType(self, node: jast.ArrayType) -> str:
        return f"{self.visit(node.type)}{''.join([self.visit(dims) for dims in node.dims])}"

    def visit_dim(self, node: jast.dim) -> str:
        return "[]"

    def visit_typebound(self, node: jast.typebound) -> str:
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        return annotations + " & ".join([self.visit(bound) for bound in node.types])

    def visit_typeparam(self, node: jast.typeparam) -> str:
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        type_bound = (
            " extends " + self.visit_typebound(node.bound) if node.bound else ""
        )
        if annotations:
            return f"{annotations} {self.visit(node.id)}{type_bound}"
        return f"{self.visit(node.id)}{type_bound}"

    def visit_typeparams(self, node: jast.typeparams) -> str:
        return (
            f"<{', '.join([self.visit(type_param) for type_param in node.parameters])}>"
        )

    def visit_pattern(self, node: jast.pattern) -> str:
        modifiers = " ".join([self.visit(mod) for mod in node.modifiers])
        type_ = self.visit(node.type)
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        identifier = self.visit(node.id)
        if modifiers:
            type_ = f"{modifiers} {type_}"
        if annotations:
            return f"{type_} {annotations} {identifier}"
        return f"{type_} {identifier}"

    def visit_guardedpattern(self, node: jast.guardedpattern) -> str:
        pattern = self.visit(node.pattern)
        condition = " && ".join([self.visit(cond) for cond in node.conditions])
        if condition:
            return f"{pattern} && {condition}"
        return pattern

    def visit_Or(self, node: jast.Or) -> str:
        return "||"

    def visit_And(self, node: jast.And) -> str:
        return "&&"

    def visit_BitOr(self, node: jast.BitOr) -> str:
        return "|"

    def visit_BitAnd(self, node: jast.BitAnd) -> str:
        return "&"

    def visit_BitXor(self, node: jast.BitXor) -> str:
        return "^"

    def visit_Eq(self, node: jast.Eq) -> str:
        return "=="

    def visit_NotEq(self, node: jast.NotEq) -> str:
        return "!="

    def visit_Lt(self, node: jast.Lt) -> str:
        return "<"

    def visit_LtE(self, node: jast.LtE) -> str:
        return "<="

    def visit_Gt(self, node: jast.Gt) -> str:
        return ">"

    def visit_GtE(self, node: jast.GtE) -> str:
        return ">="

    def visit_LShift(self, node: jast.LShift) -> str:
        return "<<"

    def visit_RShift(self, node: jast.RShift) -> str:
        return ">>"

    def visit_URShift(self, node: jast.URShift) -> str:
        return ">>>"

    def visit_Add(self, node: jast.Add) -> str:
        return "+"

    def visit_Sub(self, node: jast.Sub) -> str:
        return "-"

    def visit_Mult(self, node: jast.Mult) -> str:
        return "*"

    def visit_Div(self, node: jast.Div) -> str:
        return "/"

    def visit_Mod(self, node: jast.Mod) -> str:
        return "%"

    def visit_PreInc(self, node: jast.PreInc) -> str:
        return "++"

    def visit_PreDec(self, node: jast.PreDec) -> str:
        return "--"

    def visit_UAdd(self, node: jast.UAdd) -> str:
        return "+"

    def visit_USub(self, node: jast.USub) -> str:
        return "-"

    def visit_Not(self, node: jast.Not) -> str:
        return "!"

    def visit_Invert(self, node: jast.Invert) -> str:
        return "~"

    def visit_PostInc(self, node: jast.PostInc) -> str:
        return "++"

    def visit_PostDec(self, node: jast.PostDec) -> str:
        return "--"

    def visit_Lambda(self, node: jast.Lambda) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        if isinstance(node.args, list):
            expr = f"({', '.join([self.visit(param) for param in node.args])}) -> {self.visit(node.body)}"
        else:
            expr = f"{self.visit(node.args)} -> {self.visit(node.body)}"
        self._current_expr_level = pre_level
        if par:
            return f"({expr})"
        return expr

    def visit_Assign(self, node: jast.Assign) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = False
        target = self.visit(node.target)
        operator = self.visit(node.op)
        self._level_can_be_equal = True
        value = self.visit(node.value)
        self._current_expr_level = pre_level
        if par:
            return f"({target} {operator} {value})"
        return f"{target} {operator} {value}"

    def visit_IfExp(self, node: jast.IfExp) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = False
        test = self.visit(node.test)
        self._current_expr_level = -1
        body = self.visit(node.body)
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        orelse = self.visit(node.orelse)
        self._current_expr_level = pre_level
        if par:
            return f"({body} if {test} else {orelse})"
        return f"{body} if {test} else {orelse}"

    def visit_BinOp(self, node: jast.BinOp) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        left = self.visit(node.left)
        operator = self.visit(node.op)
        self._level_can_be_equal = False
        right = self.visit(node.right)
        self._current_expr_level = pre_level
        if par:
            return f"({left} {operator} {right})"
        return f"{left} {operator} {right}"

    def visit_InstanceOf(self, node: jast.InstanceOf) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        expr = self.visit(node.value)
        self._level_can_be_equal = False
        type_ = self.visit(node.type)
        self._current_expr_level = pre_level
        if par:
            return f"({expr} instanceof {type_})"
        return f"{expr} instanceof {type_}"

    def visit_NewObject(self, node: jast.NewObject) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = -1
        self._level_can_be_equal = False
        type_argument = self.visit(node.type_args) + " " if node.type_args else ""
        type_ = self.visit(node.type)
        args = f"({', '.join([self.visit(arg) for arg in node.args])})"
        if node.body:
            body = "{"
            if self._indent > 0:
                body += "\n"
            self._current_level += 1
            for decl in node.body:
                body += self.visit(decl)
                if self._indent > 0:
                    body += "\n"
            self._current_level -= 1
            body += "}"
        else:
            body = ""
        self._current_expr_level = pre_level
        if par:
            return f"(new {type_argument}{type_}{args}{body})"
        return f"new {type_argument}{type_}{args}{body}"

    def visit_NewArray(self, node: jast.NewArray) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = -1
        self._level_can_be_equal = False
        type_ = self.visit(node.type)
        dimensions = "".join([self.visit(dimension) for dimension in node.expr_dims])
        dimensions += "".join([self.visit(dimension) for dimension in node.dims])
        if node.initializer:
            initializer = self.visit(node.initializer)
        else:
            initializer = ""
        self._current_expr_level = pre_level
        if par:
            return f"(new {type_}{dimensions}{initializer})"
        return f"new {type_}{dimensions}{initializer}"

    def visit_Cast(self, node: jast.Cast) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        type_ = self.visit(node.type)
        if annotations:
            type_ = f"{annotations} {type_}"
        value = self.visit(node.value)
        self._current_expr_level = pre_level
        if par:
            return f"(({type_}) {value})"
        return f"({type_}) {value}"

    def visit_UnaryOp(self, node: jast.UnaryOp) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        operator = self.visit(node.op)
        value = self.visit(node.operand)
        self._current_expr_level = pre_level
        if par:
            return f"({operator}{value})"
        return f"{operator}{value}"

    def visit_PostOp(self, node: jast.PostOp) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        value = self.visit(node.operand)
        operator = self.visit(node.op)
        self._current_expr_level = pre_level
        if par:
            return f"({value}{operator})"
        return f"{value}{operator}"

    def visit_SwitchExp(self, node: jast.SwitchExp) -> str:
        pass

    def visit_Reference(self, node: jast.Reference) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.type)
        s += "::"
        if node.type_args:
            s += self.visit(node.type_args)
        if node.id:
            s += self.visit(node.id)
        if node.new:
            s += "new"
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_Call(self, node: jast.Call) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.func)
        s += "("
        s += ", ".join([self.visit(arg) for arg in node.args])
        s += ")"
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_Member(self, node: jast.Member) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.value)
        s += "."
        self._level_can_be_equal = True
        s += self.visit(node.member)
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_Subscript(self, node: jast.Subscript) -> str:
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.value)
        s += "["
        self._current_level = -1
        s += self.visit(node.index)
        s += "]"
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_This(self, node: jast.This) -> str:
        s = "this"
        if node.arguments is not None:
            s += f"({', '.join([self.visit(arg) for arg in node.arguments])})"
        return s

    def visit_Super(self, node: jast.Super) -> str:
        s = "super"
        if node.id:
            s += "."
            if node.type_args:
                s += self.visit(node.type_args)
            s += self.visit(node.id)
        if node.args is not None:
            s += f"({', '.join([self.visit(arg) for arg in node.args])})"
        return s

    def visit_Constant(self, node: jast.Constant) -> str:
        return self.visit(node.value)

    def visit_Name(self, node: jast.Name) -> str:
        return self.visit(node.id)

    def visit_ClassExpr(self, node: jast.ClassExpr) -> str:
        return f"{self.visit(node.type)}.class"

    def visit_ExplictGenericInvocation(
        self, node: jast.ExplicitGenericInvocation
    ) -> str:
        pass

    def visit_ExpCase(self, node: jast.ExpCase) -> str:
        pass

    def visit_ExpDefault(self, node: jast.ExpDefault) -> str:
        pass

    def visit_switchexprule(self, node: jast.switchexprule) -> str:
        pass

    def visit_arrayinit(self, node: jast.arrayinit) -> str:
        return f"{{{', '.join([self.visit(expr) for expr in node.values])}}}"

    def visit_receiver(self, node: jast.receiver) -> str:
        s = self.visit(node.type)
        s += " "
        if node.identifiers:
            s += (
                ".".join([self.visit(identifier) for identifier in node.identifiers])
                + "."
            )
        s += "this"
        return s

    def visit_param(self, node: jast.param) -> str:
        s = " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += self.visit(node.type) + " "
        s += self.visit(node.id)
        return s

    def visit_arity(self, node: jast.arity) -> str:
        s = " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += self.visit(node.type) + " "
        s += " ".join([self.visit(annotation) for annotation in node.annotations])
        s += "... " + self.visit(node.id)
        return s

    def visit_params(self, node: jast.params) -> str:
        s = ""
        if node.receiver_parameter:
            s += self.visit(node.receiver_parameter)
        if s and node.parameters:
            s += ", "
        s += ", ".join([self.visit(param) for param in node.parameters])
        return s

    def visit_LocalClass(self, node: jast.LocalClass) -> str:
        pass

    def visit_LocalInterface(self, node: jast.LocalInterface) -> str:
        pass

    def visit_LocalRecord(self, node: jast.LocalRecord) -> str:
        pass

    def visit_LocalVariable(self, node: jast.LocalVariable) -> str:
        self._ignore_indent_block = False
        s = " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += self.visit(node.type) + " "
        s += ", ".join([self.visit(decl) for decl in node.declarators])
        s += ";"
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + "\n"
        return s

    def visit_Block(self, node: jast.Block) -> str:
        if self._indent > 0:
            if self._ignore_indent_block:
                s = "{\n"
            else:
                s = " " * self._current_level * self._indent + "{" + "\n"
        else:
            s = "{"
        self._ignore_indent_block = False
        self._current_level += 1
        for decl in node.body:
            s += self.visit(decl)
        self._current_level -= 1
        if self._indent > 0:
            s += " " * self._current_level * self._indent + "}" + "\n"
        else:
            s += "}"
        return s

    def visit_Compound(self, node: jast.Compound) -> str:
        self._ignore_indent_block = False
        if self._indent > 0:
            s = " " * self._current_level * self._indent + "\n"
        else:
            s = " "
        return s.join([self.visit(stmt) for stmt in node.body])

    def visit_Empty(self, node: jast.Empty) -> str:
        self._ignore_indent_block = False
        if self._indent > 0:
            return " " * self._current_level * self._indent + ";\n"
        return ";"

    def visit_Labeled(self, node: jast.Labeled) -> str:
        self._ignore_indent_block = False
        if self._indent > 0:
            s = (
                " " * self._current_level * self._indent
                + self.visit(node.label)
                + ":\n"
            )
            self._current_level += 1
            s += self.visit(node.body)
            self._current_level -= 1
        else:
            s = self.visit(node.label) + ": " + self.visit(node.body)
        return s

    def visit_Expression(self, node: jast.Expression) -> str:
        self._ignore_indent_block = False
        s = self.visit(node.value)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_If(self, node: jast.If) -> str:
        self._ignore_indent_block = False
        s = "if (" + self.visit(node.test) + ") "
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s
        self._ignore_indent_block = True
        then = self.visit(node.body)
        s += then
        if s.endswith("}\n"):
            s = s[:-1]
            if node.orelse:
                s += " "
        elif node.orelse:
            if self._indent > 0:
                s += " " * self._current_level * self._indent + "else "
            else:
                s += " else "
        if node.orelse:
            self._ignore_indent_block = True
            orelse = self.visit(node.orelse)
            s += orelse
            if s.endswith("}\n"):
                s = s[:-1]
        if self._indent > 0:
            s += "\n"
        return s

    def visit_Assert(self, node: jast.Assert) -> str:
        self._ignore_indent_block = False
        s = "assert " + self.visit(node.test)
        if node.msg:
            s += " : " + self.visit(node.msg)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Throw(self, node: jast.Throw) -> str:
        self._ignore_indent_block = False
        s = "throw " + self.visit(node.exc)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Switch(self, node: jast.Switch) -> str:
        self._ignore_indent_block = False
        pass

    def visit_While(self, node: jast.While) -> str:
        self._ignore_indent_block = False
        s = "while (" + self.visit(node.test) + ") "
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s
        self._current_level += 1
        body = self.visit(node.body)
        self._current_level -= 1
        if body.lstrip().startswith("{"):
            body = body.lstrip()
        s += body
        if self._indent > 0:
            s += "\n"
        return s

    def visit_DoWhile(self, node: jast.DoWhile) -> str:
        self._ignore_indent_block = False
        s = "do "
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s
        self._current_level += 1
        body = self.visit(node.body)
        self._current_level -= 1
        if body.lstrip().startswith("{"):
            body = body.lstrip()
        s += body
        if self._indent > 0:
            s += " " * self._current_level * self._indent
        s += "while (" + self.visit(node.test) + ");"
        if self._indent > 0:
            s += "\n"
        return s

    def visit_For(self, node: jast.For) -> str:
        self._ignore_indent_block = False
        pass

    def visit_ForEach(self, node: jast.ForEach) -> str:
        self._ignore_indent_block = False
        pass

    def visit_Break(self, node: jast.Break) -> str:
        self._ignore_indent_block = False
        s = "break"
        if node.label:
            s += " " + self.visit(node.label)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Continue(self, node: jast.Continue) -> str:
        self._ignore_indent_block = False
        s = "continue"
        if node.label:
            s += " " + self.visit(node.label)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Return(self, node: jast.Return) -> str:
        self._ignore_indent_block = False
        s = "return"
        if node.value:
            s += " " + self.visit(node.value)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Synch(self, node: jast.Synch) -> str:
        self._ignore_indent_block = False
        pass

    def visit_Try(self, node: jast.Try) -> str:
        self._ignore_indent_block = False
        pass

    def visit_TryWithResources(self, node: jast.TryWithResources) -> str:
        self._ignore_indent_block = False
        pass

    def visit_Yield(self, node: jast.Yield) -> str:
        self._ignore_indent_block = False
        s = "yield"
        if node.value:
            s += " " + self.visit(node.value)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Match(self, node: jast.Match) -> str:
        pass

    def visit_Case(self, node: jast.Case) -> str:
        pass

    def visit_DefaultCase(self, node: jast.DefaultCase) -> str:
        pass

    def visit_switchgroup(self, node: jast.switchgroup) -> str:
        pass

    def visit_switchblock(self, node: jast.switchblock) -> str:
        pass

    def visit_catch(self, node: jast.catch) -> str:
        pass

    def visit_resource(self, node: jast.resource) -> str:
        pass

    def visit_Package(self, node: jast.Package) -> str:
        sep = (
            "\n" + " " * self._current_level * self._indent if self._indent > 0 else " "
        )
        s = sep.join([self.visit(annotation) for annotation in node.annotations])
        if s:
            s += sep
        s += "package " + self.visit(node.name) + ";"
        if self._indent > 0:
            s += "\n"
        return s

    def visit_Import(self, node: jast.Import) -> str:
        s = "import "
        if node.static:
            s += "static "
        s += self.visit(node.name)
        if node.on_demand:
            s += ".*"
        s += ";"
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + "\n"
        return s

    def visit_EmptyDecl(self, node: jast.EmptyDecl) -> str:
        s = ";"
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + "\n"
        return s

    def visit_Module(self, node: jast.Module) -> str:
        pass

    def visit_Field(self, node: jast.Field) -> str:
        s = " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += (
            self.visit(node.type)
            + " "
            + ", ".join([self.visit(decl) for decl in node.declarators])
            + ";"
        )
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + "\n"
        return s

    def visit_Method(self, node: jast.Method) -> str:
        if self._indent > 0:
            s = " " * self._current_level * self._indent
        else:
            s = ""
        s += " ".join([self.visit(mod) for mod in node.modifiers])
        if node.modifiers:
            s += " "
        if node.type_params:
            s += self.visit(node.type_params) + " "
        s += self.visit(node.return_type) + " "
        s += self.visit(node.id)
        s += "(" + self.visit(node.parameters) + ")"
        if node.dims:
            s += "".join([self.visit(dims) for dims in node.dims])
        s += " "
        if node.throws:
            s += "throws " + ", ".join([self.visit(throw) for throw in node.throws])
            s += " "
        self._ignore_indent_block = True
        s += self.visit(node.body)
        return s

    def visit_Class(self, node: jast.Class) -> str:
        if self._indent > 0:
            sep = "\n"
            s = " " * self._current_level * self._indent
        else:
            sep = " "
            s = ""
        s += " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += "class " + self.visit(node.id) + " "
        if node.type_params:
            s += self.visit(node.type_params) + " "
        if node.extends:
            s += "extends " + self.visit(node.extends) + " "
        if node.implements:
            s += (
                "implements "
                + ", ".join([self.visit(inter) for inter in node.implements])
                + " "
            )
        if node.permits:
            s += (
                "permits "
                + ", ".join([self.visit(permit) for permit in node.permits])
                + " "
            )
        s += "{" + sep
        self._current_level += 1
        s += sep.join([self.visit(decl) for decl in node.body])
        self._current_level -= 1
        s += "}"
        if self._indent > 0:
            s += "\n"
        return s


def unparse(node, indent=4):
    return _Unparser(indent).visit(node)
