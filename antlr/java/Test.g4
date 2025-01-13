parser grammar Test;

options {
    tokenVocab = JavaLexer;
}

typeExpression
    : '(' annotation* typeType ('&' typeType)* ')' expression
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
    : identifier typeArgumentsOrDiamond? ('.' identifier typeArgumentsOrDiamond?)*
    | primitiveType
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
    : annotation* (classOrInterfaceType | primitiveType) (annotation* '[' ']')*
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