import itertools
import unittest

from parameterized import parameterized

import jast
from utils import (
    OPERATORS,
    RIGHT_PRECEDENCE_FOR_LEFT,
    LEFT_PRECEDENCE_FOR_RIGHT,
    INSTANCEOF_HIGHER_SAME_PRECEDENCE,
    INSTANCEOF_LOWER_PRECEDENCE,
    INSTANCEOF_LOWER_SAME_PRECEDENCE,
    UNARY_OPERATORS,
)


class TestUnparse(unittest.TestCase):
    def test_identifier(self):
        tree = jast.identifier("foo")
        self.assertEqual("foo", jast.unparse(tree))

    def test_qname(self):
        tree = jast.qname([jast.identifier("foo"), jast.identifier("bar")])
        self.assertEqual("foo.bar", jast.unparse(tree))

    def test_IntLiteral(self):
        tree = jast.IntLiteral(42)
        self.assertEqual("42", jast.unparse(tree))

    def test_IntLiteral_long(self):
        tree = jast.IntLiteral(42, True)
        self.assertEqual("42l", jast.unparse(tree))

    def test_FloatLiteral(self):
        tree = jast.FloatLiteral(3.14)
        self.assertEqual("3.14", jast.unparse(tree))

    def test_FloatLiteral_double(self):
        tree = jast.FloatLiteral(3.14, True)
        self.assertEqual("3.14d", jast.unparse(tree))

    def test_BoolLiteral(self):
        tree = jast.BoolLiteral(True)
        self.assertEqual("true", jast.unparse(tree))
        tree = jast.BoolLiteral(False)
        self.assertEqual("false", jast.unparse(tree))

    def test_CharLiteral(self):
        tree = jast.CharLiteral("a")
        self.assertEqual("'a'", jast.unparse(tree))

    def test_StringLiteral(self):
        tree = jast.StringLiteral("foo")
        self.assertEqual('"foo"', jast.unparse(tree))

    def test_TextBlock(self):
        tree = jast.TextBlock("foo")
        self.assertEqual('"""foo"""', jast.unparse(tree))

    def test_NullLiteral(self):
        tree = jast.NullLiteral()
        self.assertEqual("null", jast.unparse(tree))

    def test_Abstract(self):
        tree = jast.Abstract()
        self.assertEqual("abstract", jast.unparse(tree))

    def test_Default(self):
        tree = jast.Default()
        self.assertEqual("default", jast.unparse(tree))

    def test_Final(self):
        tree = jast.Final()
        self.assertEqual("final", jast.unparse(tree))

    def test_Native(self):
        tree = jast.Native()
        self.assertEqual("native", jast.unparse(tree))

    def test_NonSealed(self):
        tree = jast.NonSealed()
        self.assertEqual("non-sealed", jast.unparse(tree))

    def test_Private(self):
        tree = jast.Private()
        self.assertEqual("private", jast.unparse(tree))

    def test_Protected(self):
        tree = jast.Protected()
        self.assertEqual("protected", jast.unparse(tree))

    def test_Public(self):
        tree = jast.Public()
        self.assertEqual("public", jast.unparse(tree))

    def test_Sealed(self):
        tree = jast.Sealed()
        self.assertEqual("sealed", jast.unparse(tree))

    def test_Static(self):
        tree = jast.Static()
        self.assertEqual("static", jast.unparse(tree))

    def test_Strictfp(self):
        tree = jast.Strictfp()
        self.assertEqual("strictfp", jast.unparse(tree))

    def test_Synchronized(self):
        tree = jast.Synchronized()
        self.assertEqual("synchronized", jast.unparse(tree))

    def test_Transient(self):
        tree = jast.Transient()
        self.assertEqual("transient", jast.unparse(tree))

    def test_Transitive(self):
        tree = jast.Transitive()
        self.assertEqual("transitive", jast.unparse(tree))

    def test_Volatile(self):
        tree = jast.Volatile()
        self.assertEqual("volatile", jast.unparse(tree))

    def test_elementvaluepair(self):
        elementvaluepair = jast.elementvaluepair(
            jast.identifier("foo"), jast.Constant(jast.IntLiteral(42))
        )
        self.assertEqual("foo=42", jast.unparse(elementvaluepair))

    def test_elementarrayinit(self):
        elementarrayinit = jast.elementarrayinit(
            [jast.Constant(jast.IntLiteral(1)), jast.Constant(jast.IntLiteral(42))]
        )
        self.assertEqual("{1, 42}", jast.unparse(elementarrayinit))

    def test_Annotation(self):
        tree = jast.Annotation(
            jast.qname([jast.identifier("foo")]),
            [
                jast.elementvaluepair(
                    jast.identifier("x"), jast.Constant(jast.IntLiteral(1))
                ),
                jast.elementvaluepair(
                    jast.identifier("y"), jast.Constant(jast.IntLiteral(42))
                ),
            ],
        )
        self.assertEqual("@foo(x=1, y=42)", jast.unparse(tree))

    def test_Void(self):
        tree = jast.Void()
        self.assertEqual("void", jast.unparse(tree))

    def test_Var(self):
        tree = jast.Var()
        self.assertEqual("var", jast.unparse(tree))

    def test_Boolean(self):
        tree = jast.Boolean()
        self.assertEqual("boolean", jast.unparse(tree))

    def test_Byte(self):
        tree = jast.Byte()
        self.assertEqual("byte", jast.unparse(tree))

    def test_Short(self):
        tree = jast.Short()
        self.assertEqual("short", jast.unparse(tree))

    def test_Int(self):
        tree = jast.Int()
        self.assertEqual("int", jast.unparse(tree))

    def test_Long(self):
        tree = jast.Long()
        self.assertEqual("long", jast.unparse(tree))

    def test_Char(self):
        tree = jast.Char()
        self.assertEqual("char", jast.unparse(tree))

    def test_Float(self):
        tree = jast.Float()
        self.assertEqual("float", jast.unparse(tree))

    def test_Double(self):
        tree = jast.Double()
        self.assertEqual("double", jast.unparse(tree))

    def test_wildcardbound_extends(self):
        tree = jast.wildcardbound(jast.Int(), extends=True)
        self.assertEqual(" extends int", jast.unparse(tree))

    def test_wildcardbound_super(self):
        tree = jast.wildcardbound(jast.Int(), super_=True)
        self.assertEqual(" super int", jast.unparse(tree))

    def test_Wildcard_bound(self):
        tree = jast.Wildcard(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            bound=jast.wildcardbound(jast.Int(), extends=True),
        )
        self.assertEqual("@foo ? extends int", jast.unparse(tree))

    def test_Wildcard_unbound(self):
        tree = jast.Wildcard()
        self.assertEqual("?", jast.unparse(tree))

    def test_typeargs(self):
        tree = jast.typeargs([jast.Int(), jast.Boolean()])
        self.assertEqual("<int, boolean>", jast.unparse(tree))

    def test_Coit(self):
        tree = jast.Coit(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
            type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
        )
        self.assertEqual("@foo bar<int, boolean>", jast.unparse(tree))

    def test_ClassType(self):
        class_type = jast.ClassType(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            coits=[
                jast.Coit(
                    id=jast.identifier("bar"),
                    type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
                ),
                jast.Coit(
                    id=jast.identifier("baz"),
                ),
            ],
        )
        self.assertEqual("@foo bar<int, boolean>.baz", jast.unparse(class_type))

    def test_dim(self):
        dim = jast.dim(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))]
        )
        self.assertEqual("@foo[]", jast.unparse(dim))

    def test_ArrayType(self):
        array_type = jast.ArrayType(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            type=jast.Int(),
            dims=[jast.dim(), jast.dim()],
        )
        self.assertEqual("@foo int[][]", jast.unparse(array_type))

    def test_variabledeclaratorid(self):
        tree = jast.variabledeclaratorid(
            jast.identifier("foo"),
        )
        self.assertEqual("foo", jast.unparse(tree))

    def test_variabledeclaratorid_dims(self):
        tree = jast.variabledeclaratorid(
            jast.identifier("foo"), dims=[jast.dim(), jast.dim()]
        )
        self.assertEqual("foo[][]", jast.unparse(tree))

    def test_typebound(self):
        tree = jast.typebound(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            types=[jast.Int(), jast.Boolean()],
        )
        self.assertEqual("@foo int & boolean", jast.unparse(tree))

    def test_typeparam(self):
        tree = jast.typeparam(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
            bound=jast.typebound(types=[jast.Int(), jast.Boolean()]),
        )
        self.assertEqual("@foo bar extends int & boolean", jast.unparse(tree))

    def test_typeparams(self):
        tree = jast.typeparams(
            [
                jast.typeparam(id=jast.identifier("foo")),
                jast.typeparam(id=jast.identifier("bar")),
            ]
        )
        self.assertEqual("<foo, bar>", jast.unparse(tree))

    def test_pattern(self):
        tree = jast.pattern(
            modifiers=[jast.Final()],
            type=jast.Int(),
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
        )
        self.assertEqual("final int @foo bar", jast.unparse(tree))

    def test_guardedpattern(self):
        tree = jast.guardedpattern(
            value=jast.pattern(
                type=jast.Int(),
                id=jast.identifier("bar"),
            ),
            conditions=[
                jast.Constant(jast.BoolLiteral(True)),
                jast.Constant(jast.IntLiteral(42)),
            ],
        )
        self.assertEqual("(int bar && true) && 42", jast.unparse(tree))

    def test_guardedpattern_no_conditions(self):
        tree = jast.guardedpattern(
            value=jast.pattern(
                type=jast.Int(),
                id=jast.identifier("bar"),
            ),
            conditions=[],
        )
        self.assertEqual("int bar", jast.unparse(tree))

    def test_Or(self):
        tree = jast.Or()
        self.assertEqual("||", jast.unparse(tree))

    def test_And(self):
        tree = jast.And()
        self.assertEqual("&&", jast.unparse(tree))

    def test_BitOr(self):
        tree = jast.BitOr()
        self.assertEqual("|", jast.unparse(tree))

    def test_BitAnd(self):
        tree = jast.BitAnd()
        self.assertEqual("&", jast.unparse(tree))

    def test_BitXor(self):
        tree = jast.BitXor()
        self.assertEqual("^", jast.unparse(tree))

    def test_Eq(self):
        tree = jast.Eq()
        self.assertEqual("==", jast.unparse(tree))

    def test_NotEq(self):
        tree = jast.NotEq()
        self.assertEqual("!=", jast.unparse(tree))

    def test_Lt(self):
        tree = jast.Lt()
        self.assertEqual("<", jast.unparse(tree))

    def test_LtE(self):
        tree = jast.LtE()
        self.assertEqual("<=", jast.unparse(tree))

    def test_Gt(self):
        tree = jast.Gt()
        self.assertEqual(">", jast.unparse(tree))

    def test_GtE(self):
        tree = jast.GtE()
        self.assertEqual(">=", jast.unparse(tree))

    def test_LShift(self):
        tree = jast.LShift()
        self.assertEqual("<<", jast.unparse(tree))

    def test_RShift(self):
        tree = jast.RShift()
        self.assertEqual(">>", jast.unparse(tree))

    def test_URShift(self):
        tree = jast.URShift()
        self.assertEqual(">>>", jast.unparse(tree))

    def test_Add(self):
        tree = jast.Add()
        self.assertEqual("+", jast.unparse(tree))

    def test_Sub(self):
        tree = jast.Sub()
        self.assertEqual("-", jast.unparse(tree))

    def test_Mult(self):
        tree = jast.Mult()
        self.assertEqual("*", jast.unparse(tree))

    def test_Div(self):
        tree = jast.Div()
        self.assertEqual("/", jast.unparse(tree))

    def test_Mod(self):
        tree = jast.Mod()
        self.assertEqual("%", jast.unparse(tree))

    def test_PreInc(self):
        tree = jast.PreInc()
        self.assertEqual("++", jast.unparse(tree))

    def test_PreDec(self):
        tree = jast.PreDec()
        self.assertEqual("--", jast.unparse(tree))

    def test_UAdd(self):
        tree = jast.UAdd()
        self.assertEqual("+", jast.unparse(tree))

    def test_USub(self):
        tree = jast.USub()
        self.assertEqual("-", jast.unparse(tree))

    def test_Invert(self):
        tree = jast.Invert()
        self.assertEqual("~", jast.unparse(tree))

    def test_Not(self):
        tree = jast.Not()
        self.assertEqual("!", jast.unparse(tree))

    def test_PostInc(self):
        tree = jast.PostInc()
        self.assertEqual("++", jast.unparse(tree))

    def test_PostDec(self):
        tree = jast.PostDec()
        self.assertEqual("--", jast.unparse(tree))

    def test_Lambda_identifier(self):
        tree = jast.Lambda(
            args=jast.identifier("x"), body=jast.Name(jast.identifier("x"))
        )
        self.assertEqual("x -> x", jast.unparse(tree))

    def test_Lambda_identifiers(self):
        tree = jast.Lambda(
            args=[jast.identifier("x"), jast.identifier("y")],
            body=jast.Name(jast.identifier("x")),
        )
        self.assertEqual("(x, y) -> x", jast.unparse(tree))

    def test_Lambda_identifiers_empty(self):
        tree = jast.Lambda(args=[], body=jast.Name(jast.identifier("x")))
        self.assertEqual("() -> x", jast.unparse(tree))

    def test_Lambda_parameters(self):
        tree = jast.Lambda(
            args=jast.params(
                parameters=[
                    jast.param(type=jast.Int(), id=jast.variabledeclaratorid("x")),
                    jast.param(type=jast.Boolean(), id=jast.variabledeclaratorid("y")),
                ]
            ),
            body=jast.Name(jast.identifier("x")),
        )
        self.assertEqual("(int x, boolean y) -> x", jast.unparse(tree))

    def test_Lambda_var_parameters(self):
        tree = jast.Lambda(
            args=jast.params(
                parameters=[
                    jast.param(type=jast.Var(), id=jast.variabledeclaratorid("x")),
                    jast.param(type=jast.Var(), id=jast.variabledeclaratorid("y")),
                ]
            ),
            body=jast.Name(jast.identifier("x")),
        )
        self.assertEqual("(var x, var y) -> x", jast.unparse(tree))

    def test_Lambda_block(self):
        tree = jast.Lambda(
            args=jast.identifier("x"),
            body=jast.Block(body=[jast.Return(jast.Name(jast.identifier("x")))]),
        )
        self.assertEqual("x -> { return x; }", jast.unparse(tree, indent=-1))

    def test_Assign(self):
        tree = jast.Assign(
            target=jast.Name(jast.identifier("x")),
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("x = 42", jast.unparse(tree))

    def test_Assign_parens_left(self):
        tree = jast.Assign(
            target=jast.Assign(
                target=jast.Name(jast.identifier("x")),
                value=jast.Name(jast.identifier("y")),
            ),
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("(x = y) = 42", jast.unparse(tree))

    def test_Assign_parens_right(self):
        tree = jast.Assign(
            target=jast.Name(jast.identifier("x")),
            value=jast.Assign(
                target=jast.Name(jast.identifier("y")),
                value=jast.Constant(jast.IntLiteral(42)),
            ),
        )
        self.assertEqual("x = y = 42", jast.unparse(tree))

    def _test_Assign_op(self, tree, op):
        self.assertEqual(f"x {op}= 42", jast.unparse(tree))

    @parameterized.expand(
        [
            (jast.Add(), "+"),
            (jast.Sub(), "-"),
            (jast.Mult(), "*"),
            (jast.Div(), "/"),
            (jast.Mod(), "%"),
            (jast.BitAnd(), "&"),
            (jast.BitOr(), "|"),
            (jast.BitXor(), "^"),
            (jast.LShift(), "<<"),
            (jast.RShift(), ">>"),
            (jast.URShift(), ">>>"),
        ]
    )
    def test_Assign_op(self, op, rep):
        tree = jast.Assign(
            target=jast.Name(jast.identifier("x")),
            value=jast.Constant(jast.IntLiteral(42)),
            op=op,
        )
        self._test_Assign_op(tree, rep)

    def test_IfExp(self):
        tree = jast.IfExp(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Constant(jast.IntLiteral(42)),
            orelse=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertEqual("true ? 42 : 0", jast.unparse(tree))

    def test_IfExp_parens_right_body(self):
        tree = jast.IfExp(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.IfExp(
                test=jast.Constant(jast.BoolLiteral(False)),
                body=jast.Constant(jast.IntLiteral(42)),
                orelse=jast.Constant(jast.IntLiteral(0)),
            ),
            orelse=jast.Constant(jast.IntLiteral(1)),
        )
        self.assertEqual("true ? false ? 42 : 0 : 1", jast.unparse(tree))

    def test_IfExp_parens_right_orelse(self):
        tree = jast.IfExp(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Constant(jast.IntLiteral(42)),
            orelse=jast.IfExp(
                test=jast.Constant(jast.BoolLiteral(False)),
                body=jast.Constant(jast.IntLiteral(0)),
                orelse=jast.Constant(jast.IntLiteral(1)),
            ),
        )
        self.assertEqual("true ? 42 : false ? 0 : 1", jast.unparse(tree))

    def test_IfExp_parens_left(self):
        tree = jast.IfExp(
            test=jast.IfExp(
                test=jast.Constant(jast.BoolLiteral(True)),
                body=jast.Constant(jast.IntLiteral(42)),
                orelse=jast.Constant(jast.IntLiteral(0)),
            ),
            body=jast.Constant(jast.IntLiteral(1)),
            orelse=jast.Constant(jast.IntLiteral(2)),
        )
        self.assertEqual("(true ? 42 : 0) ? 1 : 2", jast.unparse(tree))

    @parameterized.expand(OPERATORS)
    def test_BinOp(self, _, rep, op):
        tree = jast.BinOp(
            left=jast.Constant(jast.IntLiteral(1)),
            op=op(),
            right=jast.Constant(jast.IntLiteral(2)),
        )
        self.assertEqual(f"1 {rep} 2", jast.unparse(tree))

    @parameterized.expand(RIGHT_PRECEDENCE_FOR_LEFT)
    def test_BinOp_order(self, _, rep1, rep2, operator1, operator2):
        tree = jast.BinOp(
            left=jast.Constant(jast.IntLiteral(1)),
            op=operator1(),
            right=jast.BinOp(
                left=jast.Constant(jast.IntLiteral(2)),
                op=operator2(),
                right=jast.Constant(jast.IntLiteral(3)),
            ),
        )
        self.assertEqual(f"1 {rep1} 2 {rep2} 3", jast.unparse(tree))

    @parameterized.expand(LEFT_PRECEDENCE_FOR_RIGHT)
    def test_BinOp_order_parens(self, _, rep1, rep2, operator1, operator2):
        tree = jast.BinOp(
            left=jast.Constant(jast.IntLiteral(1)),
            op=operator1(),
            right=jast.BinOp(
                left=jast.Constant(jast.IntLiteral(2)),
                op=operator2(),
                right=jast.Constant(jast.IntLiteral(3)),
            ),
        )
        self.assertEqual(f"1 {rep1} (2 {rep2} 3)", jast.unparse(tree))

    @parameterized.expand(LEFT_PRECEDENCE_FOR_RIGHT)
    def test_BinOp_order_no_parens(self, _, rep1, rep2, operator1, operator2):
        tree = jast.BinOp(
            left=jast.BinOp(
                left=jast.Constant(jast.IntLiteral(1)),
                op=operator1(),
                right=jast.Constant(jast.IntLiteral(2)),
            ),
            op=operator2(),
            right=jast.Constant(jast.IntLiteral(3)),
        )
        self.assertEqual(f"1 {rep1} 2 {rep2} 3", jast.unparse(tree))

    @parameterized.expand(RIGHT_PRECEDENCE_FOR_LEFT)
    def test_BinOp_order_no_parens(self, _, rep1, rep2, operator1, operator2):
        tree = jast.BinOp(
            left=jast.BinOp(
                left=jast.Constant(jast.IntLiteral(1)),
                op=operator1(),
                right=jast.Constant(jast.IntLiteral(2)),
            ),
            op=operator2(),
            right=jast.Constant(jast.IntLiteral(3)),
        )
        self.assertEqual(f"(1 {rep1} 2) {rep2} 3", jast.unparse(tree))

    def test_InstanceOf(self):
        tree = jast.InstanceOf(
            value=jast.Name(jast.identifier("x")),
            type=jast.Int(),
        )
        self.assertEqual("x instanceof int", jast.unparse(tree))

    @parameterized.expand(INSTANCEOF_HIGHER_SAME_PRECEDENCE)
    def test_Instanceof_order(self, _, rep, operator):
        tree = jast.InstanceOf(
            value=jast.BinOp(
                left=jast.Name(jast.identifier("x")),
                op=operator(),
                right=jast.Name(jast.identifier("y")),
            ),
            type=jast.Int(),
        )
        self.assertEqual(f"x {rep} y instanceof int", jast.unparse(tree))

    @parameterized.expand(INSTANCEOF_LOWER_PRECEDENCE)
    def test_Instanceof_order_parens(self, _, rep, operator):
        tree = jast.InstanceOf(
            value=jast.BinOp(
                left=jast.Name(jast.identifier("x")),
                op=operator(),
                right=jast.Name(jast.identifier("y")),
            ),
            type=jast.Int(),
        )
        self.assertEqual(f"(x {rep} y) instanceof int", jast.unparse(tree))

    def test_InstanceOf_left(self):
        tree = jast.InstanceOf(
            value=jast.InstanceOf(
                value=jast.Name(jast.identifier("x")),
                type=jast.Int(),
            ),
            type=jast.Int(),
        )
        self.assertEqual("x instanceof int instanceof int", jast.unparse(tree))

    @parameterized.expand(INSTANCEOF_HIGHER_SAME_PRECEDENCE)
    def test_Instanceof_reversed(self, _, rep, operator):
        tree = jast.BinOp(
            left=jast.Name(jast.identifier("x")),
            op=operator(),
            right=jast.InstanceOf(
                value=jast.Name(jast.identifier("y")),
                type=jast.Int(),
            ),
        )
        self.assertEqual(f"x {rep} (y instanceof int)", jast.unparse(tree))

    @parameterized.expand(INSTANCEOF_LOWER_PRECEDENCE)
    def test_Instanceof_reversed_parens(self, _, rep, operator):
        tree = jast.BinOp(
            left=jast.Name(jast.identifier("x")),
            op=operator(),
            right=jast.InstanceOf(
                value=jast.Name(jast.identifier("y")),
                type=jast.Int(),
            ),
        )
        self.assertEqual(f"x {rep} y instanceof int", jast.unparse(tree))

    @parameterized.expand(INSTANCEOF_LOWER_SAME_PRECEDENCE)
    def test_Instanceof_BinOp(self, _, rep, operator):
        tree = jast.BinOp(
            left=jast.InstanceOf(
                value=jast.Name(jast.identifier("x")),
                type=jast.Int(),
            ),
            op=operator(),
            right=jast.Name(jast.identifier("y")),
        )
        self.assertEqual(f"x instanceof int {rep} y", jast.unparse(tree))

    @parameterized.expand(UNARY_OPERATORS)
    def test_UnaryOp(self, _, rep, op):
        tree = jast.UnaryOp(
            op=op(),
            operand=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual(f"{rep}42", jast.unparse(tree))

    @parameterized.expand(
        [
            tuple([*data1, *data2])
            for data1, data2 in itertools.product(UNARY_OPERATORS, UNARY_OPERATORS)
        ]
    )
    def test_UnaryOp_twice(self, _, rep1, op1, __, rep2, op2):
        tree = jast.UnaryOp(
            op=op1(),
            operand=jast.UnaryOp(
                op=op2(),
                operand=jast.Constant(jast.IntLiteral(42)),
            ),
        )
        self.assertEqual(f"{rep1}{rep2}42", jast.unparse(tree))

    def test_UnaryOp_parens(self):
        tree = jast.UnaryOp(
            op=jast.USub(),
            operand=jast.BinOp(
                left=jast.Name(jast.identifier("x")),
                op=jast.Mult(),
                right=jast.Name(jast.identifier("y")),
            ),
        )
        self.assertEqual("-(x * y)", jast.unparse(tree))

    def test_UnaryOp_no_parens(self):
        tree = jast.BinOp(
            left=jast.UnaryOp(
                op=jast.USub(),
                operand=jast.Name(jast.identifier("x")),
            ),
            op=jast.Mult(),
            right=jast.Name(jast.identifier("y")),
        )
        self.assertEqual("-x * y", jast.unparse(tree))

    def test_UnaryOp_cast(self):
        tree = jast.Cast(
            type=jast.typebound(types=[jast.Int()]),
            value=jast.UnaryOp(
                op=jast.USub(),
                operand=jast.Name(jast.identifier("x")),
            ),
        )
        self.assertEqual("(int) -x", jast.unparse(tree))

    def test_UnaryOp_cast_parens(self):
        tree = jast.UnaryOp(
            op=jast.USub(),
            operand=jast.Cast(
                type=jast.typebound(types=[jast.Int()]),
                value=jast.Name(jast.identifier("x")),
            ),
        )
        self.assertEqual("-((int) x)", jast.unparse(tree))

    def test_Cast(self):
        tree = jast.Cast(
            type=jast.typebound(types=[jast.Int()]),
            value=jast.Name(jast.identifier("x")),
        )
        self.assertEqual("(int) x", jast.unparse(tree))

    def test_Cast_twice(self):
        tree = jast.Cast(
            type=jast.typebound(types=[jast.Int()]),
            value=jast.Cast(
                type=jast.typebound(types=[jast.Long()]),
                value=jast.Name(jast.identifier("x")),
            ),
        )
        self.assertEqual("(int) (long) x", jast.unparse(tree))

    def test_Cast_type_bounds(self):
        tree = jast.Cast(
            type=jast.typebound(types=[jast.Int(), jast.Long()]),
            value=jast.Name(jast.identifier("x")),
        )
        self.assertEqual("(int & long) x", jast.unparse(tree))

    def test_Cast_parens(self):
        tree = jast.Cast(
            type=jast.typebound(types=[jast.Int()]),
            value=jast.BinOp(
                left=jast.Name(jast.identifier("x")),
                op=jast.Mult(),
                right=jast.Name(jast.identifier("y")),
            ),
        )
        self.assertEqual("(int) (x * y)", jast.unparse(tree))

    def test_Cast_no_parens(self):
        tree = jast.BinOp(
            left=jast.Cast(
                type=jast.typebound(types=[jast.Int()]),
                value=jast.Name(jast.identifier("x")),
            ),
            op=jast.Mult(),
            right=jast.Name(jast.identifier("y")),
        )
        self.assertEqual("(int) x * y", jast.unparse(tree))

    def test_Cast_annotation(self):
        tree = jast.Cast(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            type=jast.typebound(types=[jast.Int()]),
            value=jast.Name(jast.identifier("x")),
        )
        self.assertEqual("(@foo int) x", jast.unparse(tree))

    def test_NewObject(self):
        tree = jast.NewObject(
            type=jast.ClassType(
                annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
                coits=[
                    jast.Coit(
                        id=jast.identifier("bar"),
                        type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
                    ),
                    jast.Coit(
                        id=jast.identifier("baz"),
                    ),
                ],
            ),
            args=[jast.Constant(jast.IntLiteral(1)), jast.Constant(jast.IntLiteral(2))],
        )
        self.assertEqual("new @foo bar<int, boolean>.baz(1, 2)", jast.unparse(tree))

    def test_NewObject_no_args(self):
        tree = jast.NewObject(
            type=jast.ClassType(
                coits=[
                    jast.Coit(
                        id=jast.identifier("X"),
                    ),
                ],
            ),
            args=[],
        )
        self.assertEqual("new X()", jast.unparse(tree))

    def test_NewObject_with_body(self):
        tree = jast.NewObject(
            type=jast.ClassType(
                coits=[
                    jast.Coit(
                        id=jast.identifier("X"),
                    ),
                ],
            ),
            args=[],
            body=[jast.EmptyDecl(), jast.EmptyDecl()],
        )
        self.assertEqual("new X() { ; ; }", jast.unparse(tree, indent=-1))

    def test_NewArray(self):
        tree = jast.NewArray(
            type=jast.Int(),
            expr_dims=[
                jast.Constant(jast.IntLiteral(1)),
                jast.Constant(jast.IntLiteral(2)),
            ],
            dims=[jast.dim(), jast.dim()],
        )
        self.assertEqual("new int[1][2][][]", jast.unparse(tree))

    def test_NewArray_initializer(self):
        tree = jast.NewArray(
            type=jast.Int(),
            dims=[jast.dim()],
            initializer=jast.arrayinit(
                [jast.Constant(jast.IntLiteral(3)), jast.Constant(jast.IntLiteral(4))]
            ),
        )
        self.assertEqual("new int[] {3, 4}", jast.unparse(tree))
