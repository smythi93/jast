
// Generated from antlr/java/JavaParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "JavaParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by JavaParser.
 */
class  JavaParserVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by JavaParser.
   */
    virtual std::any visitCompilationUnit(JavaParser::CompilationUnitContext *context) = 0;

    virtual std::any visitDeclarationStart(JavaParser::DeclarationStartContext *context) = 0;

    virtual std::any visitStatementStart(JavaParser::StatementStartContext *context) = 0;

    virtual std::any visitExpressionStart(JavaParser::ExpressionStartContext *context) = 0;

    virtual std::any visitDirectiveStart(JavaParser::DirectiveStartContext *context) = 0;

    virtual std::any visitOrdinaryCompilationUnit(JavaParser::OrdinaryCompilationUnitContext *context) = 0;

    virtual std::any visitModularCompilationUnit(JavaParser::ModularCompilationUnitContext *context) = 0;

    virtual std::any visitPackageDeclaration(JavaParser::PackageDeclarationContext *context) = 0;

    virtual std::any visitImportDeclaration(JavaParser::ImportDeclarationContext *context) = 0;

    virtual std::any visitTypeDeclaration(JavaParser::TypeDeclarationContext *context) = 0;

    virtual std::any visitModifier(JavaParser::ModifierContext *context) = 0;

    virtual std::any visitClassOrInterfaceModifier(JavaParser::ClassOrInterfaceModifierContext *context) = 0;

    virtual std::any visitVariableModifier(JavaParser::VariableModifierContext *context) = 0;

    virtual std::any visitClassDeclaration(JavaParser::ClassDeclarationContext *context) = 0;

    virtual std::any visitClassExtends(JavaParser::ClassExtendsContext *context) = 0;

    virtual std::any visitClassImplements(JavaParser::ClassImplementsContext *context) = 0;

    virtual std::any visitClassPermits(JavaParser::ClassPermitsContext *context) = 0;

    virtual std::any visitTypeParameters(JavaParser::TypeParametersContext *context) = 0;

    virtual std::any visitTypeParameter(JavaParser::TypeParameterContext *context) = 0;

    virtual std::any visitTypeBound(JavaParser::TypeBoundContext *context) = 0;

    virtual std::any visitEnumDeclaration(JavaParser::EnumDeclarationContext *context) = 0;

    virtual std::any visitEnumConstants(JavaParser::EnumConstantsContext *context) = 0;

    virtual std::any visitEnumConstant(JavaParser::EnumConstantContext *context) = 0;

    virtual std::any visitEnumBodyDeclarations(JavaParser::EnumBodyDeclarationsContext *context) = 0;

    virtual std::any visitInterfaceDeclaration(JavaParser::InterfaceDeclarationContext *context) = 0;

    virtual std::any visitClassBody(JavaParser::ClassBodyContext *context) = 0;

    virtual std::any visitInterfaceBody(JavaParser::InterfaceBodyContext *context) = 0;

    virtual std::any visitClassBodyDeclaration(JavaParser::ClassBodyDeclarationContext *context) = 0;

    virtual std::any visitMemberDeclaration(JavaParser::MemberDeclarationContext *context) = 0;

    virtual std::any visitMethodDeclaration(JavaParser::MethodDeclarationContext *context) = 0;

    virtual std::any visitDims(JavaParser::DimsContext *context) = 0;

    virtual std::any visitDim(JavaParser::DimContext *context) = 0;

    virtual std::any visitThrows_(JavaParser::Throws_Context *context) = 0;

    virtual std::any visitMethodBody(JavaParser::MethodBodyContext *context) = 0;

    virtual std::any visitTypeTypeOrVoid(JavaParser::TypeTypeOrVoidContext *context) = 0;

    virtual std::any visitConstructorDeclaration(JavaParser::ConstructorDeclarationContext *context) = 0;

    virtual std::any visitCompactConstructorDeclaration(JavaParser::CompactConstructorDeclarationContext *context) = 0;

    virtual std::any visitFieldDeclaration(JavaParser::FieldDeclarationContext *context) = 0;

    virtual std::any visitInterfaceBodyDeclaration(JavaParser::InterfaceBodyDeclarationContext *context) = 0;

    virtual std::any visitInterfaceMemberDeclaration(JavaParser::InterfaceMemberDeclarationContext *context) = 0;

    virtual std::any visitConstDeclaration(JavaParser::ConstDeclarationContext *context) = 0;

    virtual std::any visitInterfaceMethodModifier(JavaParser::InterfaceMethodModifierContext *context) = 0;

    virtual std::any visitInterfaceMethodDeclaration(JavaParser::InterfaceMethodDeclarationContext *context) = 0;

    virtual std::any visitVariableDeclarators(JavaParser::VariableDeclaratorsContext *context) = 0;

    virtual std::any visitVariableDeclarator(JavaParser::VariableDeclaratorContext *context) = 0;

    virtual std::any visitVariableDeclaratorId(JavaParser::VariableDeclaratorIdContext *context) = 0;

    virtual std::any visitVariableInitializer(JavaParser::VariableInitializerContext *context) = 0;

    virtual std::any visitArrayInitializer(JavaParser::ArrayInitializerContext *context) = 0;

    virtual std::any visitClassOrInterfaceType(JavaParser::ClassOrInterfaceTypeContext *context) = 0;

    virtual std::any visitCoit(JavaParser::CoitContext *context) = 0;

    virtual std::any visitTypeArgument(JavaParser::TypeArgumentContext *context) = 0;

    virtual std::any visitQualifiedNameList(JavaParser::QualifiedNameListContext *context) = 0;

    virtual std::any visitFormalParameters(JavaParser::FormalParametersContext *context) = 0;

    virtual std::any visitReceiverParameter(JavaParser::ReceiverParameterContext *context) = 0;

    virtual std::any visitFormalParameterList(JavaParser::FormalParameterListContext *context) = 0;

    virtual std::any visitFormalParameter(JavaParser::FormalParameterContext *context) = 0;

    virtual std::any visitLastFormalParameter(JavaParser::LastFormalParameterContext *context) = 0;

    virtual std::any visitLambdaLVTIList(JavaParser::LambdaLVTIListContext *context) = 0;

    virtual std::any visitLambdaLVTIParameter(JavaParser::LambdaLVTIParameterContext *context) = 0;

    virtual std::any visitQualifiedName(JavaParser::QualifiedNameContext *context) = 0;

    virtual std::any visitLiteral(JavaParser::LiteralContext *context) = 0;

    virtual std::any visitIntegerLiteral(JavaParser::IntegerLiteralContext *context) = 0;

    virtual std::any visitFloatLiteral(JavaParser::FloatLiteralContext *context) = 0;

    virtual std::any visitAnnotation(JavaParser::AnnotationContext *context) = 0;

    virtual std::any visitElementValuePairs(JavaParser::ElementValuePairsContext *context) = 0;

    virtual std::any visitElementValuePair(JavaParser::ElementValuePairContext *context) = 0;

    virtual std::any visitElementValue(JavaParser::ElementValueContext *context) = 0;

    virtual std::any visitElementValueArrayInitializer(JavaParser::ElementValueArrayInitializerContext *context) = 0;

    virtual std::any visitAnnotationTypeDeclaration(JavaParser::AnnotationTypeDeclarationContext *context) = 0;

    virtual std::any visitAnnotationTypeBody(JavaParser::AnnotationTypeBodyContext *context) = 0;

    virtual std::any visitAnnotationTypeElementDeclaration(JavaParser::AnnotationTypeElementDeclarationContext *context) = 0;

    virtual std::any visitAnnotationTypeElementRest(JavaParser::AnnotationTypeElementRestContext *context) = 0;

    virtual std::any visitAnnotationConstantDeclaration(JavaParser::AnnotationConstantDeclarationContext *context) = 0;

    virtual std::any visitAnnotationMethodDeclaration(JavaParser::AnnotationMethodDeclarationContext *context) = 0;

    virtual std::any visitDefaultValue(JavaParser::DefaultValueContext *context) = 0;

    virtual std::any visitModuleDeclaration(JavaParser::ModuleDeclarationContext *context) = 0;

    virtual std::any visitModuleBody(JavaParser::ModuleBodyContext *context) = 0;

    virtual std::any visitModuleDirective(JavaParser::ModuleDirectiveContext *context) = 0;

    virtual std::any visitRequiresModifier(JavaParser::RequiresModifierContext *context) = 0;

    virtual std::any visitRecordDeclaration(JavaParser::RecordDeclarationContext *context) = 0;

    virtual std::any visitRecordComponentList(JavaParser::RecordComponentListContext *context) = 0;

    virtual std::any visitRecordComponent(JavaParser::RecordComponentContext *context) = 0;

    virtual std::any visitRecordBody(JavaParser::RecordBodyContext *context) = 0;

    virtual std::any visitRecordBodyDeclaration(JavaParser::RecordBodyDeclarationContext *context) = 0;

    virtual std::any visitBlock(JavaParser::BlockContext *context) = 0;

    virtual std::any visitBlockStatement(JavaParser::BlockStatementContext *context) = 0;

    virtual std::any visitLocalVariableDeclaration(JavaParser::LocalVariableDeclarationContext *context) = 0;

    virtual std::any visitIdentifier(JavaParser::IdentifierContext *context) = 0;

    virtual std::any visitTypeIdentifier(JavaParser::TypeIdentifierContext *context) = 0;

    virtual std::any visitLocalTypeDeclaration(JavaParser::LocalTypeDeclarationContext *context) = 0;

    virtual std::any visitStatement(JavaParser::StatementContext *context) = 0;

    virtual std::any visitSwitchBlock(JavaParser::SwitchBlockContext *context) = 0;

    virtual std::any visitCatchClause(JavaParser::CatchClauseContext *context) = 0;

    virtual std::any visitCatchType(JavaParser::CatchTypeContext *context) = 0;

    virtual std::any visitFinallyBlock(JavaParser::FinallyBlockContext *context) = 0;

    virtual std::any visitResourceSpecification(JavaParser::ResourceSpecificationContext *context) = 0;

    virtual std::any visitResources(JavaParser::ResourcesContext *context) = 0;

    virtual std::any visitResource(JavaParser::ResourceContext *context) = 0;

    virtual std::any visitSwitchBlockStatementGroup(JavaParser::SwitchBlockStatementGroupContext *context) = 0;

    virtual std::any visitSwitchLabel(JavaParser::SwitchLabelContext *context) = 0;

    virtual std::any visitForInit(JavaParser::ForInitContext *context) = 0;

    virtual std::any visitParExpression(JavaParser::ParExpressionContext *context) = 0;

    virtual std::any visitExpressionList(JavaParser::ExpressionListContext *context) = 0;

    virtual std::any visitMethodCall(JavaParser::MethodCallContext *context) = 0;

    virtual std::any visitPostfixExpression(JavaParser::PostfixExpressionContext *context) = 0;

    virtual std::any visitPrefixExpression(JavaParser::PrefixExpressionContext *context) = 0;

    virtual std::any visitTypeExpression(JavaParser::TypeExpressionContext *context) = 0;

    virtual std::any visitMultiplicativeExpression(JavaParser::MultiplicativeExpressionContext *context) = 0;

    virtual std::any visitAdditiveExpression(JavaParser::AdditiveExpressionContext *context) = 0;

    virtual std::any visitShiftExpression(JavaParser::ShiftExpressionContext *context) = 0;

    virtual std::any visitRelationalExpression(JavaParser::RelationalExpressionContext *context) = 0;

    virtual std::any visitEqualityExpression(JavaParser::EqualityExpressionContext *context) = 0;

    virtual std::any visitBitwiseAndExpression(JavaParser::BitwiseAndExpressionContext *context) = 0;

    virtual std::any visitBitwiseXorExpression(JavaParser::BitwiseXorExpressionContext *context) = 0;

    virtual std::any visitBitwiseOrExpression(JavaParser::BitwiseOrExpressionContext *context) = 0;

    virtual std::any visitLogicalAndExpression(JavaParser::LogicalAndExpressionContext *context) = 0;

    virtual std::any visitLogicalOrExpression(JavaParser::LogicalOrExpressionContext *context) = 0;

    virtual std::any visitTernaryExpression(JavaParser::TernaryExpressionContext *context) = 0;

    virtual std::any visitAssignmentExpression(JavaParser::AssignmentExpressionContext *context) = 0;

    virtual std::any visitExpression(JavaParser::ExpressionContext *context) = 0;

    virtual std::any visitPattern(JavaParser::PatternContext *context) = 0;

    virtual std::any visitLambdaExpression(JavaParser::LambdaExpressionContext *context) = 0;

    virtual std::any visitLambdaParameters(JavaParser::LambdaParametersContext *context) = 0;

    virtual std::any visitLambdaBody(JavaParser::LambdaBodyContext *context) = 0;

    virtual std::any visitExplicitGenericInvocationExpression(JavaParser::ExplicitGenericInvocationExpressionContext *context) = 0;

    virtual std::any visitThisExpression(JavaParser::ThisExpressionContext *context) = 0;

    virtual std::any visitMemberReferenceExpression(JavaParser::MemberReferenceExpressionContext *context) = 0;

    virtual std::any visitMethodCallExpression(JavaParser::MethodCallExpressionContext *context) = 0;

    virtual std::any visitMethodReferenceExpression(JavaParser::MethodReferenceExpressionContext *context) = 0;

    virtual std::any visitParExpr(JavaParser::ParExprContext *context) = 0;

    virtual std::any visitLiteralExpression(JavaParser::LiteralExpressionContext *context) = 0;

    virtual std::any visitClassExpression(JavaParser::ClassExpressionContext *context) = 0;

    virtual std::any visitSuperExpression(JavaParser::SuperExpressionContext *context) = 0;

    virtual std::any visitArrayAccessExpression(JavaParser::ArrayAccessExpressionContext *context) = 0;

    virtual std::any visitIdentifierExpression(JavaParser::IdentifierExpressionContext *context) = 0;

    virtual std::any visitSwitchExpression(JavaParser::SwitchExpressionContext *context) = 0;

    virtual std::any visitSwitchLabeledRule(JavaParser::SwitchLabeledRuleContext *context) = 0;

    virtual std::any visitGuardedPattern(JavaParser::GuardedPatternContext *context) = 0;

    virtual std::any visitSwitchRuleOutcome(JavaParser::SwitchRuleOutcomeContext *context) = 0;

    virtual std::any visitClassType(JavaParser::ClassTypeContext *context) = 0;

    virtual std::any visitCreator(JavaParser::CreatorContext *context) = 0;

    virtual std::any visitObjectCreator(JavaParser::ObjectCreatorContext *context) = 0;

    virtual std::any visitCreatedName(JavaParser::CreatedNameContext *context) = 0;

    virtual std::any visitCoitDiamond(JavaParser::CoitDiamondContext *context) = 0;

    virtual std::any visitInnerCreator(JavaParser::InnerCreatorContext *context) = 0;

    virtual std::any visitDimExpr(JavaParser::DimExprContext *context) = 0;

    virtual std::any visitArrayCreator(JavaParser::ArrayCreatorContext *context) = 0;

    virtual std::any visitExplicitGenericInvocation(JavaParser::ExplicitGenericInvocationContext *context) = 0;

    virtual std::any visitTypeArgumentsOrDiamond(JavaParser::TypeArgumentsOrDiamondContext *context) = 0;

    virtual std::any visitNonWildcardTypeArgumentsOrDiamond(JavaParser::NonWildcardTypeArgumentsOrDiamondContext *context) = 0;

    virtual std::any visitNonWildcardTypeArguments(JavaParser::NonWildcardTypeArgumentsContext *context) = 0;

    virtual std::any visitTypeList(JavaParser::TypeListContext *context) = 0;

    virtual std::any visitTypeType(JavaParser::TypeTypeContext *context) = 0;

    virtual std::any visitPrimitiveType(JavaParser::PrimitiveTypeContext *context) = 0;

    virtual std::any visitTypeArguments(JavaParser::TypeArgumentsContext *context) = 0;

    virtual std::any visitSuperSuffix(JavaParser::SuperSuffixContext *context) = 0;

    virtual std::any visitExplicitGenericInvocationSuffix(JavaParser::ExplicitGenericInvocationSuffixContext *context) = 0;

    virtual std::any visitArguments(JavaParser::ArgumentsContext *context) = 0;


};

