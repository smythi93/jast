# Generated from antlr/java/JavaParser.g4 by ANTLR 4.13.2
from antlr4 import *

if "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser


# This class defines a complete listener for a parse tree produced by JavaParser.
class JavaParserListener(ParseTreeListener):
    # Enter a parse tree produced by JavaParser#compilationUnit.
    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaParser#compilationUnit.
    def exitCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        pass

    # Enter a parse tree produced by JavaParser#declarationStart.
    def enterDeclarationStart(self, ctx: JavaParser.DeclarationStartContext):
        pass

    # Exit a parse tree produced by JavaParser#declarationStart.
    def exitDeclarationStart(self, ctx: JavaParser.DeclarationStartContext):
        pass

    # Enter a parse tree produced by JavaParser#statementStart.
    def enterStatementStart(self, ctx: JavaParser.StatementStartContext):
        pass

    # Exit a parse tree produced by JavaParser#statementStart.
    def exitStatementStart(self, ctx: JavaParser.StatementStartContext):
        pass

    # Enter a parse tree produced by JavaParser#expressionStart.
    def enterExpressionStart(self, ctx: JavaParser.ExpressionStartContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionStart.
    def exitExpressionStart(self, ctx: JavaParser.ExpressionStartContext):
        pass

    # Enter a parse tree produced by JavaParser#ordinaryCompilationUnit.
    def enterOrdinaryCompilationUnit(
        self, ctx: JavaParser.OrdinaryCompilationUnitContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#ordinaryCompilationUnit.
    def exitOrdinaryCompilationUnit(
        self, ctx: JavaParser.OrdinaryCompilationUnitContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#modularCompilationUnit.
    def enterModularCompilationUnit(
        self, ctx: JavaParser.ModularCompilationUnitContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#modularCompilationUnit.
    def exitModularCompilationUnit(self, ctx: JavaParser.ModularCompilationUnitContext):
        pass

    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#packageDeclaration.
    def exitPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx: JavaParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx: JavaParser.TypeDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#modifier.
    def enterModifier(self, ctx: JavaParser.ModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#modifier.
    def exitModifier(self, ctx: JavaParser.ModifierContext):
        pass

    # Enter a parse tree produced by JavaParser#classOrInterfaceModifier.
    def enterClassOrInterfaceModifier(
        self, ctx: JavaParser.ClassOrInterfaceModifierContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#classOrInterfaceModifier.
    def exitClassOrInterfaceModifier(
        self, ctx: JavaParser.ClassOrInterfaceModifierContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#variableModifier.
    def enterVariableModifier(self, ctx: JavaParser.VariableModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#variableModifier.
    def exitVariableModifier(self, ctx: JavaParser.VariableModifierContext):
        pass

    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classDeclaration.
    def exitClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#classExtends.
    def enterClassExtends(self, ctx: JavaParser.ClassExtendsContext):
        pass

    # Exit a parse tree produced by JavaParser#classExtends.
    def exitClassExtends(self, ctx: JavaParser.ClassExtendsContext):
        pass

    # Enter a parse tree produced by JavaParser#classImplements.
    def enterClassImplements(self, ctx: JavaParser.ClassImplementsContext):
        pass

    # Exit a parse tree produced by JavaParser#classImplements.
    def exitClassImplements(self, ctx: JavaParser.ClassImplementsContext):
        pass

    # Enter a parse tree produced by JavaParser#classPermits.
    def enterClassPermits(self, ctx: JavaParser.ClassPermitsContext):
        pass

    # Exit a parse tree produced by JavaParser#classPermits.
    def exitClassPermits(self, ctx: JavaParser.ClassPermitsContext):
        pass

    # Enter a parse tree produced by JavaParser#typeParameters.
    def enterTypeParameters(self, ctx: JavaParser.TypeParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameters.
    def exitTypeParameters(self, ctx: JavaParser.TypeParametersContext):
        pass

    # Enter a parse tree produced by JavaParser#typeParameter.
    def enterTypeParameter(self, ctx: JavaParser.TypeParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameter.
    def exitTypeParameter(self, ctx: JavaParser.TypeParameterContext):
        pass

    # Enter a parse tree produced by JavaParser#typeBound.
    def enterTypeBound(self, ctx: JavaParser.TypeBoundContext):
        pass

    # Exit a parse tree produced by JavaParser#typeBound.
    def exitTypeBound(self, ctx: JavaParser.TypeBoundContext):
        pass

    # Enter a parse tree produced by JavaParser#enumDeclaration.
    def enterEnumDeclaration(self, ctx: JavaParser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#enumDeclaration.
    def exitEnumDeclaration(self, ctx: JavaParser.EnumDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#enumConstants.
    def enterEnumConstants(self, ctx: JavaParser.EnumConstantsContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstants.
    def exitEnumConstants(self, ctx: JavaParser.EnumConstantsContext):
        pass

    # Enter a parse tree produced by JavaParser#enumConstant.
    def enterEnumConstant(self, ctx: JavaParser.EnumConstantContext):
        pass

    # Exit a parse tree produced by JavaParser#enumConstant.
    def exitEnumConstant(self, ctx: JavaParser.EnumConstantContext):
        pass

    # Enter a parse tree produced by JavaParser#enumBodyDeclarations.
    def enterEnumBodyDeclarations(self, ctx: JavaParser.EnumBodyDeclarationsContext):
        pass

    # Exit a parse tree produced by JavaParser#enumBodyDeclarations.
    def exitEnumBodyDeclarations(self, ctx: JavaParser.EnumBodyDeclarationsContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx: JavaParser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx: JavaParser.InterfaceDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#classBody.
    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#classBody.
    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceBody.
    def enterInterfaceBody(self, ctx: JavaParser.InterfaceBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBody.
    def exitInterfaceBody(self, ctx: JavaParser.InterfaceBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#classBodyDeclaration.
    def enterClassBodyDeclaration(self, ctx: JavaParser.ClassBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classBodyDeclaration.
    def exitClassBodyDeclaration(self, ctx: JavaParser.ClassBodyDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#memberDeclaration.
    def enterMemberDeclaration(self, ctx: JavaParser.MemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#memberDeclaration.
    def exitMemberDeclaration(self, ctx: JavaParser.MemberDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#dims.
    def enterDims(self, ctx: JavaParser.DimsContext):
        pass

    # Exit a parse tree produced by JavaParser#dims.
    def exitDims(self, ctx: JavaParser.DimsContext):
        pass

    # Enter a parse tree produced by JavaParser#dim.
    def enterDim(self, ctx: JavaParser.DimContext):
        pass

    # Exit a parse tree produced by JavaParser#dim.
    def exitDim(self, ctx: JavaParser.DimContext):
        pass

    # Enter a parse tree produced by JavaParser#throws_.
    def enterThrows_(self, ctx: JavaParser.Throws_Context):
        pass

    # Exit a parse tree produced by JavaParser#throws_.
    def exitThrows_(self, ctx: JavaParser.Throws_Context):
        pass

    # Enter a parse tree produced by JavaParser#methodBody.
    def enterMethodBody(self, ctx: JavaParser.MethodBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#methodBody.
    def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#typeTypeOrVoid.
    def enterTypeTypeOrVoid(self, ctx: JavaParser.TypeTypeOrVoidContext):
        pass

    # Exit a parse tree produced by JavaParser#typeTypeOrVoid.
    def exitTypeTypeOrVoid(self, ctx: JavaParser.TypeTypeOrVoidContext):
        pass

    # Enter a parse tree produced by JavaParser#constructorDeclaration.
    def enterConstructorDeclaration(
        self, ctx: JavaParser.ConstructorDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#compactConstructorDeclaration.
    def enterCompactConstructorDeclaration(
        self, ctx: JavaParser.CompactConstructorDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#compactConstructorDeclaration.
    def exitCompactConstructorDeclaration(
        self, ctx: JavaParser.CompactConstructorDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def enterInterfaceBodyDeclaration(
        self, ctx: JavaParser.InterfaceBodyDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def exitInterfaceBodyDeclaration(
        self, ctx: JavaParser.InterfaceBodyDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def enterInterfaceMemberDeclaration(
        self, ctx: JavaParser.InterfaceMemberDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def exitInterfaceMemberDeclaration(
        self, ctx: JavaParser.InterfaceMemberDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#constDeclaration.
    def enterConstDeclaration(self, ctx: JavaParser.ConstDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#constDeclaration.
    def exitConstDeclaration(self, ctx: JavaParser.ConstDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#interfaceMethodModifier.
    def enterInterfaceMethodModifier(
        self, ctx: JavaParser.InterfaceMethodModifierContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodModifier.
    def exitInterfaceMethodModifier(
        self, ctx: JavaParser.InterfaceMethodModifierContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def enterInterfaceMethodDeclaration(
        self, ctx: JavaParser.InterfaceMethodDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def exitInterfaceMethodDeclaration(
        self, ctx: JavaParser.InterfaceMethodDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#variableDeclarators.
    def enterVariableDeclarators(self, ctx: JavaParser.VariableDeclaratorsContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarators.
    def exitVariableDeclarators(self, ctx: JavaParser.VariableDeclaratorsContext):
        pass

    # Enter a parse tree produced by JavaParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        pass

    # Enter a parse tree produced by JavaParser#variableDeclaratorId.
    def enterVariableDeclaratorId(self, ctx: JavaParser.VariableDeclaratorIdContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclaratorId.
    def exitVariableDeclaratorId(self, ctx: JavaParser.VariableDeclaratorIdContext):
        pass

    # Enter a parse tree produced by JavaParser#variableInitializer.
    def enterVariableInitializer(self, ctx: JavaParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#variableInitializer.
    def exitVariableInitializer(self, ctx: JavaParser.VariableInitializerContext):
        pass

    # Enter a parse tree produced by JavaParser#arrayInitializer.
    def enterArrayInitializer(self, ctx: JavaParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayInitializer.
    def exitArrayInitializer(self, ctx: JavaParser.ArrayInitializerContext):
        pass

    # Enter a parse tree produced by JavaParser#classOrInterfaceType.
    def enterClassOrInterfaceType(self, ctx: JavaParser.ClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#classOrInterfaceType.
    def exitClassOrInterfaceType(self, ctx: JavaParser.ClassOrInterfaceTypeContext):
        pass

    # Enter a parse tree produced by JavaParser#coit.
    def enterCoit(self, ctx: JavaParser.CoitContext):
        pass

    # Exit a parse tree produced by JavaParser#coit.
    def exitCoit(self, ctx: JavaParser.CoitContext):
        pass

    # Enter a parse tree produced by JavaParser#typeArgument.
    def enterTypeArgument(self, ctx: JavaParser.TypeArgumentContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgument.
    def exitTypeArgument(self, ctx: JavaParser.TypeArgumentContext):
        pass

    # Enter a parse tree produced by JavaParser#qualifiedNameList.
    def enterQualifiedNameList(self, ctx: JavaParser.QualifiedNameListContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedNameList.
    def exitQualifiedNameList(self, ctx: JavaParser.QualifiedNameListContext):
        pass

    # Enter a parse tree produced by JavaParser#formalParameters.
    def enterFormalParameters(self, ctx: JavaParser.FormalParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameters.
    def exitFormalParameters(self, ctx: JavaParser.FormalParametersContext):
        pass

    # Enter a parse tree produced by JavaParser#receiverParameter.
    def enterReceiverParameter(self, ctx: JavaParser.ReceiverParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#receiverParameter.
    def exitReceiverParameter(self, ctx: JavaParser.ReceiverParameterContext):
        pass

    # Enter a parse tree produced by JavaParser#formalParameterList.
    def enterFormalParameterList(self, ctx: JavaParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameterList.
    def exitFormalParameterList(self, ctx: JavaParser.FormalParameterListContext):
        pass

    # Enter a parse tree produced by JavaParser#formalParameter.
    def enterFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#formalParameter.
    def exitFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        pass

    # Enter a parse tree produced by JavaParser#lastFormalParameter.
    def enterLastFormalParameter(self, ctx: JavaParser.LastFormalParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#lastFormalParameter.
    def exitLastFormalParameter(self, ctx: JavaParser.LastFormalParameterContext):
        pass

    # Enter a parse tree produced by JavaParser#lambdaLVTIList.
    def enterLambdaLVTIList(self, ctx: JavaParser.LambdaLVTIListContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaLVTIList.
    def exitLambdaLVTIList(self, ctx: JavaParser.LambdaLVTIListContext):
        pass

    # Enter a parse tree produced by JavaParser#lambdaLVTIParameter.
    def enterLambdaLVTIParameter(self, ctx: JavaParser.LambdaLVTIParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaLVTIParameter.
    def exitLambdaLVTIParameter(self, ctx: JavaParser.LambdaLVTIParameterContext):
        pass

    # Enter a parse tree produced by JavaParser#qualifiedName.
    def enterQualifiedName(self, ctx: JavaParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedName.
    def exitQualifiedName(self, ctx: JavaParser.QualifiedNameContext):
        pass

    # Enter a parse tree produced by JavaParser#literal.
    def enterLiteral(self, ctx: JavaParser.LiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#literal.
    def exitLiteral(self, ctx: JavaParser.LiteralContext):
        pass

    # Enter a parse tree produced by JavaParser#integerLiteral.
    def enterIntegerLiteral(self, ctx: JavaParser.IntegerLiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#integerLiteral.
    def exitIntegerLiteral(self, ctx: JavaParser.IntegerLiteralContext):
        pass

    # Enter a parse tree produced by JavaParser#floatLiteral.
    def enterFloatLiteral(self, ctx: JavaParser.FloatLiteralContext):
        pass

    # Exit a parse tree produced by JavaParser#floatLiteral.
    def exitFloatLiteral(self, ctx: JavaParser.FloatLiteralContext):
        pass

    # Enter a parse tree produced by JavaParser#annotation.
    def enterAnnotation(self, ctx: JavaParser.AnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotation.
    def exitAnnotation(self, ctx: JavaParser.AnnotationContext):
        pass

    # Enter a parse tree produced by JavaParser#elementValuePairs.
    def enterElementValuePairs(self, ctx: JavaParser.ElementValuePairsContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValuePairs.
    def exitElementValuePairs(self, ctx: JavaParser.ElementValuePairsContext):
        pass

    # Enter a parse tree produced by JavaParser#elementValuePair.
    def enterElementValuePair(self, ctx: JavaParser.ElementValuePairContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValuePair.
    def exitElementValuePair(self, ctx: JavaParser.ElementValuePairContext):
        pass

    # Enter a parse tree produced by JavaParser#elementValue.
    def enterElementValue(self, ctx: JavaParser.ElementValueContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValue.
    def exitElementValue(self, ctx: JavaParser.ElementValueContext):
        pass

    # Enter a parse tree produced by JavaParser#elementValueArrayInitializer.
    def enterElementValueArrayInitializer(
        self, ctx: JavaParser.ElementValueArrayInitializerContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#elementValueArrayInitializer.
    def exitElementValueArrayInitializer(
        self, ctx: JavaParser.ElementValueArrayInitializerContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#annotationTypeDeclaration.
    def enterAnnotationTypeDeclaration(
        self, ctx: JavaParser.AnnotationTypeDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeDeclaration.
    def exitAnnotationTypeDeclaration(
        self, ctx: JavaParser.AnnotationTypeDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#annotationTypeBody.
    def enterAnnotationTypeBody(self, ctx: JavaParser.AnnotationTypeBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeBody.
    def exitAnnotationTypeBody(self, ctx: JavaParser.AnnotationTypeBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#annotationTypeElementDeclaration.
    def enterAnnotationTypeElementDeclaration(
        self, ctx: JavaParser.AnnotationTypeElementDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeElementDeclaration.
    def exitAnnotationTypeElementDeclaration(
        self, ctx: JavaParser.AnnotationTypeElementDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#annotationTypeElementRest.
    def enterAnnotationTypeElementRest(
        self, ctx: JavaParser.AnnotationTypeElementRestContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#annotationTypeElementRest.
    def exitAnnotationTypeElementRest(
        self, ctx: JavaParser.AnnotationTypeElementRestContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#annotationConstantDeclaration.
    def enterAnnotationConstantDeclaration(
        self, ctx: JavaParser.AnnotationConstantDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#annotationConstantDeclaration.
    def exitAnnotationConstantDeclaration(
        self, ctx: JavaParser.AnnotationConstantDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#annotationMethodDeclaration.
    def enterAnnotationMethodDeclaration(
        self, ctx: JavaParser.AnnotationMethodDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#annotationMethodDeclaration.
    def exitAnnotationMethodDeclaration(
        self, ctx: JavaParser.AnnotationMethodDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#defaultValue.
    def enterDefaultValue(self, ctx: JavaParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by JavaParser#defaultValue.
    def exitDefaultValue(self, ctx: JavaParser.DefaultValueContext):
        pass

    # Enter a parse tree produced by JavaParser#moduleDeclaration.
    def enterModuleDeclaration(self, ctx: JavaParser.ModuleDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleDeclaration.
    def exitModuleDeclaration(self, ctx: JavaParser.ModuleDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#moduleBody.
    def enterModuleBody(self, ctx: JavaParser.ModuleBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleBody.
    def exitModuleBody(self, ctx: JavaParser.ModuleBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#moduleDirective.
    def enterModuleDirective(self, ctx: JavaParser.ModuleDirectiveContext):
        pass

    # Exit a parse tree produced by JavaParser#moduleDirective.
    def exitModuleDirective(self, ctx: JavaParser.ModuleDirectiveContext):
        pass

    # Enter a parse tree produced by JavaParser#requiresModifier.
    def enterRequiresModifier(self, ctx: JavaParser.RequiresModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#requiresModifier.
    def exitRequiresModifier(self, ctx: JavaParser.RequiresModifierContext):
        pass

    # Enter a parse tree produced by JavaParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx: JavaParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx: JavaParser.RecordDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#recordComponentList.
    def enterRecordComponentList(self, ctx: JavaParser.RecordComponentListContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponentList.
    def exitRecordComponentList(self, ctx: JavaParser.RecordComponentListContext):
        pass

    # Enter a parse tree produced by JavaParser#recordComponent.
    def enterRecordComponent(self, ctx: JavaParser.RecordComponentContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponent.
    def exitRecordComponent(self, ctx: JavaParser.RecordComponentContext):
        pass

    # Enter a parse tree produced by JavaParser#recordBody.
    def enterRecordBody(self, ctx: JavaParser.RecordBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#recordBody.
    def exitRecordBody(self, ctx: JavaParser.RecordBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#recordBodyDeclaration.
    def enterRecordBodyDeclaration(self, ctx: JavaParser.RecordBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#recordBodyDeclaration.
    def exitRecordBodyDeclaration(self, ctx: JavaParser.RecordBodyDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#block.
    def enterBlock(self, ctx: JavaParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaParser#block.
    def exitBlock(self, ctx: JavaParser.BlockContext):
        pass

    # Enter a parse tree produced by JavaParser#blockStatement.
    def enterBlockStatement(self, ctx: JavaParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#blockStatement.
    def exitBlockStatement(self, ctx: JavaParser.BlockStatementContext):
        pass

    # Enter a parse tree produced by JavaParser#localVariableDeclaration.
    def enterLocalVariableDeclaration(
        self, ctx: JavaParser.LocalVariableDeclarationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#localVariableDeclaration.
    def exitLocalVariableDeclaration(
        self, ctx: JavaParser.LocalVariableDeclarationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#identifier.
    def enterIdentifier(self, ctx: JavaParser.IdentifierContext):
        pass

    # Exit a parse tree produced by JavaParser#identifier.
    def exitIdentifier(self, ctx: JavaParser.IdentifierContext):
        pass

    # Enter a parse tree produced by JavaParser#typeIdentifier.
    def enterTypeIdentifier(self, ctx: JavaParser.TypeIdentifierContext):
        pass

    # Exit a parse tree produced by JavaParser#typeIdentifier.
    def exitTypeIdentifier(self, ctx: JavaParser.TypeIdentifierContext):
        pass

    # Enter a parse tree produced by JavaParser#localTypeDeclaration.
    def enterLocalTypeDeclaration(self, ctx: JavaParser.LocalTypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#localTypeDeclaration.
    def exitLocalTypeDeclaration(self, ctx: JavaParser.LocalTypeDeclarationContext):
        pass

    # Enter a parse tree produced by JavaParser#statement.
    def enterStatement(self, ctx: JavaParser.StatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statement.
    def exitStatement(self, ctx: JavaParser.StatementContext):
        pass

    # Enter a parse tree produced by JavaParser#switchBlock.
    def enterSwitchBlock(self, ctx: JavaParser.SwitchBlockContext):
        pass

    # Exit a parse tree produced by JavaParser#switchBlock.
    def exitSwitchBlock(self, ctx: JavaParser.SwitchBlockContext):
        pass

    # Enter a parse tree produced by JavaParser#catchClause.
    def enterCatchClause(self, ctx: JavaParser.CatchClauseContext):
        pass

    # Exit a parse tree produced by JavaParser#catchClause.
    def exitCatchClause(self, ctx: JavaParser.CatchClauseContext):
        pass

    # Enter a parse tree produced by JavaParser#catchType.
    def enterCatchType(self, ctx: JavaParser.CatchTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#catchType.
    def exitCatchType(self, ctx: JavaParser.CatchTypeContext):
        pass

    # Enter a parse tree produced by JavaParser#finallyBlock.
    def enterFinallyBlock(self, ctx: JavaParser.FinallyBlockContext):
        pass

    # Exit a parse tree produced by JavaParser#finallyBlock.
    def exitFinallyBlock(self, ctx: JavaParser.FinallyBlockContext):
        pass

    # Enter a parse tree produced by JavaParser#resourceSpecification.
    def enterResourceSpecification(self, ctx: JavaParser.ResourceSpecificationContext):
        pass

    # Exit a parse tree produced by JavaParser#resourceSpecification.
    def exitResourceSpecification(self, ctx: JavaParser.ResourceSpecificationContext):
        pass

    # Enter a parse tree produced by JavaParser#resources.
    def enterResources(self, ctx: JavaParser.ResourcesContext):
        pass

    # Exit a parse tree produced by JavaParser#resources.
    def exitResources(self, ctx: JavaParser.ResourcesContext):
        pass

    # Enter a parse tree produced by JavaParser#resource.
    def enterResource(self, ctx: JavaParser.ResourceContext):
        pass

    # Exit a parse tree produced by JavaParser#resource.
    def exitResource(self, ctx: JavaParser.ResourceContext):
        pass

    # Enter a parse tree produced by JavaParser#switchBlockStatementGroup.
    def enterSwitchBlockStatementGroup(
        self, ctx: JavaParser.SwitchBlockStatementGroupContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#switchBlockStatementGroup.
    def exitSwitchBlockStatementGroup(
        self, ctx: JavaParser.SwitchBlockStatementGroupContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#switchLabel.
    def enterSwitchLabel(self, ctx: JavaParser.SwitchLabelContext):
        pass

    # Exit a parse tree produced by JavaParser#switchLabel.
    def exitSwitchLabel(self, ctx: JavaParser.SwitchLabelContext):
        pass

    # Enter a parse tree produced by JavaParser#forInit.
    def enterForInit(self, ctx: JavaParser.ForInitContext):
        pass

    # Exit a parse tree produced by JavaParser#forInit.
    def exitForInit(self, ctx: JavaParser.ForInitContext):
        pass

    # Enter a parse tree produced by JavaParser#parExpression.
    def enterParExpression(self, ctx: JavaParser.ParExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#parExpression.
    def exitParExpression(self, ctx: JavaParser.ParExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#expressionList.
    def enterExpressionList(self, ctx: JavaParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionList.
    def exitExpressionList(self, ctx: JavaParser.ExpressionListContext):
        pass

    # Enter a parse tree produced by JavaParser#methodCall.
    def enterMethodCall(self, ctx: JavaParser.MethodCallContext):
        pass

    # Exit a parse tree produced by JavaParser#methodCall.
    def exitMethodCall(self, ctx: JavaParser.MethodCallContext):
        pass

    # Enter a parse tree produced by JavaParser#postfixExpression.
    def enterPostfixExpression(self, ctx: JavaParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#postfixExpression.
    def exitPostfixExpression(self, ctx: JavaParser.PostfixExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#prefixExpression.
    def enterPrefixExpression(self, ctx: JavaParser.PrefixExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#prefixExpression.
    def exitPrefixExpression(self, ctx: JavaParser.PrefixExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#typeExpression.
    def enterTypeExpression(self, ctx: JavaParser.TypeExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#typeExpression.
    def exitTypeExpression(self, ctx: JavaParser.TypeExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#multiplicativeExpression.
    def enterMultiplicativeExpression(
        self, ctx: JavaParser.MultiplicativeExpressionContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#multiplicativeExpression.
    def exitMultiplicativeExpression(
        self, ctx: JavaParser.MultiplicativeExpressionContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#additiveExpression.
    def enterAdditiveExpression(self, ctx: JavaParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#additiveExpression.
    def exitAdditiveExpression(self, ctx: JavaParser.AdditiveExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#shiftExpression.
    def enterShiftExpression(self, ctx: JavaParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#shiftExpression.
    def exitShiftExpression(self, ctx: JavaParser.ShiftExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#relationalExpression.
    def enterRelationalExpression(self, ctx: JavaParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#relationalExpression.
    def exitRelationalExpression(self, ctx: JavaParser.RelationalExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#equalityExpression.
    def enterEqualityExpression(self, ctx: JavaParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#equalityExpression.
    def exitEqualityExpression(self, ctx: JavaParser.EqualityExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#bitwiseAndExpression.
    def enterBitwiseAndExpression(self, ctx: JavaParser.BitwiseAndExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#bitwiseAndExpression.
    def exitBitwiseAndExpression(self, ctx: JavaParser.BitwiseAndExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#bitwiseXorExpression.
    def enterBitwiseXorExpression(self, ctx: JavaParser.BitwiseXorExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#bitwiseXorExpression.
    def exitBitwiseXorExpression(self, ctx: JavaParser.BitwiseXorExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#bitwiseOrExpression.
    def enterBitwiseOrExpression(self, ctx: JavaParser.BitwiseOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#bitwiseOrExpression.
    def exitBitwiseOrExpression(self, ctx: JavaParser.BitwiseOrExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx: JavaParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx: JavaParser.LogicalAndExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx: JavaParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx: JavaParser.LogicalOrExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#ternaryExpression.
    def enterTernaryExpression(self, ctx: JavaParser.TernaryExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#ternaryExpression.
    def exitTernaryExpression(self, ctx: JavaParser.TernaryExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx: JavaParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx: JavaParser.AssignmentExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#expression.
    def enterExpression(self, ctx: JavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#expression.
    def exitExpression(self, ctx: JavaParser.ExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#pattern.
    def enterPattern(self, ctx: JavaParser.PatternContext):
        pass

    # Exit a parse tree produced by JavaParser#pattern.
    def exitPattern(self, ctx: JavaParser.PatternContext):
        pass

    # Enter a parse tree produced by JavaParser#lambdaExpression.
    def enterLambdaExpression(self, ctx: JavaParser.LambdaExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaExpression.
    def exitLambdaExpression(self, ctx: JavaParser.LambdaExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#lambdaParameters.
    def enterLambdaParameters(self, ctx: JavaParser.LambdaParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParameters.
    def exitLambdaParameters(self, ctx: JavaParser.LambdaParametersContext):
        pass

    # Enter a parse tree produced by JavaParser#lambdaBody.
    def enterLambdaBody(self, ctx: JavaParser.LambdaBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaBody.
    def exitLambdaBody(self, ctx: JavaParser.LambdaBodyContext):
        pass

    # Enter a parse tree produced by JavaParser#ExplicitGenericInvocationExpression.
    def enterExplicitGenericInvocationExpression(
        self, ctx: JavaParser.ExplicitGenericInvocationExpressionContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#ExplicitGenericInvocationExpression.
    def exitExplicitGenericInvocationExpression(
        self, ctx: JavaParser.ExplicitGenericInvocationExpressionContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#ThisExpression.
    def enterThisExpression(self, ctx: JavaParser.ThisExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#ThisExpression.
    def exitThisExpression(self, ctx: JavaParser.ThisExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#MemberReferenceExpression.
    def enterMemberReferenceExpression(
        self, ctx: JavaParser.MemberReferenceExpressionContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#MemberReferenceExpression.
    def exitMemberReferenceExpression(
        self, ctx: JavaParser.MemberReferenceExpressionContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#MethodCallExpression.
    def enterMethodCallExpression(self, ctx: JavaParser.MethodCallExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#MethodCallExpression.
    def exitMethodCallExpression(self, ctx: JavaParser.MethodCallExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#MethodReferenceExpression.
    def enterMethodReferenceExpression(
        self, ctx: JavaParser.MethodReferenceExpressionContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#MethodReferenceExpression.
    def exitMethodReferenceExpression(
        self, ctx: JavaParser.MethodReferenceExpressionContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#ParExpr.
    def enterParExpr(self, ctx: JavaParser.ParExprContext):
        pass

    # Exit a parse tree produced by JavaParser#ParExpr.
    def exitParExpr(self, ctx: JavaParser.ParExprContext):
        pass

    # Enter a parse tree produced by JavaParser#LiteralExpression.
    def enterLiteralExpression(self, ctx: JavaParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#LiteralExpression.
    def exitLiteralExpression(self, ctx: JavaParser.LiteralExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#ClassExpression.
    def enterClassExpression(self, ctx: JavaParser.ClassExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#ClassExpression.
    def exitClassExpression(self, ctx: JavaParser.ClassExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#SuperExpression.
    def enterSuperExpression(self, ctx: JavaParser.SuperExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#SuperExpression.
    def exitSuperExpression(self, ctx: JavaParser.SuperExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#ArrayAccessExpression.
    def enterArrayAccessExpression(self, ctx: JavaParser.ArrayAccessExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#ArrayAccessExpression.
    def exitArrayAccessExpression(self, ctx: JavaParser.ArrayAccessExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#IdentifierExpression.
    def enterIdentifierExpression(self, ctx: JavaParser.IdentifierExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#IdentifierExpression.
    def exitIdentifierExpression(self, ctx: JavaParser.IdentifierExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#switchExpression.
    def enterSwitchExpression(self, ctx: JavaParser.SwitchExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#switchExpression.
    def exitSwitchExpression(self, ctx: JavaParser.SwitchExpressionContext):
        pass

    # Enter a parse tree produced by JavaParser#switchLabeledRule.
    def enterSwitchLabeledRule(self, ctx: JavaParser.SwitchLabeledRuleContext):
        pass

    # Exit a parse tree produced by JavaParser#switchLabeledRule.
    def exitSwitchLabeledRule(self, ctx: JavaParser.SwitchLabeledRuleContext):
        pass

    # Enter a parse tree produced by JavaParser#guardedPattern.
    def enterGuardedPattern(self, ctx: JavaParser.GuardedPatternContext):
        pass

    # Exit a parse tree produced by JavaParser#guardedPattern.
    def exitGuardedPattern(self, ctx: JavaParser.GuardedPatternContext):
        pass

    # Enter a parse tree produced by JavaParser#switchRuleOutcome.
    def enterSwitchRuleOutcome(self, ctx: JavaParser.SwitchRuleOutcomeContext):
        pass

    # Exit a parse tree produced by JavaParser#switchRuleOutcome.
    def exitSwitchRuleOutcome(self, ctx: JavaParser.SwitchRuleOutcomeContext):
        pass

    # Enter a parse tree produced by JavaParser#classType.
    def enterClassType(self, ctx: JavaParser.ClassTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#classType.
    def exitClassType(self, ctx: JavaParser.ClassTypeContext):
        pass

    # Enter a parse tree produced by JavaParser#creator.
    def enterCreator(self, ctx: JavaParser.CreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#creator.
    def exitCreator(self, ctx: JavaParser.CreatorContext):
        pass

    # Enter a parse tree produced by JavaParser#objectCreator.
    def enterObjectCreator(self, ctx: JavaParser.ObjectCreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#objectCreator.
    def exitObjectCreator(self, ctx: JavaParser.ObjectCreatorContext):
        pass

    # Enter a parse tree produced by JavaParser#createdName.
    def enterCreatedName(self, ctx: JavaParser.CreatedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#createdName.
    def exitCreatedName(self, ctx: JavaParser.CreatedNameContext):
        pass

    # Enter a parse tree produced by JavaParser#coitDiamond.
    def enterCoitDiamond(self, ctx: JavaParser.CoitDiamondContext):
        pass

    # Exit a parse tree produced by JavaParser#coitDiamond.
    def exitCoitDiamond(self, ctx: JavaParser.CoitDiamondContext):
        pass

    # Enter a parse tree produced by JavaParser#innerCreator.
    def enterInnerCreator(self, ctx: JavaParser.InnerCreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#innerCreator.
    def exitInnerCreator(self, ctx: JavaParser.InnerCreatorContext):
        pass

    # Enter a parse tree produced by JavaParser#dimExpr.
    def enterDimExpr(self, ctx: JavaParser.DimExprContext):
        pass

    # Exit a parse tree produced by JavaParser#dimExpr.
    def exitDimExpr(self, ctx: JavaParser.DimExprContext):
        pass

    # Enter a parse tree produced by JavaParser#arrayCreator.
    def enterArrayCreator(self, ctx: JavaParser.ArrayCreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayCreator.
    def exitArrayCreator(self, ctx: JavaParser.ArrayCreatorContext):
        pass

    # Enter a parse tree produced by JavaParser#explicitGenericInvocation.
    def enterExplicitGenericInvocation(
        self, ctx: JavaParser.ExplicitGenericInvocationContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#explicitGenericInvocation.
    def exitExplicitGenericInvocation(
        self, ctx: JavaParser.ExplicitGenericInvocationContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def enterTypeArgumentsOrDiamond(
        self, ctx: JavaParser.TypeArgumentsOrDiamondContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def exitTypeArgumentsOrDiamond(self, ctx: JavaParser.TypeArgumentsOrDiamondContext):
        pass

    # Enter a parse tree produced by JavaParser#nonWildcardTypeArgumentsOrDiamond.
    def enterNonWildcardTypeArgumentsOrDiamond(
        self, ctx: JavaParser.NonWildcardTypeArgumentsOrDiamondContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#nonWildcardTypeArgumentsOrDiamond.
    def exitNonWildcardTypeArgumentsOrDiamond(
        self, ctx: JavaParser.NonWildcardTypeArgumentsOrDiamondContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#nonWildcardTypeArguments.
    def enterNonWildcardTypeArguments(
        self, ctx: JavaParser.NonWildcardTypeArgumentsContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#nonWildcardTypeArguments.
    def exitNonWildcardTypeArguments(
        self, ctx: JavaParser.NonWildcardTypeArgumentsContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#typeList.
    def enterTypeList(self, ctx: JavaParser.TypeListContext):
        pass

    # Exit a parse tree produced by JavaParser#typeList.
    def exitTypeList(self, ctx: JavaParser.TypeListContext):
        pass

    # Enter a parse tree produced by JavaParser#typeType.
    def enterTypeType(self, ctx: JavaParser.TypeTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#typeType.
    def exitTypeType(self, ctx: JavaParser.TypeTypeContext):
        pass

    # Enter a parse tree produced by JavaParser#primitiveType.
    def enterPrimitiveType(self, ctx: JavaParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#primitiveType.
    def exitPrimitiveType(self, ctx: JavaParser.PrimitiveTypeContext):
        pass

    # Enter a parse tree produced by JavaParser#typeArguments.
    def enterTypeArguments(self, ctx: JavaParser.TypeArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArguments.
    def exitTypeArguments(self, ctx: JavaParser.TypeArgumentsContext):
        pass

    # Enter a parse tree produced by JavaParser#superSuffix.
    def enterSuperSuffix(self, ctx: JavaParser.SuperSuffixContext):
        pass

    # Exit a parse tree produced by JavaParser#superSuffix.
    def exitSuperSuffix(self, ctx: JavaParser.SuperSuffixContext):
        pass

    # Enter a parse tree produced by JavaParser#explicitGenericInvocationSuffix.
    def enterExplicitGenericInvocationSuffix(
        self, ctx: JavaParser.ExplicitGenericInvocationSuffixContext
    ):
        pass

    # Exit a parse tree produced by JavaParser#explicitGenericInvocationSuffix.
    def exitExplicitGenericInvocationSuffix(
        self, ctx: JavaParser.ExplicitGenericInvocationSuffixContext
    ):
        pass

    # Enter a parse tree produced by JavaParser#arguments.
    def enterArguments(self, ctx: JavaParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#arguments.
    def exitArguments(self, ctx: JavaParser.ArgumentsContext):
        pass


del JavaParser
