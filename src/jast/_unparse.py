import jast._jast as jast

from jast._visitors import JNodeVisitor


class _Unparser(JNodeVisitor):
    def __init__(self, indent=4):
        self._indent = indent
        self._current_level = 0
        self._current_expr_level = -1
        self._level_can_be_equal = True
        self._ignore_indent_block = False

    def _check_level(self, level):
        if level < self._current_expr_level:
            return True
        elif not self._level_can_be_equal and level == self._current_expr_level:
            return True
        return False

    def visit_Identifier(self, node: jast.Identifier):
        return node.name

    def visit_QualifiedName(self, node: jast.QualifiedName):
        return ".".join([self.visit(identifier) for identifier in node.identifiers])

    def visit_IntegerLiteral(self, node):
        return str(node.value) + ("l" if node.long else "")

    def visit_FloatLiteral(self, node):
        return str(node.value) + ("d" if node.double else "")

    def visit_BoolLiteral(self, node):
        return "true" if node.value else "false"

    def visit_CharLiteral(self, node):
        return f"'{node.value}'"

    def visit_StringLiteral(self, node):
        return f'"{node.value}"'

    def visit_TextBlock(self, node):
        return f'"""{node.value}"""'

    def visit_NullLiteral(self, node):
        return "null"

    def visit_Transitive(self, node):
        return "transitive"

    def visit_Static(self, node):
        return "static"

    def visit_Public(self, node):
        return "public"

    def visit_Protected(self, node):
        return "protected"

    def visit_Private(self, node):
        return "private"

    def visit_Abstract(self, node):
        return "abstract"

    def visit_Final(self, node):
        return "final"

    def visit_Sealed(self, node):
        return "sealed"

    def visit_Strictfp(self, node):
        return "strictfp"

    def visit_Transient(self, node):
        return "transient"

    def visit_Volatile(self, node):
        return "volatile"

    def visit_Synchronized(self, node):
        return "synchronized"

    def visit_Native(self, node):
        return "native"

    def visit_Default(self, node):
        return "default"

    def visit_ElementValuePair(self, node):
        return f"{self.visit(node.identifier)} = {self.visit(node.value)}"

    def visit_ElementValueArrayInitializer(self, node):
        return f"{{{', '.join([self.visit(value) for value in node.values])}}}"

    def visit_Annotation(self, node):
        return f"@{self.visit(node.name)}({', '.join([self.visit(value) for value in node.elements])})"

    def visit_Void(self, node):
        return "void"

    def visit_Var(self, node):
        return "var"

    def visit_Boolean(self, node):
        return "boolean"

    def visit_Byte(self, node):
        return "byte"

    def visit_Short(self, node):
        return "short"

    def visit_Int(self, node):
        return "int"

    def visit_Long(self, node):
        return "long"

    def visit_Char(self, node):
        return "char"

    def visit_Float(self, node):
        return "float"

    def visit_Double(self, node):
        return "double"

    def visit_WildcardBound(self, node):
        if node.super:
            return "super " + self.visit(node.type)
        elif node.extends:
            return "extends " + self.visit(node.type)
        else:
            raise ValueError("WildcardBound must have either super or extends")

    def visit_Wildcard(self, node):
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        bound = self.visit(node.bound) if node.bound else ""
        if annotations:
            return f"{annotations} ?{bound}"
        return f"?{bound}"

    def visit_TypeArguments(self, node):
        return f"<{', '.join([self.visit(type_arg) for type_arg in node.types])}>"

    def visit_ArrayType(self, node):
        return f"{self.visit(node.type)}{''.join([self.visit(dims) for dims in node.dims])}"

    def visit_Dim(self, node):
        return "[]"

    def visit_TypeParameter(self, node):
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        type_bound = " extends " + self.visit(node.bound) if node.bound else ""
        if annotations:
            return f"{annotations} {self.visit(node.identifier)}{type_bound}"
        return f"{self.visit(node.identifier)}{type_bound}"

    def visit_TypeParameters(self, node):
        return (
            f"<{', '.join([self.visit(type_param) for type_param in node.parameters])}>"
        )

    def visit_Pattern(self, node):
        modifiers = " ".join([self.visit(mod) for mod in node.modifiers])
        type_ = self.visit(node.type)
        annotations = " ".join(
            [self.visit(annotation) for annotation in node.annotations]
        )
        identifier = self.visit(node.identifier)
        if modifiers:
            type_ = f"{modifiers} {type_}"
        if annotations:
            return f"{type_} {annotations} {identifier}"
        return f"{type_} {identifier}"

    def visit_GuardedPattern(self, node):
        pattern = self.visit(node.pattern)
        condition = " && ".join([self.visit(cond) for cond in node.conditions])
        if condition:
            return f"{pattern} && {condition}"
        return pattern

    def visit_Assign(self, node):
        return "="

    def visit_AddAssign(self, node):
        return "+="

    def visit_SubAssign(self, node):
        return "-="

    def visit_MulAssign(self, node):
        return "*="

    def visit_DivAssign(self, node):
        return "/="

    def visit_ModAssign(self, node):
        return "%="

    def visit_AndAssign(self, node):
        return "&="

    def visit_OrAssign(self, node):
        return "|="

    def visit_XorAssign(self, node):
        return "^="

    def visit_LShiftAssign(self, node):
        return "<<="

    def visit_RShiftAssign(self, node):
        return ">>="

    def visit_URShiftAssign(self, node):
        return ">>>="

    def visit_Or(self, node):
        return "||"

    def visit_And(self, node):
        return "&&"

    def visit_BitOr(self, node):
        return "|"

    def visit_BitAnd(self, node):
        return "&"

    def visit_BitXor(self, node):
        return "^"

    def visit_Eq(self, node):
        return "=="

    def visit_NotEq(self, node):
        return "!="

    def visit_Lt(self, node):
        return "<"

    def visit_LtE(self, node):
        return "<="

    def visit_Gt(self, node):
        return ">"

    def visit_GtE(self, node):
        return ">="

    def visit_LShift(self, node):
        return "<<"

    def visit_RShift(self, node):
        return ">>"

    def visit_URShift(self, node):
        return ">>>"

    def visit_Add(self, node):
        return "+"

    def visit_Sub(self, node):
        return "-"

    def visit_Mul(self, node):
        return "*"

    def visit_Div(self, node):
        return "/"

    def visit_Mod(self, node):
        return "%"

    def visit_PreInc(self, node):
        return "++"

    def visit_PreDec(self, node):
        return "--"

    def visit_UAdd(self, node):
        return "+"

    def visit_USub(self, node):
        return "-"

    def visit_Not(self, node):
        return "!"

    def visit_Invert(self, node):
        return "~"

    def visit_PostInc(self, node):
        return "++"

    def visit_PostDec(self, node):
        return "--"

    def visit_Lambda(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        if isinstance(node.parameters, list):
            expr = f"({', '.join([self.visit(param) for param in node.parameters])}) -> {self.visit(node.body)}"
        else:
            expr = f"{self.visit(node.parameters)} -> {self.visit(node.body)}"
        self._current_expr_level = pre_level
        if par:
            return f"({expr})"
        return expr

    def visit_Assignment(self, node):
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

    def visit_IfExp(self, node):
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

    def visit_BinOp(self, node):
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

    def visit_InstanceOf(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        expr = self.visit(node.expr)
        self._level_can_be_equal = False
        type_ = self.visit(node.type)
        self._current_expr_level = pre_level
        if par:
            return f"({expr} instanceof {type_})"
        return f"{expr} instanceof {type_}"

    def visit_NewObject(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = -1
        self._level_can_be_equal = False
        type_argument = (
            self.visit(node.type_arguments) + " " if node.type_arguments else ""
        )
        type_ = self.visit(node.type)
        args = f"({', '.join([self.visit(arg) for arg in node.arguments])})"
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

    def visit_NewArray(self, node):
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

    def visit_Cast(self, node):
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
        value = self.visit(node.expr)
        self._current_expr_level = pre_level
        if par:
            return f"(({type_}) {value})"
        return f"({type_}) {value}"

    def visit_UnaryOp(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        operator = self.visit(node.op)
        value = self.visit(node.expr)
        self._current_expr_level = pre_level
        if par:
            return f"({operator}{value})"
        return f"{operator}{value}"

    def visit_PostUnaryOp(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        value = self.visit(node.expr)
        operator = self.visit(node.op)
        self._current_expr_level = pre_level
        if par:
            return f"({value}{operator})"
        return f"{value}{operator}"

    def visit_SwitchExpr(self, node):
        pass

    def visit_Reference(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.type)
        s += "::"
        if node.type_arguments:
            s += self.visit(node.type_arguments)
        if node.identifier:
            s += self.visit(node.identifier)
        if node.new:
            s += "new"
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_Call(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.function)
        s += "("
        s += ", ".join([self.visit(arg) for arg in node.arguments])
        s += ")"
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_Member(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.expr)
        s += "."
        self._level_can_be_equal = True
        s += self.visit(node.member)
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_ArrayAccess(self, node):
        par = self._check_level(node.level)
        pre_level = self._current_expr_level
        self._current_expr_level = node.level
        self._level_can_be_equal = True
        s = self.visit(node.expr)
        s += "["
        self._current_level = -1
        s += self.visit(node.index)
        s += "]"
        self._current_expr_level = pre_level
        if par:
            return f"({s})"
        return s

    def visit_This(self, node):
        s = "this"
        if node.arguments is not None:
            s += f"({', '.join([self.visit(arg) for arg in node.arguments])})"
        return s

    def visit_Super(self, node):
        s = "super"
        if node.identifier:
            s += "."
            if node.type_arguments:
                s += self.visit(node.type_arguments)
            s += self.visit(node.identifier)
        if node.arguments is not None:
            s += f"({', '.join([self.visit(arg) for arg in node.arguments])})"
        return s

    def visit_Constant(self, node):
        return self.visit(node.value)

    def visit_Name(self, node):
        return self.visit(node.identifier)

    def visit_Class(self, node):
        return f"{self.visit(node.type)}.class"

    def visit_ExplictGenericInvocation(self, node):
        pass

    def visit_NewInnerObject(self, node):
        pass

    def visit_DimExpr(self, node):
        return f"[{self.visit(node.expr)}]"

    def visit_ExprCase(self, node):
        pass

    def visit_ExprDefault(self, node):
        pass

    def visit_SwitchExprRule(self, node):
        pass

    def visit_ArrayInitializer(self, node):
        return f"{{{', '.join([self.visit(expr) for expr in node.values])}}}"

    def visit_ReceiverParameter(self, node):
        s = self.visit(node.type)
        s += " "
        if node.identifiers:
            s += (
                ".".join([self.visit(identifier) for identifier in node.identifiers])
                + "."
            )
        s += "this"
        return s

    def visit_Parameter(self, node):
        s = " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += self.visit(node.type) + " "
        s += self.visit(node.identifier)
        return s

    def visit_VariableArityParameter(self, node):
        s = " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += self.visit(node.type) + " "
        s += " ".join([self.visit(annotation) for annotation in node.annotations])
        s += "... " + self.visit(node.identifier)
        return s

    def visit_FormalParameters(self, node):
        s = ""
        if node.receiver_parameter:
            s += self.visit(node.receiver_parameter)
        if s and node.parameters:
            s += ", "
        s += ", ".join([self.visit(param) for param in node.parameters])
        return s

    def visit_LocalClassDeclaration(self, node):
        pass

    def visit_LocalInterfaceDeclaration(self, node):
        pass

    def visit_LocalRecordDeclaration(self, node):
        pass

    def visit_LocalVariableDeclaration(self, node):
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

    def visit_Block(self, node):
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

    def visit_Compound(self, node):
        self._ignore_indent_block = False
        if self._indent > 0:
            s = " " * self._current_level * self._indent
        else:
            s = " "
        return s.join([self.visit(stmt) for stmt in node.statements])

    def visit_Empty(self, node):
        self._ignore_indent_block = False
        if self._indent > 0:
            return " " * self._current_level * self._indent + ";\n"
        return ";"

    def visit_Labeled(self, node):
        self._ignore_indent_block = False
        if self._indent > 0:
            s = (
                " " * self._current_level * self._indent
                + self.visit(node.identifier)
                + ":\n"
            )
            self._current_level += 1
            s += self.visit(node.body)
            self._current_level -= 1
        else:
            s = self.visit(node.identifier) + ": " + self.visit(node.body)
        return s

    def visit_Expression(self, node):
        self._ignore_indent_block = False
        s = self.visit(node.expression)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_If(self, node):
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

    def visit_Assert(self, node):
        self._ignore_indent_block = False
        s = "assert " + self.visit(node.test)
        if node.message:
            s += " : " + self.visit(node.message)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Throw(self, node):
        self._ignore_indent_block = False
        s = "throw " + self.visit(node.expression)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Switch(self, node):
        self._ignore_indent_block = False
        pass

    def visit_While(self, node):
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

    def visit_DoWhile(self, node):
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

    def visit_For(self, node):
        self._ignore_indent_block = False
        pass

    def visit_ForEach(self, node):
        self._ignore_indent_block = False
        pass

    def visit_Break(self, node):
        self._ignore_indent_block = False
        s = "break"
        if node.identifier:
            s += " " + self.visit(node.identifier)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Continue(self, node):
        self._ignore_indent_block = False
        s = "continue"
        if node.identifier:
            s += " " + self.visit(node.identifier)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Return(self, node):
        self._ignore_indent_block = False
        s = "return"
        if node.expression:
            s += " " + self.visit(node.expression)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Synch(self, node):
        self._ignore_indent_block = False
        pass

    def visit_Try(self, node):
        self._ignore_indent_block = False
        pass

    def visit_TryWithResources(self, node):
        self._ignore_indent_block = False
        pass

    def visit_Yield(self, node):
        self._ignore_indent_block = False
        s = "yield"
        if node.expression:
            s += " " + self.visit(node.expression)
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + ";\n"
        else:
            s += ";"
        return s

    def visit_Match(self, node):
        pass

    def visit_Case(self, node):
        pass

    def visit_DefaultCase(self, node):
        pass

    def visit_SwitchGroup(self, node):
        pass

    def visit_SwitchBlock(self, node):
        pass

    def visit_CatchClause(self, node):
        pass

    def visit_Resource(self, node):
        pass

    def visit_PackageDeclaration(self, node):
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

    def visit_ImportDeclaration(self, node):
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

    def visit_EmptyDeclaration(self, node):
        s = ";"
        if self._indent > 0:
            s = " " * self._current_level * self._indent + s + "\n"
        return s

    def visit_ModuleDeclaration(self, node):
        pass

    def visit_FieldDeclaration(self, node):
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

    def visit_MethodDeclaration(self, node):
        if self._indent > 0:
            s = " " * self._current_level * self._indent
        else:
            s = ""
        s += " ".join([self.visit(mod) for mod in node.modifiers])
        if node.modifiers:
            s += " "
        if node.type_parameters:
            s += self.visit(node.type_parameters) + " "
        s += self.visit(node.return_type) + " "
        s += self.visit(node.identifier)
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

    def visit_ClassDeclaration(self, node):
        if self._indent > 0:
            sep = "\n"
            s = " " * self._current_level * self._indent
        else:
            sep = " "
            s = ""
        s += " ".join([self.visit(mod) for mod in node.modifiers])
        if s:
            s += " "
        s += "class " + self.visit(node.identifier) + " "
        if node.type_parameters:
            s += self.visit(node.type_parameters) + " "
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
