/*
 [The "BSD licence"]
 Copyright (c) 2013 Terence Parr, Sam Harwell
 Copyright (c) 2017 Ivan Kochurkin (upgrade to Java 8)
 Copyright (c) 2021 Michał Lorek (upgrade to Java 11)
 Copyright (c) 2022 Michał Lorek (upgrade to Java 17)
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. The name of the author may not be used to endorse or promote products
    derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

// $antlr-format alignTrailingComments true, columnLimit 150, minEmptyLines 1, maxEmptyLinesToKeep 1, reflowComments
// false, useTab false
// $antlr-format allowShortRulesOnASingleLine false, allowShortBlocksOnASingleLine true, alignSemicolons hanging,
// alignColons hanging

parser grammar JavaParser;

options {
    tokenVocab = JavaLexer;
}

compilationUnit
    : ordinaryCompilationUnit EOF
    | modularCompilationUnit EOF
    ;

declarationStart
    : packageDeclaration EOF
    | importDeclaration EOF
    | moduleDeclaration EOF
    | fieldDeclaration EOF
    | methodDeclaration EOF
    | interfaceMethodDeclaration EOF
    | STATIC? block EOF
    | constructorDeclaration EOF
    | compactConstructorDeclaration EOF
    | interfaceDeclaration EOF
    | annotationMethodDeclaration EOF
    | annotationConstantDeclaration EOF
    | annotationTypeDeclaration EOF
    | classDeclaration EOF
    | enumDeclaration EOF
    | recordDeclaration EOF
    ;

statementStart
    : blockStatement EOF
    ;

expressionStart
    : expression EOF
    ;

ordinaryCompilationUnit
    : packageDeclaration? (importDeclaration | ';')* (typeDeclaration | ';')*
    ;

modularCompilationUnit
    : (importDeclaration | ';')* moduleDeclaration
    ;

packageDeclaration
    : annotation* PACKAGE qualifiedName ';'
    ;

importDeclaration
    : IMPORT STATIC? qualifiedName ('.' '*')? ';'
    ;

typeDeclaration
    : classOrInterfaceModifier* (
        classDeclaration
        | enumDeclaration
        | interfaceDeclaration
        | annotationTypeDeclaration
        | recordDeclaration
    )
    ;

modifier
    : classOrInterfaceModifier
    | NATIVE
    | SYNCHRONIZED
    | TRANSIENT
    | VOLATILE
    ;

classOrInterfaceModifier
    : annotation
    | PUBLIC
    | PROTECTED
    | PRIVATE
    | STATIC
    | ABSTRACT
    | FINAL // FINAL for class only -- does not apply to interfaces
    | STRICTFP
    | SEALED     // Java17
    | NON_SEALED // Java17
    ;

variableModifier
    : FINAL
    | annotation
    ;

classDeclaration
    : CLASS identifier typeParameters? classExtends? classImplements? classPermits? classBody
    ;

classExtends:
    EXTENDS typeType
    ;

classImplements:
    IMPLEMENTS typeList
    ;

classPermits:
    PERMITS typeList
    ;

typeParameters
    : '<' typeParameter (',' typeParameter)* '>'
    ;

typeParameter
    : annotation* identifier (EXTENDS typeBound)?
    ;

typeBound
    : annotation* typeType ('&' typeType)*
    ;

enumDeclaration
    : ENUM identifier classImplements? '{' enumConstants? ','? enumBodyDeclarations? '}'
    ;

enumConstants
    : enumConstant (',' enumConstant)*
    ;

enumConstant
    : annotation* identifier arguments? classBody?
    ;

enumBodyDeclarations
    : ';' classBodyDeclaration*
    ;

interfaceDeclaration
    : INTERFACE identifier typeParameters? classExtends? classImplements? interfaceBody
    ;

classBody
    : '{' classBodyDeclaration* '}'
    ;

interfaceBody
    : '{' interfaceBodyDeclaration* '}'
    ;

classBodyDeclaration
    : ';'
    | STATIC? block
    | modifier* memberDeclaration
    ;

memberDeclaration
    : recordDeclaration //Java17
    | methodDeclaration
    | fieldDeclaration
    | constructorDeclaration
    | interfaceDeclaration
    | annotationTypeDeclaration
    | classDeclaration
    | enumDeclaration
    ;

/* We use rule this even for void methods which cannot have [] after parameters.
   This simplifies grammar and we can consider void to be a type, which
   renders the [] matching as a context-sensitive issue or a semantic check
   for invalid return type after parsing.
 */
methodDeclaration
    : typeParameters? typeTypeOrVoid identifier formalParameters dims? throws_? methodBody
    ;

dims
    : dim dim*
    ;

dim
    : annotation* '[' ']'
    ;

throws_
    : THROWS qualifiedNameList
    ;

methodBody
    : block
    | ';'
    ;

typeTypeOrVoid
    : typeType
    | VOID
    ;

constructorDeclaration
    : typeParameters? identifier formalParameters throws_? constructorBody = block
    ;

compactConstructorDeclaration
    : modifier* identifier constructorBody = block
    ;

fieldDeclaration
    : typeType variableDeclarators ';'
    ;

interfaceBodyDeclaration
    : modifier* interfaceMemberDeclaration
    | ';'
    ;

interfaceMemberDeclaration
    : recordDeclaration // Java17
    | constDeclaration
    | interfaceMethodDeclaration
    | interfaceDeclaration
    | annotationTypeDeclaration
    | classDeclaration
    | enumDeclaration
    ;

constDeclaration
    : typeType variableDeclarators ';'
    ;

// Early versions of Java allows brackets after the method name, eg.
// public int[] return2DArray() [] { ... }
// is the same as
// public int[][] return2DArray() { ... }

// Java8
interfaceMethodModifier
    : annotation
    | PUBLIC
    | ABSTRACT
    | DEFAULT
    | STATIC
    | STRICTFP
    ;

interfaceMethodDeclaration
    : interfaceMethodModifier* typeParameters? annotation* typeTypeOrVoid
      identifier formalParameters dims? throws_? methodBody
    ;

variableDeclarators
    : variableDeclarator (',' variableDeclarator)*
    ;

variableDeclarator
    : variableDeclaratorId ('=' variableInitializer)?
    ;

variableDeclaratorId
    : identifier dims?
    ;

variableInitializer
    : arrayInitializer
    | expression
    ;

arrayInitializer
    : '{' (variableInitializer (',' variableInitializer)* ','?)? '}'
    ;

classOrInterfaceType
    : (coit '.')* coit
    ;

coit
    : typeIdentifier typeArguments?
    ;

typeArgument
    : typeType
    | annotation* '?' ((EXTENDS | SUPER) typeType)?
    ;

qualifiedNameList
    : qualifiedName (',' qualifiedName)*
    ;

formalParameters
    : '(' (
        receiverParameter?
        | receiverParameter (',' formalParameterList)?
        | formalParameterList?
    ) ')'
    ;

receiverParameter
    : typeType (identifier '.')* THIS
    ;

formalParameterList
    : formalParameter (',' formalParameter)* (',' lastFormalParameter)?
    | lastFormalParameter
    ;

formalParameter
    : variableModifier* typeType variableDeclaratorId
    ;

lastFormalParameter
    : variableModifier* typeType annotation* '...' variableDeclaratorId
    ;

// local variable type inference
lambdaLVTIList
    : lambdaLVTIParameter (',' lambdaLVTIParameter)*
    ;

lambdaLVTIParameter
    : variableModifier* VAR identifier
    ;

qualifiedName
    : identifier ('.' identifier)*
    ;

literal
    : integerLiteral
    | floatLiteral
    | CHAR_LITERAL
    | STRING_LITERAL
    | BOOL_LITERAL
    | NULL_LITERAL
    | TEXT_BLOCK // Java17
    ;

integerLiteral
    : DECIMAL_LITERAL
    | HEX_LITERAL
    | OCT_LITERAL
    | BINARY_LITERAL
    ;

floatLiteral
    : FLOAT_LITERAL
    | HEX_FLOAT_LITERAL
    ;

// ANNOTATIONS

annotation
    : '@' qualifiedName (
        '(' ( elementValuePairs | elementValue)? ')'
    )?
    ;

elementValuePairs
    : elementValuePair (',' elementValuePair)*
    ;

elementValuePair
    : identifier '=' elementValue
    ;

elementValue
    : expression
    | annotation
    | elementValueArrayInitializer
    ;

elementValueArrayInitializer
    : '{' (elementValue (',' elementValue)*)? ','? '}'
    ;

annotationTypeDeclaration
    : '@' INTERFACE identifier annotationTypeBody
    ;

annotationTypeBody
    : '{' annotationTypeElementDeclaration* '}'
    ;

annotationTypeElementDeclaration
    : modifier* annotationTypeElementRest
    | ';' // this is not allowed by the grammar, but apparently allowed by the actual compiler
    ;

annotationTypeElementRest
    : annotationConstantDeclaration
    | annotationMethodDeclaration
    | classDeclaration ';'?
    | interfaceDeclaration ';'?
    | enumDeclaration ';'?
    | annotationTypeDeclaration ';'?
    | recordDeclaration ';'? // Java17
    ;

annotationConstantDeclaration
    : typeType variableDeclarators ';'
    ;

annotationMethodDeclaration
    : typeType identifier '(' ')' defaultValue? ';'
    ;

defaultValue
    : DEFAULT elementValue
    ;

// MODULES - Java9

moduleDeclaration
    : OPEN? MODULE qualifiedName moduleBody
    ;

moduleBody
    : '{' moduleDirective* '}'
    ;

moduleDirective
    : REQUIRES requiresModifier* qualifiedName ';'
    | EXPORTS qualifiedName (TO qualifiedName)? ';'
    | OPENS qualifiedName (TO qualifiedName)? ';'
    | USES qualifiedName ';'
    | PROVIDES qualifiedName WITH qualifiedName ';'
    ;

requiresModifier
    : TRANSITIVE
    | STATIC
    ;

// RECORDS - Java 17

recordDeclaration
    : RECORD identifier typeParameters? '(' recordComponentList? ')' classImplements? recordBody
    ;

recordComponentList
    : recordComponent (',' recordComponent)*
    ;

recordComponent
    : typeType identifier
    ;

recordBody
    : '{' recordBodyDeclaration* '}'
    ;

recordBodyDeclaration
    : classBodyDeclaration
    | compactConstructorDeclaration
    ;

// STATEMENTS / BLOCKS

block
    : '{' blockStatement* '}'
    ;

blockStatement
    : localVariableDeclaration ';'
    | localTypeDeclaration
    | statement
    ;

localVariableDeclaration
    : variableModifier* (VAR identifier '=' expression | typeType variableDeclarators)
    ;

identifier
    : IDENTIFIER
    | MODULE
    | OPEN
    | REQUIRES
    | EXPORTS
    | OPENS
    | TO
    | USES
    | PROVIDES
    | WITH
    | TRANSITIVE
    | YIELD
    | SEALED
    | PERMITS
    | RECORD
    | VAR
    ;

typeIdentifier // Identifiers that are not restricted for type declarations
    : IDENTIFIER
    | MODULE
    | OPEN
    | REQUIRES
    | EXPORTS
    | OPENS
    | TO
    | USES
    | PROVIDES
    | WITH
    | TRANSITIVE
    | SEALED
    | PERMITS
    | RECORD
    ;

localTypeDeclaration
    : classOrInterfaceModifier* (classDeclaration | interfaceDeclaration | recordDeclaration)
    ;

statement
    : blockLabel = block
    | ASSERT expression (':' expression)? ';'
    | IF parExpression statement (ELSE statement)?
    | FOR '(' forInit? ';' expression? ';' forUpdate = expressionList? ')' statement
    | FOR '(' variableModifier* (typeType | VAR) variableDeclaratorId ':' expression  ')' statement
    | WHILE parExpression statement
    | DO statement WHILE parExpression ';'
    | TRY block (catchClause+ finallyBlock? | finallyBlock)
    | TRY resourceSpecification block catchClause* finallyBlock?
    | SWITCH parExpression switchBlock
    | SYNCHRONIZED parExpression block
    | RETURN expression? ';'
    | THROW expression ';'
    | BREAK identifier? ';'
    | CONTINUE identifier? ';'
    | YIELD expression ';' // Java17
    | SEMI
    | statementExpression = expression ';'
    | identifierLabel = identifier ':' statement
    ;

switchBlock
    : '{' switchBlockStatementGroup* switchLabel* '}'
    ;

catchClause
    : CATCH '(' variableModifier* catchType identifier ')' block
    ;

catchType
    : qualifiedName ('|' qualifiedName)*
    ;

finallyBlock
    : FINALLY block
    ;

resourceSpecification
    : '(' resources ';'? ')'
    ;

resources
    : resource (';' resource)*
    ;

resource
    : variableModifier* (classOrInterfaceType variableDeclaratorId | VAR identifier) '=' expression
    | qualifiedName
    ;

/** Matches cases then statements, both of which are mandatory.
 *  To handle empty cases at the end, we add switchLabel* to statement.
 */

switchBlockStatementGroup
    : switchLabel+ blockStatement+
    ;

switchLabel
    : CASE (
        constantExpression = expression
        | enumConstantName = IDENTIFIER
        | typeType varName = identifier
    ) ':'
    | DEFAULT ':'
    ;

forInit
    : localVariableDeclaration
    | expressionList
    ;

// EXPRESSIONS

parExpression
    : '(' expression ')'
    ;

expressionList
    : expression (',' expression)*
    ;

methodCall
    : (identifier | THIS | SUPER) arguments
    ;


postfixExpression
    : postfixExpression postfix = ('++' | '--') // Level 15
    | switchExpression
    ;

prefixExpression
    : prefix = ('+' | '-' | '++' | '--' | '~' | '!') prefixExpression // Level 14
    | postfixExpression
    ;

typeExpression
    : '(' annotation* typeType ('&' typeType)* ')' typeExpression // Level 13
    | NEW creator
    | prefixExpression
    ;

multiplicativeExpression
    : multiplicativeExpression bop = ('*' | '/' | '%') typeExpression // Level 12
    | typeExpression
    ;

additiveExpression
    : additiveExpression bop = ('+' | '-') multiplicativeExpression // Level 11
    | multiplicativeExpression
    ;

shiftExpression
    : shiftExpression ('<' '<' | '>' '>' '>' | '>' '>') additiveExpression // Level 10
    | additiveExpression
    ;

relationalExpression
    : relationalExpression bop = ('<=' | '>=' | '>' | '<') shiftExpression // Level 9
    | relationalExpression bop = INSTANCEOF (typeType | pattern) // Level 9
    | shiftExpression
    ;

equalityExpression
    : equalityExpression bop = ('==' | '!=') relationalExpression // Level 8
    | relationalExpression
    ;

bitwiseAndExpression
    : bitwiseAndExpression '&' equalityExpression // Level 7
    | equalityExpression
    ;

bitwiseXorExpression
    : bitwiseXorExpression '^' bitwiseAndExpression // Level 6
    | bitwiseAndExpression
    ;

bitwiseOrExpression
    : bitwiseOrExpression '|' bitwiseXorExpression // Level 5
    | bitwiseXorExpression
    ;

logicalAndExpression
    : logicalAndExpression '&&' bitwiseOrExpression // Level 4
    | bitwiseOrExpression
    ;

logicalOrExpression
    : logicalOrExpression '||' logicalAndExpression // Level 3
    | logicalAndExpression
    ;

ternaryExpression
    : logicalOrExpression bop = '?' expression ':' ternaryExpression // Level 2
    | logicalOrExpression bop = '?' expression ':' lambdaExpression // Level 2
    | logicalOrExpression
    ;

assignmentExpression
    : ternaryExpression bop = (
        '='
        | '+='
        | '-='
        | '*='
        | '/='
        | '&='
        | '|='
        | '^='
        | '>>='
        | '>>>='
        | '<<='
        | '%='
    ) expression
    | ternaryExpression
    ;

expression
    : assignmentExpression
    | lambdaExpression
    ;

// Java17
pattern
    : variableModifier* typeType annotation* identifier
    ;

// Java8
lambdaExpression
    : lambdaParameters '->' lambdaBody
    ;

// Java8
lambdaParameters
    : identifier
    | '(' formalParameterList? ')'
    | '(' identifier (',' identifier)* ')'
    | '(' lambdaLVTIList? ')'
    ;

// Java8
lambdaBody
    : expression
    | block
    ;

primary
    : '(' expression ')'                                            #ParExpr
    | THIS                                                          #ThisExpression
    | SUPER                                                         #SuperExpression
    | literal                                                       #LiteralExpression
    | identifier                                                    #IdentifierExpression
    | typeTypeOrVoid '.' CLASS                                      #ClassExpression
    | nonWildcardTypeArguments (explicitGenericInvocationSuffix | THIS arguments) #ExplicitGenericInvocationExpression
    | primary '[' expression ']'                                    #ArrayAccessExpression
    | primary bop = '.' (
        identifier
        | methodCall
        | THIS
        | NEW nonWildcardTypeArguments? innerCreator
        | SUPER superSuffix
        | explicitGenericInvocation
    )                                                               #MemberReferenceExpression
    // Method calls and method references are part of primary, and hence level 16 precedence
    | methodCall                                                    #MethodCallExpression
    | primary '::' typeArguments? identifier                     #MethodReferenceExpression
    | typeType '::' (typeArguments? identifier | NEW)               #MethodReferenceExpression
    | classType '::' typeArguments? NEW                             #MethodReferenceExpression
    ;

// Java17
switchExpression
    : SWITCH parExpression '{' switchLabeledRule* '}'
    | primary
    ;

// Java17
switchLabeledRule
    : CASE (expressionList | NULL_LITERAL | guardedPattern) (ARROW | COLON) switchRuleOutcome
    | DEFAULT (ARROW | COLON) switchRuleOutcome
    ;

// Java17
guardedPattern
    : '(' guardedPattern ')'
    | variableModifier* typeType annotation* identifier ('&&' expression)*
    | guardedPattern '&&' expression
    ;

// Java17
switchRuleOutcome
    : block
    | blockStatement*
    ;

classType
    : (classOrInterfaceType '.')? annotation* identifier typeArguments?
    ;

creator
    : objectCreator
    | arrayCreator
    ;

objectCreator
    : nonWildcardTypeArguments? createdName arguments classBody?
    ;

createdName
    : coitDiamond ('.' coitDiamond)*
    | primitiveType
    ;

 coitDiamond
    : identifier typeArgumentsOrDiamond?
    ;

innerCreator
    : identifier nonWildcardTypeArgumentsOrDiamond? arguments classBody?
    ;

dimExpr
    : '[' expression ']'
    ;

arrayCreator
    : createdName dims arrayInitializer
    | createdName dimExpr+ dims?
    ;

explicitGenericInvocation
    : nonWildcardTypeArguments explicitGenericInvocationSuffix
    ;

typeArgumentsOrDiamond
    : '<' '>'
    | typeArguments
    ;

nonWildcardTypeArgumentsOrDiamond
    : '<' '>'
    | nonWildcardTypeArguments
    ;

nonWildcardTypeArguments
    : '<' typeList '>'
    ;

typeList
    : typeType (',' typeType)*
    ;

typeType
    : annotation* (classOrInterfaceType | primitiveType) dims?
    ;

primitiveType
    : BOOLEAN
    | CHAR
    | BYTE
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    ;

typeArguments
    : '<' typeArgument (',' typeArgument)* '>'
    ;

superSuffix
    : arguments
    | '.' typeArguments? identifier arguments?
    ;

explicitGenericInvocationSuffix
    : SUPER superSuffix
    | identifier arguments
    ;

arguments
    : '(' expressionList? ')'
    ;