from typing import List, Dict, Optional

from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

import jast._jast as jast
from jast import typeargs
from jast._parser.JavaParser import JavaParser
from jast._parser.JavaParserVisitor import JavaParserVisitor


class JASTConverter(JavaParserVisitor):
    @staticmethod
    def _get_location_rule(ctx: ParserRuleContext) -> Dict[str, int]:
        if ctx.stop:
            stop = ctx.stop
        else:
            stop = ctx.start
        return {
            "lineno": ctx.start.line,
            "col_offset": ctx.start.column,
            "end_lineno": stop.line,
            "end_col_offset": stop.column,
        }

    @staticmethod
    def _get_location_token(token: TerminalNodeImpl) -> Dict[str, int]:
        return {
            "lineno": token.symbol.line,
            "col_offset": token.symbol.start,
            "end_lineno": token.symbol.line,
            "end_col_offset": token.symbol.stop,
        }

    @staticmethod
    def _set_location_rule(node: jast.JAST, ctx: ParserRuleContext):
        setattr(node, "lineno", ctx.start.line)
        setattr(node, "col_offset", ctx.start.column)
        setattr(node, "end_lineno", ctx.stop.line)
        setattr(node, "end_col_offset", ctx.stop.column)

    def visitCompilationUnit(self, ctx: JavaParser.CompilationUnitContext) -> jast.mod:
        if ctx.ordinaryCompilationUnit():
            return self.visitOrdinaryCompilationUnit(ctx.ordinaryCompilationUnit())
        else:
            return self.visitModularCompilationUnit(ctx.modularCompilationUnit())

    def visitOrdinaryCompilationUnit(
        self, ctx: JavaParser.OrdinaryCompilationUnitContext
    ) -> jast.CompilationUnit:
        package = (
            self.visitPackageDeclaration(ctx.packageDeclaration())
            if ctx.packageDeclaration()
            else None
        )
        imports = [
            self.visitImportDeclaration(import_declaration)
            for import_declaration in ctx.importDeclaration()
        ]
        declarations = [
            self.visitTypeDeclaration(type_declaration)
            for type_declaration in ctx.typeDeclaration()
        ]
        return jast.CompilationUnit(
            package=package,
            imports=imports,
            body=declarations,
            **self._get_location_rule(ctx),
        )

    def visitModularCompilationUnit(
        self, ctx: JavaParser.ModularCompilationUnitContext
    ) -> jast.ModularUnit:
        imports = [
            self.visitImportDeclaration(import_declaration)
            for import_declaration in ctx.importDeclaration()
        ]
        module = self.visitModuleDeclaration(ctx.moduleDeclaration())
        return jast.ModularUnit(
            imports=imports, body=module, **self._get_location_rule(ctx)
        )

    def visitPackageDeclaration(
        self, ctx: JavaParser.PackageDeclarationContext
    ) -> jast.Package:
        annotations = [
            self.visitAnnotation(annotation) for annotation in ctx.annotation()
        ]
        name = self.visitQualifiedName(ctx.qualifiedName())
        return jast.Package(
            annotations=annotations, name=name, **self._get_location_rule(ctx)
        )

    def visitImportDeclaration(
        self, ctx: JavaParser.ImportDeclarationContext
    ) -> jast.Import:
        static = ctx.STATIC() is not None
        name = self.visitQualifiedName(ctx.qualifiedName())
        on_demand = ctx.MUL() is not None
        return jast.Import(
            static=static,
            name=name,
            on_demand=on_demand,
            **self._get_location_rule(ctx),
        )

    def visitTypeDeclaration(
        self, ctx: JavaParser.TypeDeclarationContext
    ) -> jast.declaration:
        modifiers = [
            self.visitClassOrInterfaceModifier(modifier)
            for modifier in ctx.classOrInterfaceModifier()
        ]
        if ctx.classDeclaration():
            declaration = self.visitClassDeclaration(ctx.classDeclaration())
        elif ctx.enumDeclaration():
            declaration = self.visitEnumDeclaration(ctx.enumDeclaration())
        elif ctx.interfaceDeclaration():
            declaration = self.visitInterfaceDeclaration(ctx.interfaceDeclaration())
        elif ctx.annotationTypeDeclaration():
            declaration = self.visitAnnotationTypeDeclaration(
                ctx.annotationTypeDeclaration()
            )
        else:
            declaration = self.visitRecordDeclaration(ctx.recordDeclaration())
        setattr(declaration, "modifiers", modifiers)
        self._set_location_rule(declaration, ctx)
        return declaration

    def visitModifier(self, ctx: JavaParser.ModifierContext) -> jast.modifier:
        if ctx.NATIVE():
            return jast.Native()
        elif ctx.SYNCHRONIZED():
            return jast.Synchronized()
        elif ctx.TRANSIENT():
            return jast.Transient()
        elif ctx.VOLATILE():
            return jast.Volatile()
        else:
            return self.visitClassOrInterfaceModifier(ctx.classOrInterfaceModifier())

    def visitClassOrInterfaceModifier(
        self, ctx: JavaParser.ClassOrInterfaceModifierContext
    ) -> jast.modifier:
        if ctx.PUBLIC():
            return jast.Public()
        elif ctx.PROTECTED():
            return jast.Protected()
        elif ctx.PRIVATE():
            return jast.Private()
        elif ctx.STATIC():
            return jast.Static()
        elif ctx.ABSTRACT():
            return jast.Abstract()
        elif ctx.FINAL():
            return jast.Final()
        elif ctx.STRICTFP():
            return jast.Strictfp()
        elif ctx.SEALED():
            return jast.Sealed()
        elif ctx.NON_SEALED():
            return jast.NonSealed()
        else:
            return self.visitAnnotation(ctx.annotation())

    def visitVariableModifier(
        self, ctx: JavaParser.VariableModifierContext
    ) -> jast.modifier:
        if ctx.FINAL():
            return jast.Final()
        else:
            return self.visitAnnotation(ctx.annotation())

    def visitClassDeclaration(
        self, ctx: JavaParser.ClassDeclarationContext
    ) -> jast.Class:
        identifier = self.visitIdentifier(ctx.identifier())
        type_parameters = (
            self.visitTypeParameters(ctx.typeParameters())
            if ctx.typeParameters()
            else None
        )
        extends = (
            self.visitClassExtends(ctx.classExtends()) if ctx.classExtends() else None
        )
        implements = (
            self.visitClassImplements(ctx.classImplements())
            if ctx.classImplements()
            else None
        )
        permits = (
            self.visitClassPermits(ctx.classPermits()) if ctx.classPermits() else None
        )
        body = self.visitClassBody(ctx.classBody())
        return jast.Class(
            id=identifier,
            type_params=type_parameters,
            extends=extends,
            implements=implements,
            permits=permits,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitClassExtends(self, ctx: JavaParser.ClassExtendsContext) -> jast.jtype:
        return self.visitTypeType(ctx.typeType())

    def visitClassImplements(
        self, ctx: JavaParser.ClassImplementsContext
    ) -> List[jast.jtype]:
        return self.visitTypeList(ctx.typeList())

    def visitClassPermits(
        self, ctx: JavaParser.ClassPermitsContext
    ) -> List[jast.jtype]:
        return self.visitTypeList(ctx.typeList())

    def visitTypeParameters(
        self, ctx: JavaParser.TypeParametersContext
    ) -> jast.typeparams:
        return jast.typeparams(
            parameters=[
                self.visitTypeParameter(type_parameter)
                for type_parameter in ctx.typeParameter()
            ],
        )

    def visitTypeParameter(
        self, ctx: JavaParser.TypeParameterContext
    ) -> jast.typeparam:
        annotations = [
            self.visitAnnotation(annotation) for annotation in ctx.annotation()
        ]
        identifier = self.visitIdentifier(ctx.identifier())
        type_bound = self.visitTypeBound(ctx.typeBound()) if ctx.typeBound() else None
        return jast.typeparam(
            annotations=annotations,
            id=identifier,
            bound=type_bound,
        )

    def visitTypeBound(self, ctx: JavaParser.TypeBoundContext) -> jast.typebound:
        annotations = [
            self.visitAnnotation(annotation) for annotation in ctx.annotation()
        ]
        bounds = [self.visitTypeType(type_type) for type_type in ctx.typeType()]
        return jast.typebound(
            annotations=annotations,
            types=bounds,
        )

    def visitEnumDeclaration(self, ctx: JavaParser.EnumDeclarationContext) -> jast.Enum:
        identifier = self.visitIdentifier(ctx.identifier())
        implements = (
            self.visitClassImplements(ctx.classImplements())
            if ctx.classImplements()
            else None
        )
        constants = (
            self.visitEnumConstants(ctx.enumConstants())
            if ctx.enumConstants()
            else None
        )
        body = (
            self.visitEnumBodyDeclarations(ctx.enumBodyDeclarations())
            if ctx.enumBodyDeclarations()
            else None
        )
        return jast.Enum(
            id=identifier,
            implements=implements,
            constants=constants,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitEnumConstants(
        self, ctx: JavaParser.EnumConstantsContext
    ) -> List[jast.enumconstant]:
        return [
            self.visitEnumConstant(enum_constant)
            for enum_constant in ctx.enumConstant()
        ]

    def visitEnumConstant(
        self, ctx: JavaParser.EnumConstantContext
    ) -> jast.enumconstant:
        annotations = [
            self.visitAnnotation(annotation) for annotation in ctx.annotation()
        ]
        identifier = self.visitIdentifier(ctx.identifier())
        arguments = self.visitArguments(ctx.arguments()) if ctx.arguments() else None
        body = self.visitClassBody(ctx.classBody()) if ctx.classBody() else None
        return jast.enumconstant(
            annotations=annotations,
            id=identifier,
            args=arguments,
            body=body,
        )

    def visitEnumBodyDeclarations(
        self, ctx: JavaParser.EnumBodyDeclarationsContext
    ) -> List[jast.declaration]:
        return [
            self.visitClassBodyDeclaration(class_body_declaration)
            for class_body_declaration in ctx.classBodyDeclaration()
        ]

    def visitInterfaceDeclaration(
        self, ctx: JavaParser.InterfaceDeclarationContext
    ) -> jast.Interface:
        identifier = self.visitIdentifier(ctx.identifier())
        type_parameters = (
            self.visitTypeParameters(ctx.typeParameters())
            if ctx.typeParameters()
            else None
        )
        extends = (
            self.visitClassExtends(ctx.classExtends()) if ctx.classExtends() else None
        )
        implements = (
            self.visitClassImplements(ctx.classImplements())
            if ctx.classImplements()
            else None
        )
        body = self.visitInterfaceBody(ctx.interfaceBody())
        return jast.Interface(
            id=identifier,
            type_params=type_parameters,
            extends=extends,
            implements=implements,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitClassBody(
        self, ctx: JavaParser.ClassBodyContext
    ) -> List[jast.declaration]:
        return [
            self.visitClassBodyDeclaration(class_body_declaration)
            for class_body_declaration in ctx.classBodyDeclaration()
        ]

    def visitInterfaceBody(
        self, ctx: JavaParser.InterfaceBodyContext
    ) -> List[jast.declaration]:
        return [
            self.visitInterfaceBodyDeclaration(interface_body_declaration)
            for interface_body_declaration in ctx.interfaceBodyDeclaration()
        ]

    def visitClassBodyDeclaration(
        self, ctx: JavaParser.ClassBodyDeclarationContext
    ) -> jast.declaration:
        if ctx.SEMI():
            return jast.EmptyDecl(**self._get_location_rule(ctx))
        elif ctx.block():
            return jast.Initializer(
                body=self.visitBlock(ctx.block()),
                static=ctx.STATIC() is not None,
                **self._get_location_rule(ctx),
            )

        else:
            declaration = self.visitMemberDeclaration(ctx.memberDeclaration())
            modifiers = [self.visitModifier(modifier) for modifier in ctx.modifier()]
            setattr(declaration, "modifiers", modifiers)
            self._set_location_rule(declaration, ctx)
            return declaration

    def visitMemberDeclaration(
        self, ctx: JavaParser.MemberDeclarationContext
    ) -> jast.declaration:
        if ctx.recordDeclaration():
            return self.visitRecordDeclaration(ctx.recordDeclaration())
        elif ctx.methodDeclaration():
            return self.visitMethodDeclaration(ctx.methodDeclaration())
        elif ctx.fieldDeclaration():
            return self.visitFieldDeclaration(ctx.fieldDeclaration())
        elif ctx.constructorDeclaration():
            return self.visitConstructorDeclaration(ctx.constructorDeclaration())
        elif ctx.interfaceDeclaration():
            return self.visitInterfaceDeclaration(ctx.interfaceDeclaration())
        elif ctx.annotationTypeDeclaration():
            return self.visitAnnotationTypeDeclaration(ctx.annotationTypeDeclaration())
        elif ctx.classDeclaration():
            return self.visitClassDeclaration(ctx.classDeclaration())
        else:
            return self.visitEnumDeclaration(ctx.enumDeclaration())

    def visitMethodDeclaration(
        self, ctx: JavaParser.MethodDeclarationContext
    ) -> jast.Method:
        type_parameters = (
            self.visitTypeParameters(ctx.typeParameters())
            if ctx.typeParameters()
            else None
        )
        return_type = self.visitTypeTypeOrVoid(ctx.typeTypeOrVoid())
        identifier = self.visitIdentifier(ctx.identifier())
        parameters = self.visitFormalParameters(ctx.formalParameters())
        dims = self.visitDims(ctx.dims()) if ctx.dims() else None
        throws = self.visitThrows_(ctx.throws_()) if ctx.throws_() else None
        body = self.visitMethodBody(ctx.methodBody())
        return jast.Method(
            type_params=type_parameters,
            return_type=return_type,
            id=identifier,
            parameters=parameters,
            dims=dims,
            throws=throws,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitDims(self, ctx: JavaParser.DimsContext) -> List[jast.dim]:
        return [self.visitDim(dim) for dim in ctx.dim()]

    def visitDim(self, ctx: JavaParser.DimContext) -> jast.dim:
        return jast.dim(
            annotations=[
                self.visitAnnotation(annotation) for annotation in ctx.annotation()
            ],
        )

    def visitThrows_(self, ctx: JavaParser.Throws_Context) -> List[jast.qname]:
        return self.visitQualifiedNameList(ctx.qualifiedNameList())

    def visitMethodBody(
        self, ctx: JavaParser.MethodBodyContext
    ) -> Optional[jast.Block]:
        if ctx.SEMI():
            return None
        else:
            return self.visitBlock(ctx.block())

    def visitTypeTypeOrVoid(self, ctx: JavaParser.TypeTypeOrVoidContext) -> jast.jtype:
        if ctx.VOID():
            return jast.Void()
        else:
            return self.visitTypeType(ctx.typeType())

    def visitConstructorDeclaration(
        self, ctx: JavaParser.ConstructorDeclarationContext
    ) -> jast.Constructor:
        type_parameters = (
            self.visitTypeParameters(ctx.typeParameters())
            if ctx.typeParameters()
            else None
        )
        identifier = self.visitIdentifier(ctx.identifier())
        parameters = self.visitFormalParameters(ctx.formalParameters())
        throws = self.visitThrows_(ctx.throws_()) if ctx.throws_() else None
        body = self.visitBlock(ctx.constructorBody)
        return jast.Constructor(
            type_params=type_parameters,
            id=identifier,
            parameters=parameters,
            throws=throws,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitCompactConstructorDeclaration(
        self, ctx: JavaParser.CompactConstructorDeclarationContext
    ) -> jast.Constructor:
        modifiers = [self.visitModifier(modifier) for modifier in ctx.modifier()]
        identifier = self.visitIdentifier(ctx.identifier())
        body = self.visitBlock(ctx.constructorBody)
        return jast.Constructor(
            modifiers=modifiers,
            id=identifier,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitFieldDeclaration(
        self, ctx: JavaParser.FieldDeclarationContext
    ) -> jast.Field:
        type_ = self.visitTypeType(ctx.typeType())
        declarators = self.visitVariableDeclarators(ctx.variableDeclarators())
        return jast.Field(
            type=type_,
            declarators=declarators,
            **self._get_location_rule(ctx),
        )

    def visitInterfaceBodyDeclaration(
        self, ctx: JavaParser.InterfaceBodyDeclarationContext
    ) -> jast.declaration:
        if ctx.SEMI():
            return jast.EmptyDecl(**self._get_location_rule(ctx))
        else:
            declaration = self.visitInterfaceMemberDeclaration(
                ctx.interfaceMemberDeclaration()
            )
            modifiers = [self.visitModifier(modifier) for modifier in ctx.modifier()]
            setattr(declaration, "modifiers", modifiers)
            self._set_location_rule(declaration, ctx)
            return declaration

    def visitInterfaceMemberDeclaration(
        self, ctx: JavaParser.InterfaceMemberDeclarationContext
    ) -> jast.declaration:
        if ctx.recordDeclaration():
            return self.visitRecordDeclaration(ctx.recordDeclaration())
        elif ctx.constDeclaration():
            return self.visitConstDeclaration(ctx.constDeclaration())
        elif ctx.interfaceMethodDeclaration():
            return self.visitInterfaceMethodDeclaration(
                ctx.interfaceMethodDeclaration()
            )
        elif ctx.interfaceDeclaration():
            return self.visitInterfaceDeclaration(ctx.interfaceDeclaration())
        elif ctx.annotationTypeDeclaration():
            return self.visitAnnotationTypeDeclaration(ctx.annotationTypeDeclaration())
        elif ctx.classDeclaration():
            return self.visitClassDeclaration(ctx.classDeclaration())
        else:
            return self.visitEnumDeclaration(ctx.enumDeclaration())

    def visitConstDeclaration(
        self, ctx: JavaParser.ConstDeclarationContext
    ) -> jast.Field:
        type_ = self.visitTypeType(ctx.typeType())
        declarators = self.visitVariableDeclarators(ctx.variableDeclarators())
        return jast.Field(
            type=type_,
            declarators=declarators,
            **self._get_location_rule(ctx),
        )

    def visitInterfaceMethodModifier(
        self, ctx: JavaParser.InterfaceMethodModifierContext
    ) -> jast.modifier:
        if ctx.PUBLIC():
            return jast.Public()
        elif ctx.ABSTRACT():
            return jast.Abstract()
        elif ctx.DEFAULT():
            return jast.Default()
        elif ctx.STATIC():
            return jast.Static()
        elif ctx.STRICTFP():
            return jast.Strictfp()
        else:
            return self.visitAnnotation(ctx.annotation())

    def visitInterfaceMethodDeclaration(
        self, ctx: JavaParser.InterfaceMethodDeclarationContext
    ) -> jast.Method:
        modifiers = [
            self.visitInterfaceMethodModifier(modifier)
            for modifier in ctx.interfaceMethodModifier()
        ]
        type_parameters = (
            self.visitTypeParameters(ctx.typeParameters())
            if ctx.typeParameters()
            else None
        )
        annotations = [
            self.visitAnnotation(annotation) for annotation in ctx.annotation()
        ]
        return_type = self.visitTypeTypeOrVoid(ctx.typeTypeOrVoid())
        identifier = self.visitIdentifier(ctx.identifier())
        parameters = self.visitFormalParameters(ctx.formalParameters())
        dims = self.visitDims(ctx.dims()) if ctx.dims() else None
        throws = self.visitThrows_(ctx.throws_()) if ctx.throws_() else None
        body = self.visitMethodBody(ctx.methodBody())
        return jast.Method(
            modifiers=modifiers,
            type_params=type_parameters,
            annotations=annotations,
            return_type=return_type,
            id=identifier,
            parameters=parameters,
            dims=dims,
            throws=throws,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitVariableDeclarators(
        self, ctx: JavaParser.VariableDeclaratorsContext
    ) -> List[jast.declarator]:
        return [
            self.visitVariableDeclarator(variable_declarator)
            for variable_declarator in ctx.variableDeclarator()
        ]

    def visitVariableDeclarator(
        self, ctx: JavaParser.VariableDeclaratorContext
    ) -> jast.declarator:
        identifier = self.visitVariableDeclaratorId(ctx.variableDeclaratorId())
        initializer = (
            self.visitVariableInitializer(ctx.variableInitializer())
            if ctx.variableInitializer()
            else None
        )
        return jast.declarator(
            id=identifier,
            init=initializer,
        )

    def visitVariableDeclaratorId(
        self, ctx: JavaParser.VariableDeclaratorIdContext
    ) -> jast.variabledeclaratorid:
        identifier = self.visitIdentifier(ctx.identifier())
        dims = self.visitDims(ctx.dims()) if ctx.dims() else None
        return jast.variabledeclaratorid(id=identifier, dims=dims)

    def visitVariableInitializer(
        self, ctx: JavaParser.VariableInitializerContext
    ) -> jast.expr | jast.arrayinit:
        if ctx.expression():
            return self.visitExpression(ctx.expression())
        else:
            return self.visitArrayInitializer(ctx.arrayInitializer())

    def visitArrayInitializer(
        self, ctx: JavaParser.ArrayInitializerContext
    ) -> jast.arrayinit:
        return jast.arrayinit(
            values=[
                self.visitVariableInitializer(variable_initializer)
                for variable_initializer in ctx.variableInitializer()
            ],
        )

    def visitClassOrInterfaceType(self, ctx: JavaParser.ClassOrInterfaceTypeContext):
        coits = [self.visitCoit(coit) for coit in ctx.coit()]
        if len(coits) == 1:
            return coits[0]
        return jast.ClassType(coits=coits)

    def visitCoit(self, ctx: JavaParser.CoitContext):
        identifier = self.visitTypeIdentifier(ctx.typeIdentifier())
        type_arguments = (
            self.visitTypeArguments(ctx.typeArguments())
            if ctx.typeArguments()
            else None
        )
        return jast.Coit(
            id=identifier,
            type_args=type_arguments,
        )

    def visitTypeArgument(self, ctx: JavaParser.TypeArgumentContext) -> jast.jtype:
        if ctx.QUESTION():
            annotations = [
                self.visitAnnotation(annotation) for annotation in ctx.annotation()
            ]
            if ctx.typeType():
                bound = jast.wildcardbound(
                    type=self.visitTypeType(ctx.typeType()),
                    extends=ctx.EXTENDS() is not None,
                    super_=ctx.SUPER() is not None,
                )
            else:
                bound = None
            return jast.Wildcard(
                annotations=annotations,
                bound=bound,
            )
        else:
            return self.visitTypeType(ctx.typeType())

    def visitQualifiedNameList(
        self, ctx: JavaParser.QualifiedNameListContext
    ) -> List[jast.qname]:
        return [
            self.visitQualifiedName(qualified_name)
            for qualified_name in ctx.qualifiedName()
        ]

    def visitFormalParameters(
        self, ctx: JavaParser.FormalParametersContext
    ) -> jast.params:
        receiver_parameter = (
            self.visitReceiverParameter(ctx.receiverParameter())
            if ctx.receiverParameter()
            else None
        )
        parameters = (
            self.visitFormalParameterList(ctx.formalParameterList())
            if ctx.formalParameterList()
            else None
        )
        return jast.params(
            receiver_param=receiver_parameter,
            parameters=parameters,
        )

    def visitReceiverParameter(
        self, ctx: JavaParser.ReceiverParameterContext
    ) -> jast.receiver:
        type_ = self.visitTypeType(ctx.typeType())
        identifiers = [
            self.visitIdentifier(identifier) for identifier in ctx.identifier()
        ]
        return jast.receiver(
            type=type_,
            identifiers=identifiers,
        )

    def visitFormalParameterList(
        self, ctx: JavaParser.FormalParameterListContext
    ) -> List[jast.param | jast.arity]:
        return [
            self.visitFormalParameter(formal_parameter)
            for formal_parameter in ctx.formalParameter()
        ] + (
            [self.visitLastFormalParameter(ctx.lastFormalParameter())]
            if ctx.lastFormalParameter()
            else []
        )

    def visitFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        modifiers = [
            self.visitVariableModifier(modifier) for modifier in ctx.variableModifier()
        ]
        type_ = self.visitTypeType(ctx.typeType())
        identifier = self.visitVariableDeclaratorId(ctx.variableDeclaratorId())
        return jast.param(
            modifiers=modifiers,
            type=type_,
            id=identifier,
        )

    def visitLastFormalParameter(
        self, ctx: JavaParser.LastFormalParameterContext
    ) -> jast.arity:
        modifiers = [
            self.visitVariableModifier(modifier) for modifier in ctx.variableModifier()
        ]
        type_ = self.visitTypeType(ctx.typeType())
        annotations = [
            self.visitAnnotation(annotation) for annotation in ctx.annotation()
        ]
        identifier = self.visitVariableDeclaratorId(ctx.variableDeclaratorId())
        return jast.arity(
            modifiers=modifiers,
            type=type_,
            annotations=annotations,
            id=identifier,
        )

    def visitLambdaLVTIList(self, ctx: JavaParser.LambdaLVTIListContext):
        return [
            self.visitLambdaLVTIParameter(lvti) for lvti in ctx.lambdaLVTIParameter()
        ]

    def visitLambdaLVTIParameter(
        self, ctx: JavaParser.LambdaLVTIParameterContext
    ) -> jast.param:
        modifiers = [
            self.visitVariableModifier(modifier) for modifier in ctx.variableModifier()
        ]
        type_ = jast.Var()
        identifier = jast.variabledeclaratorid(
            id=self.visitIdentifier(ctx.identifier()),
        )
        return jast.param(
            modifiers=modifiers,
            type=type_,
            id=identifier,
        )

    def visitQualifiedName(self, ctx: JavaParser.QualifiedNameContext) -> jast.qname:
        return jast.qname(
            identifiers=[
                self.visitIdentifier(identifier) for identifier in ctx.identifier()
            ]
        )

    def visitLiteral(self, ctx: JavaParser.LiteralContext) -> jast.literal:
        if ctx.integerLiteral():
            return self.visitIntegerLiteral(ctx.integerLiteral())
        elif ctx.floatLiteral():
            return self.visitFloatLiteral(ctx.floatLiteral())
        elif ctx.CHAR_LITERAL():
            return jast.CharLiteral(value=ctx.getText()[1:-1])
        elif ctx.STRING_LITERAL():
            return jast.StringLiteral(value=ctx.getText()[1:-1])
        elif ctx.BOOL_LITERAL():
            return jast.BoolLiteral(value=ctx.getText() == "true")
        elif ctx.NULL_LITERAL():
            return jast.NullLiteral()
        else:
            text = ctx.getText()[3:-3]
            lines = text.split("\n")[1:]
            min_spaces = min(
                len(line) - len(line.lstrip()) for line in lines if line.strip()
            )
            return jast.TextBlock(
                value=[
                    line[min_spaces:] if line.strip() else line.strip()
                    for line in lines
                ]
            )

    def visitIntegerLiteral(
        self, ctx: JavaParser.IntegerLiteralContext
    ) -> jast.IntLiteral:
        text = ctx.getText()
        long = "l" in text or "L" in text
        text = text.replace("l", "").replace("L", "")
        if ctx.OCT_LITERAL():
            text = text[1:]
            while text.startswith("_"):
                text = text[1:]
            text = "0o" + text
        return jast.IntLiteral(
            value=eval(text),
            long=long,
        )

    def visitFloatLiteral(
        self, ctx: JavaParser.FloatLiteralContext
    ) -> jast.FloatLiteral:
        text = ctx.getText()
        double = "d" in text or "D" in text
        text = text.replace("d", "").replace("D", "").replace("f", "").replace("F", "")
        if ctx.FLOAT_LITERAL():
            value = float(text)
        else:
            value = float.fromhex(text)
        return jast.FloatLiteral(
            value=value,
            double=double,
        )

    def visitAnnotation(self, ctx: JavaParser.AnnotationContext) -> jast.Annotation:
        name = self.visitQualifiedName(ctx.qualifiedName())
        elements = (
            self.visitElementValuePairs(ctx.elementValuePairs())
            if ctx.elementValuePairs()
            else [self.visitElementValue(ctx.elementValue())]
            if ctx.elementValue()
            else None
        )
        return jast.Annotation(
            name=name,
            elements=elements,
        )

    def visitElementValuePairs(
        self, ctx: JavaParser.ElementValuePairsContext
    ) -> List[jast.elementvaluepair]:
        return [
            self.visitElementValuePair(elementValuePair)
            for elementValuePair in ctx.elementValuePair()
        ]

    def visitElementValuePair(
        self, ctx: JavaParser.ElementValuePairContext
    ) -> jast.elementvaluepair:
        name = self.visitIdentifier(ctx.identifier())
        value = self.visitElementValue(ctx.elementValue())
        return jast.elementvaluepair(
            id=name,
            value=value,
        )

    def visitElementValue(
        self, ctx: JavaParser.ElementValueContext
    ) -> jast.expr | jast.Annotation | jast.elementarrayinit:
        if ctx.expression():
            return self.visitExpression(ctx.expression())
        elif ctx.annotation():
            return self.visitAnnotation(ctx.annotation())
        else:
            return self.visitElementValueArrayInitializer(
                ctx.elementValueArrayInitializer()
            )

    def visitElementValueArrayInitializer(
        self, ctx: JavaParser.ElementValueArrayInitializerContext
    ) -> jast.elementarrayinit:
        return jast.elementarrayinit(
            values=[
                self.visitElementValue(elementValue)
                for elementValue in ctx.elementValue()
            ],
        )

    def visitAnnotationTypeDeclaration(
        self, ctx: JavaParser.AnnotationTypeDeclarationContext
    ) -> jast.AnnotationDecl:
        identifier = self.visitIdentifier(ctx.identifier())
        body = self.visitAnnotationTypeBody(ctx.annotationTypeBody())
        return jast.AnnotationDecl(
            id=identifier,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitAnnotationTypeBody(
        self, ctx: JavaParser.AnnotationTypeBodyContext
    ) -> List[jast.declaration]:
        return [
            self.visitAnnotationTypeElementDeclaration(annotationTypeElementDeclaration)
            for annotationTypeElementDeclaration in ctx.annotationTypeElementDeclaration()
        ]

    def visitAnnotationTypeElementDeclaration(
        self, ctx: JavaParser.AnnotationTypeElementDeclarationContext
    ) -> jast.declaration:
        if ctx.SEMI():
            return jast.EmptyDecl(**self._get_location_rule(ctx))
        else:
            declaration = self.visitAnnotationTypeElementRest(
                ctx.annotationTypeElementRest()
            )
            modifiers = [self.visitModifier(modifier) for modifier in ctx.modifier()]
            setattr(declaration, "modifiers", modifiers)
            self._set_location_rule(declaration, ctx)
            return declaration

    def visitAnnotationTypeElementRest(
        self, ctx: JavaParser.AnnotationTypeElementRestContext
    ) -> jast.declaration:
        if ctx.annotationConstantDeclaration():
            return self.visitAnnotationConstantDeclaration(
                ctx.annotationConstantDeclaration()
            )
        elif ctx.annotationMethodDeclaration():
            return self.visitAnnotationMethodDeclaration(
                ctx.annotationMethodDeclaration()
            )
        elif ctx.classDeclaration():
            return self.visitClassDeclaration(ctx.classDeclaration())
        elif ctx.interfaceDeclaration():
            return self.visitInterfaceDeclaration(ctx.interfaceDeclaration())
        elif ctx.enumDeclaration():
            return self.visitEnumDeclaration(ctx.enumDeclaration())
        elif ctx.annotationTypeDeclaration():
            return self.visitAnnotationTypeDeclaration(ctx.annotationTypeDeclaration())
        else:
            return self.visitRecordDeclaration(ctx.recordDeclaration())

    def visitAnnotationConstantDeclaration(
        self, ctx: JavaParser.AnnotationConstantDeclarationContext
    ) -> jast.Field:
        type_ = self.visitTypeType(ctx.typeType())
        declarators = self.visitVariableDeclarators(ctx.variableDeclarators())
        return jast.Field(
            type=type_,
            declarators=declarators,
            **self._get_location_rule(ctx),
        )

    def visitAnnotationMethodDeclaration(
        self, ctx: JavaParser.AnnotationMethodDeclarationContext
    ) -> jast.AnnotationMethod:
        type_ = self.visitTypeType(ctx.typeType())
        identifier = self.visitIdentifier(ctx.identifier())
        default = (
            self.visitDefaultValue(ctx.defaultValue()) if ctx.defaultValue() else None
        )
        return jast.AnnotationMethod(
            type=type_,
            id=identifier,
            default=default,
            **self._get_location_rule(ctx),
        )

    def visitDefaultValue(
        self, ctx: JavaParser.DefaultValueContext
    ) -> jast.expr | jast.Annotation | jast.elementarrayinit:
        return self.visitElementValue(ctx.elementValue())

    def visitModuleDeclaration(self, ctx: JavaParser.ModuleDeclarationContext):
        open_ = ctx.OPEN() is not None
        name = self.visitQualifiedName(ctx.qualifiedName())
        directives = self.visitModuleBody(ctx.moduleBody())
        return jast.Module(
            open=open_,
            name=name,
            body=directives,
            **self._get_location_rule(ctx),
        )

    def visitModuleBody(
        self, ctx: JavaParser.ModuleBodyContext
    ) -> List[jast.directive]:
        return [
            self.visitModuleDirective(moduleDirective)
            for moduleDirective in ctx.moduleDirective()
        ]

    def visitModuleDirective(
        self, ctx: JavaParser.ModuleDirectiveContext
    ) -> jast.directive:
        name = self.visitQualifiedName(ctx.qualifiedName(0))
        if ctx.REQUIRES():
            modifiers = [
                self.visitRequiresModifier(modifier)
                for modifier in ctx.requiresModifier()
            ]
            return jast.Requires(
                modifiers=modifiers,
                name=name,
                **self._get_location_rule(ctx),
            )
        elif ctx.EXPORTS():
            to = self.visitQualifiedName(ctx.qualifiedName(1)) if ctx.TO() else None
            return jast.Exports(
                name=name,
                to=to,
                **self._get_location_rule(ctx),
            )
        elif ctx.OPENS():
            to = self.visitQualifiedName(ctx.qualifiedName(1)) if ctx.TO() else None
            return jast.Opens(
                name=name,
                to=to,
                **self._get_location_rule(ctx),
            )
        elif ctx.USES():
            return jast.Uses(
                name=name,
                **self._get_location_rule(ctx),
            )
        else:
            return jast.Provides(
                name=name,
                with_=self.visitQualifiedName(ctx.qualifiedName(1)),
                **self._get_location_rule(ctx),
            )

    def visitRequiresModifier(
        self, ctx: JavaParser.RequiresModifierContext
    ) -> jast.modifier:
        if ctx.TRANSITIVE():
            return jast.Transitive()
        else:
            return jast.Static()

    def visitRecordDeclaration(
        self, ctx: JavaParser.RecordDeclarationContext
    ) -> jast.Record:
        identifier = self.visitIdentifier(ctx.identifier())
        type_parameters = (
            self.visitTypeParameters(ctx.typeParameters())
            if ctx.typeParameters()
            else None
        )
        components = (
            self.visitRecordComponentList(ctx.recordComponentList())
            if ctx.recordComponentList()
            else None
        )
        implements = (
            self.visitClassImplements(ctx.classImplements())
            if ctx.classImplements()
            else None
        )
        body = self.visitRecordBody(ctx.recordBody())
        return jast.Record(
            id=identifier,
            type_params=type_parameters,
            components=components,
            implements=implements,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitRecordComponentList(
        self, ctx: JavaParser.RecordComponentListContext
    ) -> List[jast.recordcomponent]:
        return [
            self.visitRecordComponent(recordComponent)
            for recordComponent in ctx.recordComponent()
        ]

    def visitRecordComponent(
        self, ctx: JavaParser.RecordComponentContext
    ) -> jast.recordcomponent:
        type_ = self.visitTypeType(ctx.typeType())
        identifier = self.visitIdentifier(ctx.identifier())
        return jast.recordcomponent(
            type=type_,
            id=identifier,
        )

    def visitRecordBody(
        self, ctx: JavaParser.RecordBodyContext
    ) -> List[jast.declaration]:
        return [
            self.visitRecordBodyDeclaration(recordBodyDeclaration)
            for recordBodyDeclaration in ctx.recordBodyDeclaration()
        ]

    def visitRecordBodyDeclaration(
        self, ctx: JavaParser.RecordBodyDeclarationContext
    ) -> jast.declaration:
        if ctx.classBodyDeclaration():
            return self.visitClassBodyDeclaration(ctx.classBodyDeclaration())
        else:
            return self.visitCompactConstructorDeclaration(
                ctx.compactConstructorDeclaration()
            )

    def visitBlock(self, ctx: JavaParser.BlockContext) -> jast.Block:
        return jast.Block(
            body=[
                self.visitBlockStatement(blockStatement)
                for blockStatement in ctx.blockStatement()
            ],
            **self._get_location_rule(ctx),
        )

    def visitBlockStatement(self, ctx: JavaParser.BlockStatementContext) -> jast.stmt:
        if ctx.localVariableDeclaration():
            return self.visitLocalVariableDeclaration(ctx.localVariableDeclaration())
        elif ctx.localTypeDeclaration():
            return self.visitLocalTypeDeclaration(ctx.localTypeDeclaration())
        else:
            return self.visitStatement(ctx.statement())

    def visitLocalVariableDeclaration(
        self, ctx: JavaParser.LocalVariableDeclarationContext
    ) -> jast.LocalVariable:
        modifiers = [
            self.visitVariableModifier(modifier) for modifier in ctx.variableModifier()
        ]
        if ctx.VAR():
            type_ = jast.Var()
            declarators = [
                jast.declarator(
                    id=jast.variabledeclaratorid(
                        id=self.visitIdentifier(ctx.identifier()),
                    ),
                    init=self.visitExpression(ctx.expression()),
                )
            ]
        else:
            type_ = self.visitTypeType(ctx.typeType())
            declarators = self.visitVariableDeclarators(ctx.variableDeclarators())
        return jast.LocalVariable(
            modifiers=modifiers,
            type=type_,
            declarators=declarators,
            **self._get_location_rule(ctx),
        )

    def visitIdentifier(self, ctx: JavaParser.IdentifierContext) -> jast.identifier:
        return jast.identifier(ctx.getText())

    def visitTypeIdentifier(
        self, ctx: JavaParser.TypeIdentifierContext
    ) -> jast.identifier:
        return jast.identifier(ctx.getText())

    def visitLocalTypeDeclaration(
        self, ctx: JavaParser.LocalTypeDeclarationContext
    ) -> jast.declaration:
        modifiers = [
            self.visitClassOrInterfaceModifier(modifier)
            for modifier in ctx.classOrInterfaceModifier()
        ]
        if ctx.classDeclaration():
            declaration = self.visitClassDeclaration(ctx.classDeclaration())
        elif ctx.interfaceDeclaration():
            declaration = self.visitInterfaceDeclaration(ctx.interfaceDeclaration())
        else:
            declaration = self.visitRecordDeclaration(ctx.recordDeclaration())
        setattr(declaration, "modifiers", modifiers)
        self._set_location_rule(declaration, ctx)
        return jast.LocalType(
            decl=declaration,
            **self._get_location_rule(ctx),
        )

    def visitStatement(self, ctx: JavaParser.StatementContext) -> jast.stmt:
        if ctx.blockLabel:
            return self.visitBlock(ctx.blockLabel)
        elif ctx.ASSERT():
            return jast.Assert(
                test=self.visitExpression(ctx.expression(0)),
                msg=self.visitExpression(ctx.expression(1)) if ctx.COLON() else None,
                **self._get_location_rule(ctx),
            )
        elif ctx.IF():
            return jast.If(
                test=self.visitParExpr(ctx.parExpression()),
                body=self.visitStatement(ctx.statement(0)),
                orelse=self.visitStatement(ctx.statement(1)) if ctx.ELSE() else None,
                **self._get_location_rule(ctx),
            )
        elif ctx.FOR():
            if ctx.COLON():
                return jast.ForEach(
                    modifiers=[
                        self.visitVariableModifier(modifier)
                        for modifier in ctx.variableModifier()
                    ],
                    type=jast.Var()
                    if ctx.VAR()
                    else self.visitTypeType(ctx.typeType()),
                    id=self.visitVariableDeclaratorId(ctx.variableDeclaratorId()),
                    iter=self.visitExpression(ctx.expression(0)),
                    body=self.visitStatement(ctx.statement(0)),
                    **self._get_location_rule(ctx),
                )
            else:
                return jast.For(
                    init=self.visitForInit(ctx.forInit()) if ctx.forInit() else None,
                    test=self.visitExpression(ctx.expression(0))
                    if ctx.expression()
                    else None,
                    update=self.visitExpressionList(ctx.forUpdate)
                    if ctx.forUpdate
                    else None,
                    body=self.visitStatement(ctx.statement(0)),
                    **self._get_location_rule(ctx),
                )
        elif ctx.DO():
            return jast.DoWhile(
                body=self.visitStatement(ctx.statement(0)),
                test=self.visitParExpression(ctx.parExpression()),
                **self._get_location_rule(ctx),
            )
        elif ctx.WHILE():
            return jast.While(
                test=self.visitParExpr(ctx.parExpression()),
                body=self.visitStatement(ctx.statement(0)),
                **self._get_location_rule(ctx),
            )
        elif ctx.TRY():
            if ctx.resourceSpecification():
                return jast.TryWithResources(
                    resources=self.visitResourceSpecification(
                        ctx.resourceSpecification()
                    ),
                    body=self.visitBlock(ctx.block()),
                    catches=[
                        self.visitCatchClause(catchClause)
                        for catchClause in ctx.catchClause()
                    ],
                    final=self.visitFinallyBlock(ctx.finallyBlock())
                    if ctx.finallyBlock()
                    else None,
                    **self._get_location_rule(ctx),
                )
            else:
                return jast.Try(
                    body=self.visitBlock(ctx.block()),
                    catches=[
                        self.visitCatchClause(catchClause)
                        for catchClause in ctx.catchClause()
                    ],
                    final=self.visitFinallyBlock(ctx.finallyBlock())
                    if ctx.finallyBlock()
                    else None,
                    **self._get_location_rule(ctx),
                )
        elif ctx.SWITCH():
            return jast.Switch(
                value=self.visitParExpression(ctx.parExpression()),
                body=self.visitSwitchBlock(ctx.switchBlock()),
                **self._get_location_rule(ctx),
            )
        elif ctx.SYNCHRONIZED():
            return jast.Synch(
                lock=self.visitParExpression(ctx.parExpression()),
                body=self.visitBlock(ctx.block()),
                **self._get_location_rule(ctx),
            )
        elif ctx.RETURN():
            return jast.Return(
                value=self.visitExpression(ctx.expression(0))
                if ctx.expression()
                else None,
                **self._get_location_rule(ctx),
            )
        elif ctx.THROW():
            return jast.Throw(
                exc=self.visitExpression(ctx.expression(0)),
                **self._get_location_rule(ctx),
            )
        elif ctx.BREAK():
            return jast.Break(
                label=self.visitIdentifier(ctx.identifier())
                if ctx.identifier()
                else None,
                **self._get_location_rule(ctx),
            )
        elif ctx.CONTINUE():
            return jast.Continue(
                label=self.visitIdentifier(ctx.identifier())
                if ctx.identifier()
                else None,
                **self._get_location_rule(ctx),
            )
        elif ctx.YIELD():
            return jast.Yield(
                value=self.visitExpression(ctx.expression(0)),
                **self._get_location_rule(ctx),
            )
        elif ctx.statementExpression:
            return jast.Expression(
                value=self.visitExpression(ctx.statementExpression),
                **self._get_location_rule(ctx),
            )
        elif ctx.identifierLabel:
            return jast.Labeled(
                label=self.visitIdentifier(ctx.identifierLabel),
                body=self.visitStatement(ctx.statement(0)),
                **self._get_location_rule(ctx),
            )
        else:
            return jast.Empty(**self._get_location_rule(ctx))

    def visitSwitchBlock(self, ctx: JavaParser.SwitchBlockContext) -> jast.switchblock:
        return jast.switchblock(
            groups=[
                self.visitSwitchBlockStatementGroup(switchBlockStatementGroup)
                for switchBlockStatementGroup in ctx.switchBlockStatementGroup()
            ],
            labels=[self.visitSwitchLabel(label) for label in ctx.switchLabel()],
        )

    def visitCatchClause(self, ctx: JavaParser.CatchClauseContext) -> jast.catch:
        modifiers = [
            self.visitVariableModifier(modifier) for modifier in ctx.variableModifier()
        ]
        type_ = self.visitCatchType(ctx.catchType())
        identifier = self.visitIdentifier(ctx.identifier())
        body = self.visitBlock(ctx.block())
        return jast.catch(
            modifiers=modifiers,
            excs=type_,
            id=identifier,
            body=body,
        )

    def visitCatchType(self, ctx: JavaParser.CatchTypeContext) -> List[jast.qname]:
        return [
            self.visitQualifiedName(qualifiedName)
            for qualifiedName in ctx.qualifiedName()
        ]

    def visitFinallyBlock(self, ctx: JavaParser.FinallyBlockContext) -> jast.Block:
        return self.visitBlock(ctx.block())

    def visitResourceSpecification(
        self, ctx: JavaParser.ResourceSpecificationContext
    ) -> List[jast.resource | jast.qname]:
        return self.visitResources(ctx.resources())

    def visitResources(
        self, ctx: JavaParser.ResourcesContext
    ) -> List[jast.resource | jast.qname]:
        return [self.visitResource(resource) for resource in ctx.resource()]

    def visitResource(self, ctx: JavaParser.ResourceContext) -> jast.resource:
        if ctx.qualifiedName():
            return self.visitQualifiedName(ctx.qualifiedName())
        else:
            modifiers = [
                self.visitVariableModifier(modifier)
                for modifier in ctx.variableModifier()
            ]
            if ctx.VAR():
                type_ = jast.Var()
                identifier = jast.variabledeclaratorid(
                    id=self.visitIdentifier(ctx.identifier()),
                )
            else:
                type_ = self.visitClassOrInterfaceType(ctx.classOrInterfaceType())
                identifier = self.visitVariableDeclaratorId(ctx.variableDeclaratorId())
            declarator = jast.declarator(
                id=identifier,
                init=self.visitExpression(ctx.expression()),
            )
            return jast.resource(
                modifiers=modifiers,
                type=type_,
                variable=declarator,
            )

    def visitSwitchBlockStatementGroup(
        self, ctx: JavaParser.SwitchBlockStatementGroupContext
    ) -> jast.switchgroup:
        return jast.switchgroup(
            labels=[
                self.visitSwitchLabel(switchLabel) for switchLabel in ctx.switchLabel()
            ],
            body=[
                self.visitBlockStatement(blockStatement)
                for blockStatement in ctx.blockStatement()
            ],
        )

    def visitSwitchLabel(self, ctx: JavaParser.SwitchLabelContext) -> jast.switchlabel:
        if ctx.DEFAULT():
            return jast.DefaultCase()
        else:
            if ctx.constantExpression:
                expression = self.visitExpression(ctx.constantExpression)
            elif ctx.enumConstantName:
                expression = jast.Name(
                    id=self.visitIdentifier(ctx.enumConstantName),
                    **self._get_location_rule(ctx.enumConstantName),
                )
            else:
                start = self._get_location_rule(ctx.typeType())
                end = self._get_location_rule(ctx.varName)
                expression = jast.Match(
                    type=self.visitTypeType(ctx.typeType()),
                    id=self.visitIdentifier(ctx.varName),
                    lineno=start["lineno"],
                    col_offset=start["col_offset"],
                    end_lineno=end["end_lineno"],
                    end_col_offset=end["end_col_offset"],
                )
            return jast.Case(
                guard=expression,
            )

    def visitForInit(
        self, ctx: JavaParser.ForInitContext
    ) -> jast.LocalVariable | List[jast.Expression]:
        if ctx.localVariableDeclaration():
            return self.visitLocalVariableDeclaration(ctx.localVariableDeclaration())
        else:
            return self.visitExpressionList(ctx.expressionList())

    def visitParExpr(self, ctx: JavaParser.ParExprContext) -> jast.expr:
        return self.visitExpression(ctx.expression())

    def visitExpressionList(
        self, ctx: JavaParser.ExpressionListContext
    ) -> List[jast.Expression]:
        return [self.visitExpression(expression) for expression in ctx.expression()]

    def visitMethodCall(self, ctx: JavaParser.MethodCallContext) -> jast.Call:
        if ctx.THIS():
            function = jast.This(**self._get_location_token(ctx.THIS()))
        elif ctx.SUPER():
            function = jast.Super(**self._get_location_token(ctx.SUPER()))
        else:
            function = jast.Name(
                id=self.visitIdentifier(ctx.identifier()),
                **self._get_location_rule(ctx.identifier()),
            )
        return jast.Call(
            func=function,
            args=self.visitArguments(ctx.arguments()),
            **self._get_location_rule(ctx),
        )

    def visitPostfixExpression(self, ctx: JavaParser.PostfixExpressionContext):
        if ctx.switchExpression():
            return self.visitSwitchExpression(ctx.switchExpression())
        else:
            if ctx.INC():
                op = jast.PostInc()
            else:
                op = jast.PostDec()
            return jast.PostOp(
                operand=self.visitPostfixExpression(ctx.postfixExpression()),
                op=op,
                **self._get_location_rule(ctx),
            )

    def visitPrefixExpression(self, ctx: JavaParser.PrefixExpressionContext):
        if ctx.postfixExpression():
            return self.visitPostfixExpression(ctx.postfixExpression())
        else:
            if ctx.ADD():
                op = jast.UAdd()
            elif ctx.SUB():
                op = jast.USub()
            elif ctx.INC():
                op = jast.PreInc()
            elif ctx.DEC():
                op = jast.PreDec()
            elif ctx.TILDE():
                op = jast.Invert()
            else:
                op = jast.Not()
            return jast.UnaryOp(
                operand=self.visitPrefixExpression(ctx.prefixExpression()),
                op=op,
                **self._get_location_rule(ctx),
            )

    def visitTypeExpression(self, ctx: JavaParser.TypeExpressionContext) -> jast.expr:
        if ctx.prefixExpression():
            return self.visitPrefixExpression(ctx.prefixExpression())
        elif ctx.NEW():
            return self.visitCreator(ctx.creator())
        else:
            return jast.Cast(
                annotations=[
                    self.visitAnnotation(annotation) for annotation in ctx.annotation()
                ],
                type=jast.typebound(
                    types=[self.visitTypeType(typeType) for typeType in ctx.typeType()],
                ),
                value=self.visitTypeExpression(ctx.typeExpression()),
                **self._get_location_rule(ctx),
            )

    def visitMultiplicativeExpression(
        self, ctx: JavaParser.MultiplicativeExpressionContext
    ) -> jast.expr:
        if ctx.bop:
            if ctx.MUL():
                op = jast.Mult()
            elif ctx.DIV():
                op = jast.Div()
            else:
                op = jast.Mod()
            return jast.BinOp(
                left=self.visitMultiplicativeExpression(ctx.multiplicativeExpression()),
                right=self.visitTypeExpression(ctx.typeExpression()),
                op=op,
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitTypeExpression(ctx.typeExpression())

    def visitAdditiveExpression(
        self, ctx: JavaParser.AdditiveExpressionContext
    ) -> jast.expr:
        if ctx.bop:
            if ctx.ADD():
                op = jast.Add()
            else:
                op = jast.Sub()
            return jast.BinOp(
                left=self.visitAdditiveExpression(ctx.additiveExpression()),
                right=self.visitMultiplicativeExpression(
                    ctx.multiplicativeExpression()
                ),
                op=op,
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitMultiplicativeExpression(ctx.multiplicativeExpression())

    def visitShiftExpression(self, ctx: JavaParser.ShiftExpressionContext) -> jast.expr:
        if ctx.shiftExpression():
            if ctx.LT():
                op = jast.LShift()
            elif len(ctx.GT()) == 2:
                op = jast.RShift()
            else:
                op = jast.URShift()
            return jast.BinOp(
                left=self.visitShiftExpression(ctx.shiftExpression()),
                right=self.visitAdditiveExpression(ctx.additiveExpression()),
                op=op,
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitAdditiveExpression(ctx.additiveExpression())

    def visitRelationalExpression(
        self, ctx: JavaParser.RelationalExpressionContext
    ) -> jast.expr:
        if ctx.bop:
            if ctx.INSTANCEOF():
                return jast.InstanceOf(
                    value=self.visitRelationalExpression(ctx.relationalExpression()),
                    type=self.visitTypeType(ctx.typeType())
                    if ctx.typeType()
                    else self.visitPattern(ctx.pattern()),
                    **self._get_location_rule(ctx),
                )
            else:
                if ctx.LT():
                    op = jast.Lt()
                elif ctx.GT():
                    op = jast.Gt()
                elif ctx.LE():
                    op = jast.LtE()
                else:
                    op = jast.GtE()
                return jast.BinOp(
                    left=self.visitRelationalExpression(ctx.relationalExpression()),
                    right=self.visitShiftExpression(ctx.shiftExpression()),
                    op=op,
                    **self._get_location_rule(ctx),
                )
        else:
            return self.visitShiftExpression(ctx.shiftExpression())

    def visitEqualityExpression(
        self, ctx: JavaParser.EqualityExpressionContext
    ) -> jast.expr:
        if ctx.bop:
            if ctx.EQUAL():
                op = jast.Eq()
            else:
                op = jast.NotEq()
            return jast.BinOp(
                left=self.visitEqualityExpression(ctx.equalityExpression()),
                right=self.visitRelationalExpression(ctx.relationalExpression()),
                op=op,
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitRelationalExpression(ctx.relationalExpression())

    def visitBitwiseAndExpression(
        self, ctx: JavaParser.BitwiseAndExpressionContext
    ) -> jast.expr:
        if ctx.BITAND():
            return jast.BinOp(
                left=self.visitBitwiseAndExpression(ctx.bitwiseAndExpression()),
                right=self.visitEqualityExpression(ctx.equalityExpression()),
                op=jast.BitAnd(),
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitEqualityExpression(ctx.equalityExpression())

    def visitBitwiseXorExpression(
        self, ctx: JavaParser.BitwiseXorExpressionContext
    ) -> jast.expr:
        if ctx.CARET():
            return jast.BinOp(
                left=self.visitBitwiseXorExpression(ctx.bitwiseXorExpression()),
                right=self.visitBitwiseAndExpression(ctx.bitwiseAndExpression()),
                op=jast.BitXor(),
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitBitwiseAndExpression(ctx.bitwiseAndExpression())

    def visitBitwiseOrExpression(
        self, ctx: JavaParser.BitwiseOrExpressionContext
    ) -> jast.expr:
        if ctx.BITOR():
            return jast.BinOp(
                left=self.visitBitwiseOrExpression(ctx.bitwiseOrExpression()),
                right=self.visitBitwiseXorExpression(ctx.bitwiseXorExpression()),
                op=jast.BitOr(),
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitBitwiseXorExpression(ctx.bitwiseXorExpression())

    def visitLogicalAndExpression(
        self, ctx: JavaParser.LogicalAndExpressionContext
    ) -> jast.expr:
        if ctx.AND():
            return jast.BinOp(
                left=self.visitLogicalAndExpression(ctx.logicalAndExpression()),
                right=self.visitBitwiseOrExpression(ctx.bitwiseOrExpression()),
                op=jast.And(),
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitBitwiseOrExpression(ctx.bitwiseOrExpression())

    def visitLogicalOrExpression(
        self, ctx: JavaParser.LogicalOrExpressionContext
    ) -> jast.expr:
        if ctx.OR():
            return jast.BinOp(
                left=self.visitLogicalOrExpression(ctx.logicalOrExpression()),
                right=self.visitLogicalAndExpression(ctx.logicalAndExpression()),
                op=jast.Or(),
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitLogicalAndExpression(ctx.logicalAndExpression())

    def visitTernaryExpression(
        self, ctx: JavaParser.TernaryExpressionContext
    ) -> jast.expr:
        if ctx.QUESTION():
            if ctx.ternaryExpression():
                orelse = self.visitTernaryExpression(ctx.ternaryExpression())
            else:
                orelse = self.visitLambdaExpression(ctx.lambdaExpression())
            return jast.IfExp(
                test=self.visitLogicalOrExpression(ctx.logicalOrExpression()),
                body=self.visitExpression(ctx.expression()),
                orelse=orelse,
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitLogicalOrExpression(ctx.logicalOrExpression())

    def visitAssignmentExpression(
        self, ctx: JavaParser.AssignmentExpressionContext
    ) -> jast.expr:
        if ctx.bop:
            if ctx.ASSIGN():
                op = None
            elif ctx.ADD_ASSIGN():
                op = jast.Add()
            elif ctx.SUB_ASSIGN():
                op = jast.Sub()
            elif ctx.MUL_ASSIGN():
                op = jast.Mult()
            elif ctx.DIV_ASSIGN():
                op = jast.Div()
            elif ctx.AND_ASSIGN():
                op = jast.BitAnd()
            elif ctx.OR_ASSIGN():
                op = jast.BitOr()
            elif ctx.XOR_ASSIGN():
                op = jast.BitXor()
            elif ctx.MOD_ASSIGN():
                op = jast.Mod()
            elif ctx.LSHIFT_ASSIGN():
                op = jast.LShift()
            elif ctx.RSHIFT_ASSIGN():
                op = jast.RShift()
            else:
                op = jast.URShift()
            return jast.Assign(
                target=self.visitTernaryExpression(ctx.ternaryExpression()),
                op=op,
                value=self.visitExpression(ctx.expression()),
                **self._get_location_rule(ctx),
            )
        else:
            return self.visitTernaryExpression(ctx.ternaryExpression())

    def visitExpression(self, ctx: JavaParser.ExpressionContext) -> jast.expr:
        if ctx.assignmentExpression():
            return self.visitAssignmentExpression(ctx.assignmentExpression())
        else:
            return self.visitLambdaExpression(ctx.lambdaExpression())

    def visitPattern(self, ctx: JavaParser.PatternContext) -> jast.pattern:
        return jast.pattern(
            modifiers=[
                self.visitVariableModifier(modifier)
                for modifier in ctx.variableModifier()
            ],
            type=self.visitTypeType(ctx.typeType()),
            annotations=[
                self.visitAnnotation(annotation) for annotation in ctx.annotation()
            ],
            id=self.visitIdentifier(ctx.identifier()),
        )

    def visitLambdaExpression(self, ctx: JavaParser.LambdaExpressionContext):
        parameters = self.visitLambdaParameters(ctx.lambdaParameters())
        body = self.visitLambdaBody(ctx.lambdaBody())
        return jast.Lambda(
            args=parameters,
            body=body,
            **self._get_location_rule(ctx),
        )

    def visitLambdaParameters(
        self, ctx: JavaParser.LambdaParametersContext
    ) -> jast.identifier | List[jast.identifier] | List[jast.param | jast.arity]:
        if ctx.LPAREN():
            if ctx.formalParameterList():
                return jast.params(
                    parameters=self.visitFormalParameterList(ctx.formalParameterList())
                )
            elif ctx.lambdaLVTIList():
                return jast.params(
                    parameters=self.visitLambdaLVTIList(ctx.lambdaLVTIList())
                )
            else:
                return [
                    self.visitIdentifier(identifier) for identifier in ctx.identifier()
                ]
        else:
            return self.visitIdentifier(ctx.identifier(0))

    def visitLambdaBody(
        self, ctx: JavaParser.LambdaBodyContext
    ) -> jast.expr | jast.Block:
        if ctx.expression():
            return self.visitExpression(ctx.expression())
        else:
            return self.visitBlock(ctx.block())

    def visitParExpression(self, ctx: JavaParser.ParExpressionContext) -> jast.expr:
        return self.visitExpression(ctx.expression())

    def visitThisExpression(self, ctx: JavaParser.ThisExpressionContext) -> jast.This:
        return jast.This(**self._get_location_rule(ctx))

    def visitSuperExpression(
        self, ctx: JavaParser.SuperExpressionContext
    ) -> jast.Super:
        return jast.Super(**self._get_location_rule(ctx))

    def visitLiteralExpression(
        self, ctx: JavaParser.LiteralExpressionContext
    ) -> jast.Constant:
        return jast.Constant(
            value=self.visitLiteral(ctx.literal()),
            **self._get_location_rule(ctx),
        )

    def visitIdentifierExpression(
        self, ctx: JavaParser.IdentifierExpressionContext
    ) -> jast.Name:
        return jast.Name(
            id=self.visitIdentifier(ctx.identifier()),
            **self._get_location_rule(ctx),
        )

    def visitClassExpression(
        self, ctx: JavaParser.ClassExpressionContext
    ) -> jast.ClassExpr:
        return jast.ClassExpr(
            type=self.visitTypeTypeOrVoid(ctx.typeTypeOrVoid()),
            **self._get_location_rule(ctx),
        )

    def visitExplicitGenericInvocationExpression(
        self, ctx: JavaParser.ExplicitGenericInvocationExpressionContext
    ) -> jast.ExplicitGenericInvocation:
        if ctx.THIS():
            location = self._get_location_rule(ctx)
            start = self._get_location_token(ctx.THIS())
            location["lineno"] = start["lineno"]
            location["col_offset"] = start["col_offset"]
            expression = jast.Call(
                func=jast.This(
                    **start,
                ),
                args=self.visitArguments(ctx.arguments()),
                **location,
            )
        else:
            expression = self.visitExplicitGenericInvocationSuffix(
                ctx.explicitGenericInvocationSuffix()
            )
        return jast.ExplicitGenericInvocation(
            type_args=self.visitNonWildcardTypeArguments(
                ctx.nonWildcardTypeArguments()
            ),
            value=expression,
            **self._get_location_rule(ctx),
        )

    def visitArrayAccessExpression(self, ctx: JavaParser.ArrayAccessExpressionContext):
        return jast.Subscript(
            value=self.visit(ctx.primary()),
            index=self.visitExpression(ctx.expression()),
            **self._get_location_rule(ctx),
        )

    def visitMemberReferenceExpression(
        self, ctx: JavaParser.MemberReferenceExpressionContext
    ):
        if ctx.THIS():
            expr = jast.This(**self._get_location_token(ctx.THIS()))
        elif ctx.superSuffix():
            expr = self.visitSuperSuffix(ctx.superSuffix())
        elif ctx.NEW():
            start = self._get_location_token(ctx.NEW())
            expr = self.visitInnerCreator(ctx.innerCreator())
            if ctx.nonWildcardTypeArguments():
                expr.type_args = self.visitNonWildcardTypeArguments(
                    ctx.nonWildcardTypeArguments()
                )
            expr.lineno = start["lineno"]
            expr.col_offset = start["col_offset"]
        elif ctx.identifier():
            expr = jast.Name(
                id=self.visitIdentifier(ctx.identifier()),
                **self._get_location_rule(ctx.identifier()),
            )
        elif ctx.methodCall():
            expr = self.visitMethodCall(ctx.methodCall())
        else:
            expr = self.visitExplicitGenericInvocation(ctx.explicitGenericInvocation())
        return jast.Member(
            value=self.visit(ctx.primary()),
            member=expr,
            **self._get_location_rule(ctx),
        )

    def visitMethodCallExpression(
        self, ctx: JavaParser.MethodCallExpressionContext
    ) -> jast.Call:
        return self.visitMethodCall(ctx.methodCall())

    def visitMethodReferenceExpression(
        self, ctx: JavaParser.MethodReferenceExpressionContext
    ) -> jast.Reference:
        if ctx.primary():
            expr = self.visit(ctx.primary())
        elif ctx.typeType():
            expr = self.visitTypeType(ctx.typeType())
        else:
            expr = self.visitClassType(ctx.classType())
        return jast.Reference(
            type=expr,
            type_args=self.visitTypeArguments(ctx.typeArguments())
            if ctx.typeArguments()
            else None,
            id=self.visitIdentifier(ctx.identifier()) if ctx.identifier() else None,
            new=ctx.NEW() is not None,
            **self._get_location_rule(ctx),
        )

    def visitSwitchExpression(
        self, ctx: JavaParser.SwitchExpressionContext
    ) -> jast.expr:
        if ctx.primary():
            return self.visit(ctx.primary())
        else:
            return jast.SwitchExp(
                value=self.visitParExpression(ctx.parExpression()),
                rules=[
                    self.visitSwitchLabeledRule(switchRule)
                    for switchRule in ctx.switchLabeledRule()
                ],
                **self._get_location_rule(ctx),
            )

    def visitSwitchLabeledRule(
        self, ctx: JavaParser.SwitchLabeledRuleContext
    ) -> jast.switchexprule:
        if ctx.CASE():
            if ctx.NULL_LITERAL():
                cases = [jast.Constant(jast.NullLiteral())]
            elif ctx.expressionList():
                cases = self.visitExpressionList(ctx.expressionList())
            else:
                cases = [self.visitGuardedPattern(ctx.guardedPattern())]
            label = jast.ExpCase()
        else:
            cases = None
            label = jast.ExpDefault()
        body = self.visitSwitchRuleOutcome(ctx.switchRuleOutcome())
        return jast.switchexprule(
            label=label,
            cases=cases,
            body=body,
        )

    def visitGuardedPattern(
        self, ctx: JavaParser.GuardedPatternContext
    ) -> jast.guardedpattern:
        if ctx.LPAREN():
            return self.visitGuardedPattern(ctx.guardedPattern())
        elif ctx.identifier():
            pattern = jast.pattern(
                modifiers=[
                    self.visitVariableModifier(modifier)
                    for modifier in ctx.variableModifier()
                ],
                type=self.visitTypeType(ctx.typeType()),
                annotations=[
                    self.visitAnnotation(annotation) for annotation in ctx.annotation()
                ],
                id=self.visitIdentifier(ctx.identifier()),
            )
            return jast.guardedpattern(
                value=pattern,
                conditions=[
                    self.visitExpression(condition) for condition in ctx.expression()
                ],
            )
        else:
            guarded_pattern = self.visitGuardedPattern(ctx.guardedPattern())
            guarded_pattern.conditions.append(self.visitExpression(ctx.expression(0)))
            return guarded_pattern

    def visitSwitchRuleOutcome(
        self, ctx: JavaParser.SwitchRuleOutcomeContext
    ) -> List[jast.stmt]:
        if ctx.block():
            return [self.visitBlock(ctx.block())]
        else:
            return [
                self.visitBlockStatement(statement)
                for statement in ctx.blockStatement()
            ]

    def visitClassType(self, ctx: JavaParser.ClassTypeContext) -> jast.ClassType:
        coit = jast.Coit(
            annotations=[
                self.visitAnnotation(annotation) for annotation in ctx.annotation()
            ],
            id=self.visitIdentifier(ctx.identifier()),
            type_args=self.visitTypeArguments(ctx.typeArguments())
            if ctx.typeArguments()
            else None,
        )
        if ctx.DOT():
            class_type = self.visitClassOrInterfaceType(ctx.classOrInterfaceType())
            if isinstance(class_type, jast.ClassType):
                class_type.coits.append(coit)
            else:
                class_type = jast.ClassType(coits=[class_type, coit])
            return class_type
        else:
            return coit

    def visitCreator(self, ctx: JavaParser.CreatorContext) -> jast.expr:
        if ctx.objectCreator():
            return self.visitObjectCreator(ctx.objectCreator())
        else:
            return self.visitArrayCreator(ctx.arrayCreator())

    def visitObjectCreator(
        self, ctx: JavaParser.ObjectCreatorContext
    ) -> jast.NewObject:
        return jast.NewObject(
            type_args=self.visitNonWildcardTypeArguments(ctx.nonWildcardTypeArguments())
            if ctx.nonWildcardTypeArguments()
            else None,
            type=self.visitCreatedName(ctx.createdName()),
            args=self.visitArguments(ctx.arguments()),
            body=self.visitClassBody(ctx.classBody()) if ctx.classBody() else None,
            **self._get_location_rule(ctx),
        )

    def visitCreatedName(self, ctx: JavaParser.CreatedNameContext) -> jast.jtype:
        if ctx.primitiveType():
            return self.visitPrimitiveType(ctx.primitiveType())
        else:
            coits = [self.visitCoitDiamond(coit) for coit in ctx.coitDiamond()]
            if len(coits) == 1:
                return coits[0]
            else:
                return jast.ClassType(coits=coits)

    def visitCoitDiamond(self, ctx: JavaParser.CoitDiamondContext) -> jast.Coit:
        return jast.Coit(
            id=self.visitIdentifier(ctx.identifier()),
            type_args=self.visitTypeArgumentsOrDiamond(ctx.typeArgumentsOrDiamond())
            if ctx.typeArgumentsOrDiamond()
            else None,
        )

    def visitInnerCreator(self, ctx: JavaParser.InnerCreatorContext) -> jast.NewObject:
        return jast.NewObject(
            type=jast.Coit(
                id=self.visitIdentifier(ctx.identifier()),
                type_args=self.visitNonWildcardTypeArgumentsOrDiamond(
                    ctx.nonWildcardTypeArgumentsOrDiamond()
                )
                if ctx.nonWildcardTypeArgumentsOrDiamond()
                else None,
            ),
            args=self.visitArguments(ctx.arguments()),
            body=self.visitClassBody(ctx.classBody()) if ctx.classBody() else None,
            **self._get_location_rule(ctx),
        )

    def visitDimExpr(self, ctx: JavaParser.DimExprContext) -> jast.expr:
        return self.visitExpression(ctx.expression())

    def visitArrayCreator(self, ctx: JavaParser.ArrayCreatorContext) -> jast.NewArray:
        return jast.NewArray(
            type=self.visitCreatedName(ctx.createdName()),
            expr_dims=[self.visitDimExpr(dimExpr) for dimExpr in ctx.dimExpr()],
            dims=self.visitDims(ctx.dims()) if ctx.dims() else None,
            init=self.visitArrayInitializer(ctx.arrayInitializer())
            if ctx.arrayInitializer()
            else None,
            **self._get_location_rule(ctx),
        )

    def visitExplicitGenericInvocation(
        self, ctx: JavaParser.ExplicitGenericInvocationContext
    ) -> jast.ExplicitGenericInvocation:
        return jast.ExplicitGenericInvocation(
            type_args=self.visitNonWildcardTypeArguments(
                ctx.nonWildcardTypeArguments()
            ),
            value=self.visitExplicitGenericInvocationSuffix(
                ctx.explicitGenericInvocationSuffix()
            ),
            **self._get_location_rule(ctx),
        )

    def visitTypeArgumentsOrDiamond(
        self, ctx: JavaParser.TypeArgumentsOrDiamondContext
    ) -> typeargs:
        if ctx.LT():
            return jast.typeargs(
                types=[],
            )
        else:
            return self.visitTypeArguments(ctx.typeArguments())

    def visitNonWildcardTypeArgumentsOrDiamond(
        self, ctx: JavaParser.NonWildcardTypeArgumentsOrDiamondContext
    ) -> typeargs:
        if ctx.LT():
            return jast.typeargs(
                types=[],
            )
        else:
            return self.visitNonWildcardTypeArguments(ctx.nonWildcardTypeArguments())

    def visitNonWildcardTypeArguments(
        self, ctx: JavaParser.NonWildcardTypeArgumentsContext
    ):
        return jast.typeargs(
            types=self.visitTypeList(ctx.typeList()),
        )

    def visitTypeList(self, ctx: JavaParser.TypeListContext):
        return [self.visitTypeType(typeType) for typeType in ctx.typeType()]

    def visitTypeType(self, ctx: JavaParser.TypeTypeContext) -> jast.jtype:
        if ctx.classOrInterfaceType():
            type_ = self.visitClassOrInterfaceType(ctx.classOrInterfaceType())
        else:
            type_ = self.visitPrimitiveType(ctx.primitiveType())
        if ctx.dims():
            type_ = jast.ArrayType(
                type=type_,
                dims=self.visitDims(ctx.dims()),
            )
        setattr(
            type_,
            "annotations",
            [self.visitAnnotation(annotation) for annotation in ctx.annotation()],
        )
        self._set_location_rule(type_, ctx)
        return type_

    def visitPrimitiveType(self, ctx: JavaParser.PrimitiveTypeContext):
        if ctx.BOOLEAN():
            return jast.Boolean()
        elif ctx.CHAR():
            return jast.Char()
        elif ctx.BYTE():
            return jast.Byte()
        elif ctx.SHORT():
            return jast.Short()
        elif ctx.INT():
            return jast.Int()
        elif ctx.LONG():
            return jast.Long()
        elif ctx.FLOAT():
            return jast.Float()
        else:
            return jast.Double()

    def visitTypeArguments(self, ctx: JavaParser.TypeArgumentsContext) -> typeargs:
        return jast.typeargs(
            types=[
                self.visitTypeArgument(typeArgument)
                for typeArgument in ctx.typeArgument()
            ],
        )

    def visitSuperSuffix(self, ctx: JavaParser.SuperSuffixContext) -> jast.Super:
        location = self._get_location_token(ctx.SUPER())
        if ctx.identifier():
            end = self._get_location_rule(ctx.identifier())
            location["end_lineno"] = end["end_lineno"]
            location["end_col_offset"] = end["end_col_offset"]
        expr = jast.Super(
            type_args=self.visitTypeArguments(ctx.typeArguments())
            if ctx.typeArguments()
            else None,
            id=self.visitIdentifier(ctx.identifier()) if ctx.identifier() else None,
            **location,
        )
        if ctx.arguments():
            expr = jast.Call(
                func=expr,
                args=self.visitArguments(ctx.arguments()),
                **self._get_location_rule(ctx),
            )
        return expr

    def visitExplicitGenericInvocationSuffix(
        self, ctx: JavaParser.ExplicitGenericInvocationSuffixContext
    ) -> jast.expr:
        if ctx.superSuffix():
            return self.visitSuperSuffix(ctx.superSuffix())
        else:
            return jast.Call(
                func=jast.Name(
                    id=self.visitIdentifier(ctx.identifier()),
                    **self._get_location_rule(ctx.identifier()),
                ),
                args=self.visitArguments(ctx.arguments()),
                **self._get_location_rule(ctx),
            )

    def visitArguments(self, ctx: JavaParser.ArgumentsContext) -> List[jast.expr]:
        return (
            self.visitExpressionList(ctx.expressionList())
            if ctx.expressionList()
            else []
        )

    def visitDeclarationStart(
        self, ctx: JavaParser.DeclarationStartContext
    ) -> jast.declaration:
        if ctx.packageDeclaration():
            return self.visitPackageDeclaration(ctx.packageDeclaration())
        elif ctx.importDeclaration():
            return self.visitImportDeclaration(ctx.importDeclaration())
        elif ctx.moduleDeclaration():
            return self.visitModuleDeclaration(ctx.moduleDeclaration())
        elif ctx.fieldDeclaration():
            decl = self.visitFieldDeclaration(ctx.fieldDeclaration())
        elif ctx.methodDeclaration():
            decl = self.visitMethodDeclaration(ctx.methodDeclaration())
        elif ctx.interfaceMethodDeclaration():
            decl = self.visitInterfaceMethodDeclaration(
                ctx.interfaceMethodDeclaration()
            )
        elif ctx.block():
            return jast.Initializer(
                body=self.visitBlock(ctx.block()),
                static=ctx.STATIC() is not None,
                **self._get_location_rule(ctx),
            )
        elif ctx.constructorDeclaration():
            decl = self.visitConstructorDeclaration(ctx.constructorDeclaration())
        elif ctx.compactConstructorDeclaration():
            decl = self.visitCompactConstructorDeclaration(
                ctx.compactConstructorDeclaration()
            )
        elif ctx.interfaceDeclaration():
            decl = self.visitInterfaceDeclaration(ctx.interfaceDeclaration())
        elif ctx.annotationMethodDeclaration():
            decl = self.visitAnnotationMethodDeclaration(
                ctx.annotationMethodDeclaration()
            )
        elif ctx.annotationConstantDeclaration():
            decl = self.visitAnnotationConstantDeclaration(
                ctx.annotationConstantDeclaration()
            )
        elif ctx.annotationTypeDeclaration():
            decl = self.visitAnnotationTypeDeclaration(ctx.annotationTypeDeclaration())
        elif ctx.classDeclaration():
            decl = self.visitClassDeclaration(ctx.classDeclaration())
        elif ctx.enumDeclaration():
            decl = self.visitEnumDeclaration(ctx.enumDeclaration())
        elif ctx.recordDeclaration():
            decl = self.visitRecordDeclaration(ctx.recordDeclaration())
        else:
            decl = jast.EmptyDecl(**self._get_location_rule(ctx))
        if ctx.modifier():
            modifiers = [self.visitModifier(modifier) for modifier in ctx.modifier()]
            setattr(decl, "modifiers", modifiers)
        return decl

    def visitStatementStart(self, ctx: JavaParser.StatementStartContext) -> jast.stmt:
        return self.visitBlockStatement(ctx.blockStatement())

    def visitExpressionStart(self, ctx: JavaParser.ExpressionStartContext) -> jast.expr:
        return self.visitExpression(ctx.expression())

    def visitDirectiveStart(self, ctx: JavaParser.DirectiveStartContext):
        return self.visitModuleDirective(ctx.moduleDirective())
