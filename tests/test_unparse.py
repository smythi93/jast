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
    POST_OPERATORS,
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
        tree = jast.TextBlock(["foo"])
        self.assertEqual('"""\nfoo"""', jast.unparse(tree, indent=-1))

    def test_TextBlock_new_line(self):
        tree = jast.TextBlock(["foo", ""])
        self.assertEqual('"""\n    foo\n    """', jast.unparse(tree))

    def test_TextBlock_different_indents(self):
        tree = jast.TextBlock(["foo", " bar", "", "\tbaz", ""])
        self.assertEqual(
            '"""\n    foo\n     bar\n    \n    \tbaz\n    """', jast.unparse(tree)
        )

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

    def test_NewObject_all(self):
        tree = jast.NewObject(
            type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
            type=jast.ClassType(
                coits=[
                    jast.Coit(
                        id=jast.identifier("bar"),
                    ),
                    jast.Coit(
                        id=jast.identifier("baz"),
                        type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
                    ),
                ],
            ),
            args=[jast.Constant(jast.IntLiteral(1)), jast.Constant(jast.IntLiteral(2))],
            body=[jast.EmptyDecl(), jast.EmptyDecl()],
        )
        self.assertEqual(
            "new<int, boolean> bar.baz<int, boolean>(1, 2) { ; ; }",
            jast.unparse(tree, indent=-1),
        )

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
            init=jast.arrayinit(
                [jast.Constant(jast.IntLiteral(3)), jast.Constant(jast.IntLiteral(4))]
            ),
        )
        self.assertEqual("new int[] {3, 4}", jast.unparse(tree))

    @parameterized.expand(POST_OPERATORS)
    def test_PostOp(self, _, rep, operator):
        tree = jast.PostOp(
            op=operator(),
            operand=jast.Name(jast.identifier("x")),
        )
        self.assertEqual(f"x{rep}", jast.unparse(tree))

    def test_PostOp_twice(self):
        tree = jast.PostOp(
            op=jast.PostDec(),
            operand=jast.PostOp(
                op=jast.PostInc(),
                operand=jast.Name(jast.identifier("x")),
            ),
        )
        self.assertEqual("x++--", jast.unparse(tree))

    @parameterized.expand(
        [
            [*first, *second]
            for first, second in itertools.product(POST_OPERATORS, UNARY_OPERATORS)
        ]
    )
    def test_postOp_parens(self, _, rep, operator, __, rep2, operator2):
        tree = jast.UnaryOp(
            op=operator2(),
            operand=jast.PostOp(
                op=operator(),
                operand=jast.Name(jast.identifier("x")),
            ),
        )
        self.assertEqual(f"{rep2}x{rep}", jast.unparse(tree))

    @parameterized.expand(
        [
            [*first, *second]
            for first, second in itertools.product(POST_OPERATORS, UNARY_OPERATORS)
        ]
    )
    def test_postOp_parens(self, _, rep, operator, __, rep2, operator2):
        tree = jast.PostOp(
            op=operator(),
            operand=jast.UnaryOp(
                op=operator2(),
                operand=jast.Name(jast.identifier("x")),
            ),
        )
        self.assertEqual(f"({rep2}x){rep}", jast.unparse(tree))

    def test_ExpCase(self):
        tree = jast.ExpCase()
        self.assertEqual("case", jast.unparse(tree))

    def test_ExpDefault(self):
        tree = jast.ExpDefault()
        self.assertEqual("default", jast.unparse(tree))

    def test_switchexprule_case(self):
        tree = jast.switchexprule(
            label=jast.ExpCase(),
            cases=[jast.Constant(jast.IntLiteral(42))],
            arrow=True,
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )
        self.assertEqual("case 42 -> return 24;", jast.unparse(tree, indent=-1))

    def test_switchexprule_default(self):
        switchexprule = jast.switchexprule(
            label=jast.ExpDefault(),
            body=[jast.Empty()],
        )
        self.assertEqual("default: ;", jast.unparse(switchexprule, indent=-1))

    def test_switchexprule_block(self):
        tree = jast.switchexprule(
            label=jast.ExpCase(),
            cases=[jast.Constant(jast.IntLiteral(42))],
            arrow=False,
            body=[jast.Block()],
        )
        self.assertEqual("case 42: {}", jast.unparse(tree, indent=-1))

    def test_switchexprule_empty(self):
        tree = jast.switchexprule(
            label=jast.ExpDefault(),
            arrow=True,
        )
        self.assertEqual("default ->", jast.unparse(tree, indent=-1))

    def test_SwitchExp(self):
        tree = jast.SwitchExp(
            value=jast.identifier("foo"),
            rules=[
                jast.switchexprule(
                    label=jast.ExpCase(),
                    cases=[
                        jast.Constant(jast.IntLiteral(42)),
                        jast.Constant(jast.IntLiteral(43)),
                    ],
                ),
                jast.switchexprule(
                    label=jast.ExpCase(),
                    cases=[
                        jast.guardedpattern(
                            value=jast.pattern(
                                type=jast.Int(),
                                id=jast.identifier("x"),
                            ),
                            conditions=[
                                jast.Constant(jast.BoolLiteral(True)),
                            ],
                        ),
                    ],
                    arrow=True,
                    body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
                ),
                jast.switchexprule(
                    label=jast.ExpDefault(),
                    body=[
                        jast.Block(
                            body=[jast.Return(jast.Constant(jast.IntLiteral(0)))]
                        )
                    ],
                ),
            ],
        )
        self.assertEqual(
            "switch (foo) { case 42, 43: case int x && true -> return 24; default: { return 0; } }",
            jast.unparse(tree, indent=-1),
        )

    def test_This(self):
        tree = jast.This()
        self.assertEqual("this", jast.unparse(tree))

    def test_Super(self):
        tree = jast.Super()
        self.assertEqual("super", jast.unparse(tree))

    def test_Super_in_ExplicitGenericInvocation(self):
        tree = jast.ExplicitGenericInvocation(
            type_args=jast.typeargs([jast.Int()]),
            value=jast.Super(
                type_args=jast.typeargs([jast.Int()]),
                id=jast.identifier("x"),
            ),
        )
        self.assertEqual("<int>super.<int>x", jast.unparse(tree))

    def test_Super_in_ExplicitGenericInvocation_with_args(self):
        tree = jast.ExplicitGenericInvocation(
            type_args=jast.typeargs([jast.Int()]),
            value=jast.Call(
                func=jast.Super(
                    type_args=jast.typeargs([jast.Int()]),
                    id=jast.identifier("x"),
                ),
                args=[jast.Constant(jast.IntLiteral(42))],
            ),
        )
        self.assertEqual("<int>super.<int>x(42)", jast.unparse(tree))

    def test_Constant(self):
        tree = jast.Constant(jast.IntLiteral(42))
        self.assertEqual("42", jast.unparse(tree))

    def test_Constant_boolean(self):
        tree = jast.Constant(jast.BoolLiteral(True))
        self.assertEqual("true", jast.unparse(tree))

    def test_Name(self):
        tree = jast.Name(jast.identifier("foo"))
        self.assertEqual("foo", jast.unparse(tree))

    def test_ClassExpr(self):
        tree = jast.ClassExpr(
            type=jast.ClassType(
                coits=[
                    jast.Coit(
                        id=jast.identifier("foo"),
                    ),
                    jast.Coit(
                        id=jast.identifier("bar"),
                    ),
                ],
            )
        )
        self.assertEqual("foo.bar.class", jast.unparse(tree))

    def test_ExplicitGenericInvocation(self):
        tree = jast.ExplicitGenericInvocation(
            type_args=jast.typeargs([jast.Int()]),
            value=jast.Call(func=jast.Name(jast.identifier("foo")), args=[]),
        )
        self.assertEqual("<int>foo()", jast.unparse(tree))

    def test_ExplicitGenericInvocation_args(self):
        tree = jast.ExplicitGenericInvocation(
            type_args=jast.typeargs([jast.Int()]),
            value=jast.Call(
                func=jast.Name(jast.identifier("foo")),
                args=[
                    jast.Constant(jast.IntLiteral(42)),
                    jast.Constant(jast.IntLiteral(24)),
                ],
            ),
        )
        self.assertEqual("<int>foo(42, 24)", jast.unparse(tree))

    def test_ExplicitGenericInvocation_this(self):
        tree = jast.ExplicitGenericInvocation(
            type_args=jast.typeargs([jast.Int()]),
            value=jast.Call(
                func=jast.This(),
                args=[jast.Constant(jast.IntLiteral(42))],
            ),
        )
        self.assertEqual("<int>this(42)", jast.unparse(tree))

    def test_Subscript(self):
        tree = jast.Subscript(
            value=jast.Name(jast.identifier("x")),
            index=jast.Name(jast.identifier("y")),
        )
        self.assertEqual("x[y]", jast.unparse(tree))

    def test_Subscript_primary(self):
        tree = jast.Subscript(
            value=jast.Member(
                value=jast.Name(jast.identifier("x")),
                member=jast.Name(jast.identifier("y")),
            ),
            index=jast.Name(jast.identifier("z")),
        )
        self.assertEqual("x.y[z]", jast.unparse(tree))

    def test_Subscript_parens(self):
        tree = jast.Subscript(
            value=jast.UnaryOp(
                op=jast.PreInc(),
                operand=jast.Name(jast.identifier("x")),
            ),
            index=jast.Name(jast.identifier("z")),
        )
        self.assertEqual("(++x)[z]", jast.unparse(tree))

    def test_Subscript_no_parens(self):
        tree = jast.UnaryOp(
            op=jast.PreInc(),
            operand=jast.Subscript(
                value=jast.Name(jast.identifier("x")),
                index=jast.Name(jast.identifier("z")),
            ),
        )
        self.assertEqual("++x[z]", jast.unparse(tree))

    def test_Member(self):
        tree = jast.Member(
            value=jast.Name(jast.identifier("foo")),
            member=jast.Name(jast.identifier("bar")),
        )
        self.assertEqual("foo.bar", jast.unparse(tree))

    def test_Member_call(self):
        tree = jast.Member(
            value=jast.Name(jast.identifier("foo")),
            member=jast.Call(func=jast.Name(jast.identifier("bar")), args=[]),
        )
        self.assertEqual("foo.bar()", jast.unparse(tree))

    def test_Member_this(self):
        tree = jast.Member(
            value=jast.Name(jast.identifier("bar")),
            member=jast.This(),
        )
        self.assertEqual("bar.this", jast.unparse(tree))

    def test_Member_inner_creation(self):
        tree = jast.Member(
            value=jast.Name(
                id=jast.identifier("x"),
            ),
            member=jast.NewObject(
                type_args=jast.typeargs([jast.Int()]),
                type=jast.Coit(
                    id=jast.identifier("Y"),
                    type_args=jast.typeargs([]),
                ),
                args=[jast.Constant(jast.IntLiteral(42))],
                body=[jast.EmptyDecl()],
            ),
        )
        self.assertEqual("x.new<int> Y<>(42) { ; }", jast.unparse(tree, indent=-1))

    def test_Member_super(self):
        tree = jast.Member(
            value=jast.Name(
                id=jast.identifier("x"),
            ),
            member=jast.Super(
                id=jast.identifier("y"),
            ),
        )
        self.assertEqual("x.super.y", jast.unparse(tree))

    def test_Member_super_args(self):
        tree = jast.Member(
            value=jast.Name(
                id=jast.identifier("x"),
            ),
            member=jast.Call(
                func=jast.Super(),
                args=[jast.Constant(jast.IntLiteral(42))],
            ),
        )
        self.assertEqual("x.super(42)", jast.unparse(tree))

    def test_Member_ExplicitGenericInvocation(self):
        tree = jast.Member(
            value=jast.Name(
                id=jast.identifier("x"),
            ),
            member=jast.ExplicitGenericInvocation(
                type_args=jast.typeargs([jast.Int()]),
                value=jast.Call(
                    func=jast.Name(jast.identifier("y")),
                    args=[],
                ),
            ),
        )
        self.assertEqual("x.<int>y()", jast.unparse(tree))

    def test_Member_primary(self):
        tree = jast.Member(
            value=jast.Subscript(
                value=jast.Name(jast.identifier("x")),
                index=jast.Constant(jast.IntLiteral(42)),
            ),
            member=jast.Name(jast.identifier("z")),
        )
        self.assertEqual("x[42].z", jast.unparse(tree))

    def test_Member_primary_reversed(self):
        tree = jast.Subscript(
            value=jast.Member(
                value=jast.Name(jast.identifier("x")),
                member=jast.Name(jast.identifier("y")),
            ),
            index=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("x.y[42]", jast.unparse(tree))

    def test_Member_parens(self):
        tree = jast.Member(
            value=jast.UnaryOp(
                op=jast.PreInc(),
                operand=jast.Name(jast.identifier("x")),
            ),
            member=jast.Name(jast.identifier("y")),
        )
        self.assertEqual("(++x).y", jast.unparse(tree))

    def test_Member_no_parens(self):
        tree = jast.UnaryOp(
            op=jast.PreInc(),
            operand=jast.Member(
                value=jast.Name(jast.identifier("x")),
                member=jast.Name(jast.identifier("y")),
            ),
        )
        self.assertEqual("++x.y", jast.unparse(tree))

    def test_Call(self):
        tree = jast.Call(
            func=jast.Name(jast.identifier("foo")),
        )
        self.assertEqual("foo()", jast.unparse(tree))

    def test_Call_args(self):
        tree = jast.Call(
            func=jast.Name(jast.identifier("foo")),
            args=[
                jast.Constant(jast.IntLiteral(42)),
                jast.Constant(jast.IntLiteral(24)),
            ],
        )
        self.assertEqual("foo(42, 24)", jast.unparse(tree))

    def test_Call_this(self):
        tree = jast.Call(
            func=jast.This(),
            args=[jast.Constant(jast.IntLiteral(42))],
        )
        self.assertEqual("this(42)", jast.unparse(tree))

    def test_Call_super(self):
        tree = jast.Call(
            func=jast.Super(),
            args=[jast.Constant(jast.IntLiteral(42))],
        )
        self.assertEqual("super(42)", jast.unparse(tree))

    def test_Call_no_parens(self):
        tree = jast.UnaryOp(
            op=jast.PreInc(),
            operand=jast.Call(
                func=jast.Name(jast.identifier("foo")),
                args=[jast.Constant(jast.IntLiteral(42))],
            ),
        )
        self.assertEqual("++foo(42)", jast.unparse(tree))

    def test_Reference(self):
        tree = jast.Reference(
            type=jast.Name(jast.identifier("x")),
            type_args=jast.typeargs([jast.Int()]),
            id=jast.identifier("y"),
        )
        self.assertEqual("x::<int>y", jast.unparse(tree))

    def test_Reference_primary(self):
        tree = jast.Reference(
            type=jast.Member(
                value=jast.Name(jast.identifier("x")),
                member=jast.Name(jast.identifier("y")),
            ),
            id=jast.identifier("z"),
        )
        self.assertEqual("x.y::z", jast.unparse(tree))

    def test_Reference_twice(self):
        tree = jast.Reference(
            type=jast.Reference(
                type=jast.Name(jast.identifier("x")),
                type_args=jast.typeargs([jast.Int()]),
                id=jast.identifier("y"),
            ),
            id=jast.identifier("z"),
        )
        self.assertEqual("x::<int>y::z", jast.unparse(tree))

    def test_Reference_type(self):
        tree = jast.Reference(
            type=jast.Int(),
            type_args=jast.typeargs([jast.Int()]),
            id=jast.identifier("x"),
        )
        self.assertEqual("int::<int>x", jast.unparse(tree))

    def test_Reference_new(self):
        tree = jast.Reference(
            type=jast.Int(),
            new=True,
        )
        self.assertEqual("int::new", jast.unparse(tree))

    def test_Reference_class_type(self):
        tree = jast.Reference(
            type=jast.Coit(
                id=jast.identifier("X"),
                type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
            ),
            type_args=jast.typeargs([jast.Int(), jast.Float()]),
            new=True,
        )
        self.assertEqual("X<int, boolean>::<int, float>new", jast.unparse(tree))

    def test_arrayinit(self):
        tree = jast.arrayinit(
            values=[
                jast.Constant(jast.IntLiteral(42)),
                jast.Constant(jast.IntLiteral(24)),
            ]
        )
        self.assertEqual("{42, 24}", jast.unparse(tree))

    def test_receiver(self):
        tree = jast.receiver(
            type=jast.Int(),
            identifiers=[jast.identifier("foo"), jast.identifier("bar")],
        )
        self.assertEqual("int foo.bar.this", jast.unparse(tree))

    def test_param(self):
        param = jast.param(
            modifiers=[jast.Final()],
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("bar")),
        )
        self.assertEqual("final int bar", jast.unparse(param))

    def test_arity(self):
        arity = jast.arity(
            modifiers=[jast.Final()],
            type=jast.Int(),
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.variabledeclaratorid(jast.identifier("bar")),
        )
        self.assertEqual("final int @foo ... bar", jast.unparse(arity))

    def test_params(self):
        params = jast.params(
            receiver_param=jast.receiver(jast.Int()),
            parameters=[
                jast.param(
                    type=jast.Int(),
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                ),
                jast.arity(
                    type=jast.Int(),
                    id=jast.variabledeclaratorid(jast.identifier("bar")),
                ),
            ],
        )
        self.assertEqual("int this, int foo, int ... bar", jast.unparse(params))

    def test_Empty(self):
        tree = jast.Empty()
        self.assertEqual(";", jast.unparse(tree))

    def test_Block(self):
        tree = jast.Block(body=[jast.Empty(), jast.Empty()])
        self.assertEqual("{ ; ; }", jast.unparse(tree, indent=-1))

    def test_Compound(self):
        tree = jast.Compound(body=[jast.Empty(), jast.Empty()])
        self.assertEqual("; ;", jast.unparse(tree, indent=-1))

    def test_LocalType_class(self):
        tree = jast.LocalType(
            decl=jast.Class(
                id=jast.identifier("A"),
                body=[jast.EmptyDecl()],
            )
        )
        self.assertEqual("class A { ; }", jast.unparse(tree, indent=-1))

    def test_LocalType_interface(self):
        tree = jast.LocalType(
            decl=jast.Interface(
                id=jast.identifier("A"),
                body=[jast.EmptyDecl()],
            )
        )
        self.assertEqual("interface A { ; }", jast.unparse(tree, indent=-1))

    def test_LocalType_record(self):
        tree = jast.LocalType(
            decl=jast.Record(
                id=jast.identifier("A"),
                body=[jast.EmptyDecl()],
            )
        )
        self.assertEqual("record A() { ; }", jast.unparse(tree, indent=-1))

    def test_LocalVariable(self):
        tree = jast.LocalVariable(
            modifiers=[jast.Final()],
            type=jast.Int(),
            declarators=[
                jast.declarator(
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                    init=jast.Constant(jast.IntLiteral(42)),
                ),
                jast.declarator(id=jast.variabledeclaratorid(jast.identifier("bar"))),
            ],
        )
        self.assertEqual("final int foo = 42, bar;", jast.unparse(tree))

    def test_Labeled(self):
        tree = jast.Labeled(
            label=jast.identifier("foo"),
            body=jast.Empty(),
        )
        self.assertEqual("foo:\n;", jast.unparse(tree))

    def test_Expression(self):
        tree = jast.Expression(
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("42;", jast.unparse(tree))

    def test_If(self):
        tree = jast.If(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Empty(),
            orelse=jast.Empty(),
        )
        self.assertEqual("if (true) ; else ;", jast.unparse(tree, indent=-1))

    def test_If_block(self):
        tree = jast.If(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Block(body=[jast.Empty()]),
            orelse=jast.Block(body=[jast.Empty()]),
        )
        self.assertEqual("if (true) {\n    ;\n} else {\n    ;\n}", jast.unparse(tree))

    def test_If_no_orelse(self):
        tree = jast.If(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Empty(),
        )
        self.assertEqual("if (true)\n    ;", jast.unparse(tree))

    def test_Assert(self):
        tree = jast.Assert(
            test=jast.Constant(jast.BoolLiteral(True)),
            msg=jast.Constant(jast.StringLiteral("foo")),
        )
        self.assertEqual('assert true : "foo";', jast.unparse(tree))

    def test_Match(self):
        tree = jast.Match(
            type=jast.Int(),
            id=jast.identifier("foo"),
        )
        self.assertEqual("int foo", jast.unparse(tree))

    def test_Case(self):
        tree = jast.Case(
            guard=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("case 42:", jast.unparse(tree))

    def test_DefaultCase(self):
        tree = jast.DefaultCase()
        self.assertEqual("default:", jast.unparse(tree))

    def test_Throw(self):
        tree = jast.Throw(
            exc=jast.Name(jast.identifier("foo")),
        )
        self.assertEqual("throw foo;", jast.unparse(tree))

    def test_switchgroup(self):
        tree = jast.switchgroup(
            labels=[
                jast.Case(
                    guard=jast.Constant(jast.IntLiteral(42)),
                ),
                jast.Case(
                    guard=jast.Constant(jast.IntLiteral(24)),
                ),
            ],
            body=[jast.Empty()],
        )
        self.assertEqual("case 42: case 24: ;", jast.unparse(tree, indent=-1))

    def test_switchblock(self):
        tree = jast.switchblock(
            groups=[
                jast.switchgroup(
                    labels=[
                        jast.Case(
                            guard=jast.Constant(jast.IntLiteral(42)),
                        ),
                        jast.Case(
                            guard=jast.Constant(jast.IntLiteral(24)),
                        ),
                    ],
                    body=[jast.Empty()],
                )
            ],
            labels=[jast.Case(guard=jast.Constant(jast.IntLiteral(42)))],
        )
        self.assertEqual(
            "{\n    case 42:\n    case 24:\n        ;\n    case 42:\n}",
            jast.unparse(tree),
        )

    def test_Switch(self):
        tree = jast.Switch(
            value=jast.Name(jast.identifier("foo")),
            body=jast.switchblock(
                groups=[
                    jast.switchgroup(
                        labels=[
                            jast.Case(
                                guard=jast.Constant(jast.IntLiteral(42)),
                            ),
                            jast.Case(
                                guard=jast.Constant(jast.IntLiteral(24)),
                            ),
                        ],
                        body=[jast.Empty()],
                    )
                ],
                labels=[jast.Case(guard=jast.Constant(jast.IntLiteral(42)))],
            ),
        )
        self.assertEqual(
            "switch (foo) {\n    case 42:\n    case 24:\n        ;\n    case 42:\n}",
            jast.unparse(tree),
        )

    def test_While(self):
        tree = jast.While(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Empty(),
        )
        self.assertEqual("while (true)\n    ;", jast.unparse(tree))

    def test_DoWhile(self):
        tree = jast.DoWhile(
            body=jast.Empty(),
            test=jast.Constant(jast.BoolLiteral(True)),
        )
        self.assertEqual("do\n    ;\nwhile (true);", jast.unparse(tree))

    def test_For(self):
        tree = jast.For(
            init=jast.LocalVariable(
                type=jast.Int(),
                declarators=[
                    jast.declarator(
                        id=jast.variabledeclaratorid(jast.identifier("foo")),
                        init=jast.Constant(jast.IntLiteral(42)),
                    )
                ],
            ),
            test=jast.BinOp(
                left=jast.Name(jast.identifier("foo")),
                op=jast.Gt(),
                right=jast.Constant(jast.IntLiteral(0)),
            ),
            update=[
                jast.PostOp(
                    operand=jast.Name(jast.identifier("foo")),
                    op=jast.PostDec(),
                )
            ],
            body=jast.Empty(),
        )
        self.assertEqual(
            "for (int foo = 42; foo > 0; foo--)\n    ;", jast.unparse(tree)
        )

    def test_For_block(self):
        tree = jast.For(
            init=jast.LocalVariable(
                type=jast.Int(),
                declarators=[
                    jast.declarator(
                        id=jast.variabledeclaratorid(jast.identifier("foo")),
                        init=jast.Constant(jast.IntLiteral(42)),
                    )
                ],
            ),
            test=jast.BinOp(
                left=jast.Name(jast.identifier("foo")),
                op=jast.Gt(),
                right=jast.Constant(jast.IntLiteral(0)),
            ),
            update=[
                jast.PostOp(
                    operand=jast.Name(jast.identifier("foo")),
                    op=jast.PostDec(),
                )
            ],
            body=jast.Block(body=[jast.Empty()]),
        )
        self.assertEqual(
            "for (int foo = 42; foo > 0; foo--) {\n    ;\n}",
            jast.unparse(tree),
        )

    def test_For_multiple_init_update(self):
        tree = jast.For(
            init=[
                jast.Assign(
                    target=jast.Name(jast.identifier("x")),
                    value=jast.Constant(jast.IntLiteral(0)),
                ),
                jast.Assign(
                    target=jast.Name(jast.identifier("y")),
                    value=jast.Constant(jast.IntLiteral(0)),
                ),
            ],
            test=jast.BinOp(
                left=jast.Name(jast.identifier("x")),
                op=jast.Lt(),
                right=jast.Constant(jast.IntLiteral(10)),
            ),
            update=[
                jast.PostOp(
                    operand=jast.Name(jast.identifier("x")),
                    op=jast.PostInc(),
                ),
                jast.PostOp(
                    operand=jast.Name(jast.identifier("y")),
                    op=jast.PostInc(),
                ),
            ],
            body=jast.Empty(),
        )
        self.assertEqual(
            "for (x = 0, y = 0; x < 10; x++, y++)\n    ;", jast.unparse(tree)
        )

    def test_ForEach(self):
        tree = jast.ForEach(
            modifiers=[jast.Final()],
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            iter=jast.Name(jast.identifier("bar")),
            body=jast.Empty(),
        )
        self.assertEqual("for (final int foo : bar)\n    ;", jast.unparse(tree))

    def test_ForEach_block(self):
        tree = jast.ForEach(
            modifiers=[jast.Final()],
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            iter=jast.Name(jast.identifier("bar")),
            body=jast.Block(body=[jast.Empty()]),
        )
        self.assertEqual("for (final int foo : bar) {\n    ;\n}", jast.unparse(tree))

    def test_Break(self):
        tree = jast.Break()
        self.assertEqual("break;", jast.unparse(tree))

    def test_Break_label(self):
        tree = jast.Break(label=jast.identifier("foo"))
        self.assertEqual("break foo;", jast.unparse(tree))

    def test_Continue(self):
        tree = jast.Continue()
        self.assertEqual("continue;", jast.unparse(tree))

    def test_Continue_label(self):
        tree = jast.Continue(label=jast.identifier("foo"))
        self.assertEqual("continue foo;", jast.unparse(tree))

    def test_Return(self):
        tree = jast.Return(
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("return 42;", jast.unparse(tree))

    def test_Return_no_value(self):
        tree = jast.Return()
        self.assertEqual("return;", jast.unparse(tree))

    def test_Synch(self):
        tree = jast.Synch(lock=jast.Constant(jast.IntLiteral(42)), body=jast.Block())
        self.assertEqual("synchronized (42) {}", jast.unparse(tree, indent=-1))

    def test_catch(self):
        catch = jast.catch(
            modifiers=[jast.Final()],
            excs=[jast.qname([jast.identifier("foo")])],
            id=jast.identifier("bar"),
            body=jast.Block(),
        )
        self.assertEqual("catch (final foo bar) {}", jast.unparse(catch, indent=-1))

    def test_Try(self):
        tree = jast.Try(
            body=jast.Block(),
            catches=[
                jast.catch(
                    modifiers=[jast.Final()],
                    excs=[jast.qname([jast.identifier("foo")])],
                    id=jast.identifier("bar"),
                    body=jast.Block(),
                )
            ],
            final=jast.Block(),
        )
        self.assertEqual(
            "try {} catch (final foo bar) {} finally {}", jast.unparse(tree)
        )

    def test_resource(self):
        tree = jast.resource(
            modifiers=[jast.Final()],
            type=jast.Coit(id=jast.identifier("X")),
            variable=jast.declarator(
                id=jast.variabledeclaratorid(jast.identifier("foo")),
                init=jast.Constant(jast.IntLiteral(42)),
            ),
        )
        self.assertEqual("final X foo = 42", jast.unparse(tree))

    def test_TryWithResources(self):
        tree = jast.TryWithResources(
            resources=[
                jast.resource(
                    modifiers=[jast.Final()],
                    type=jast.Coit(id=jast.identifier("X")),
                    variable=jast.declarator(
                        id=jast.variabledeclaratorid(jast.identifier("foo")),
                        init=jast.Constant(jast.IntLiteral(42)),
                    ),
                )
            ],
            body=jast.Block(),
            catches=[
                jast.catch(
                    modifiers=[jast.Final()],
                    excs=[jast.qname([jast.identifier("foo")])],
                    id=jast.identifier("bar"),
                    body=jast.Block(),
                )
            ],
            final=jast.Block(),
        )
        self.assertEqual(
            "try (final X foo = 42) {} catch (final foo bar) {} finally {}",
            jast.unparse(tree),
        )

    def test_Yield(self):
        tree = jast.Yield(value=jast.Constant(jast.IntLiteral(42)))
        self.assertEqual("yield 42;", jast.unparse(tree))

    def test_EmptyDecl(self):
        tree = jast.EmptyDecl()
        self.assertEqual(";", jast.unparse(tree))

    def test_Package(self):
        tree = jast.Package(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            name=jast.qname([jast.identifier("bar"), jast.identifier("baz")]),
        )
        self.assertEqual("@foo package bar.baz;", jast.unparse(tree))

    def test_Import(self):
        tree = jast.Import(
            static=True,
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertEqual("import static foo.bar;", jast.unparse(tree))

    def test_Import_on_demand(self):
        tree = jast.Import(
            name=jast.qname([jast.identifier("foo")]),
            on_demand=True,
        )
        self.assertEqual("import foo.*;", jast.unparse(tree))

    def test_Requires(self):
        tree = jast.Requires(
            modifiers=[jast.Static()],
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertEqual("requires static foo.bar;", jast.unparse(tree))

    def test_Exports(self):
        tree = jast.Exports(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertEqual("exports foo.bar;", jast.unparse(tree))

    def test_Exports_to(self):
        tree = jast.Exports(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            to=jast.qname([jast.identifier("baz")]),
        )
        self.assertEqual("exports foo.bar to baz;", jast.unparse(tree))

    def test_Opens(self):
        tree = jast.Opens(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertEqual("opens foo.bar;", jast.unparse(tree))

    def test_Opens_to(self):
        tree = jast.Opens(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            to=jast.qname([jast.identifier("baz")]),
        )
        self.assertEqual("opens foo.bar to baz;", jast.unparse(tree))

    def test_Uses(self):
        tree = jast.Uses(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertEqual("uses foo.bar;", jast.unparse(tree))

    def test_Provides(self):
        tree = jast.Provides(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            with_=jast.qname([jast.identifier("baz")]),
        )
        self.assertEqual("provides foo.bar with baz;", jast.unparse(tree))

    def test_Module(self):
        tree = jast.Module(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            body=[jast.Uses(name=jast.qname([jast.identifier("baz")]))],
        )
        self.assertEqual("module foo.bar {\n    uses baz;\n}", jast.unparse(tree))

    def test_Module_open(self):
        tree = jast.Module(
            open=True,
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            body=[jast.Uses(name=jast.qname([jast.identifier("baz")]))],
        )
        self.assertEqual("open module foo.bar {\n    uses baz;\n}", jast.unparse(tree))

    def test_declarator(self):
        tree = jast.declarator(
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            init=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("foo = 42", jast.unparse(tree))

    def test_declarator_no_init(self):
        tree = jast.declarator(
            id=jast.variabledeclaratorid(jast.identifier("foo")),
        )
        self.assertEqual("foo", jast.unparse(tree))

    def test_Field(self):
        tree = jast.Field(
            modifiers=[jast.Final()],
            type=jast.Int(),
            declarators=[
                jast.declarator(
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                    init=jast.Constant(jast.IntLiteral(42)),
                ),
                jast.declarator(id=jast.variabledeclaratorid(jast.identifier("bar"))),
            ],
        )
        self.assertEqual("final int foo = 42, bar;", jast.unparse(tree))

    def test_Method(self):
        tree = jast.Method(
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            return_type=jast.Int(),
            id=jast.identifier("bar"),
            parameters=jast.params(
                parameters=[
                    jast.param(
                        type=jast.Int(),
                        id=jast.variabledeclaratorid(jast.identifier("baz")),
                    ),
                    jast.param(
                        type=jast.Int(),
                        id=jast.variabledeclaratorid(jast.identifier("qux")),
                    ),
                ],
            ),
            dims=[jast.dim()],
            throws=[jast.qname([jast.identifier("quux")])],
            body=jast.Block(),
        )
        self.assertEqual(
            "public <T> @foo int bar(int baz, int qux)[] throws quux {}",
            jast.unparse(tree),
        )

    def test_Method_no_body(self):
        tree = jast.Method(
            return_type=jast.Int(),
            id=jast.identifier("bar"),
        )
        self.assertEqual("int bar();", jast.unparse(tree))

    def test_Constructor(self):
        tree = jast.Constructor(
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            id=jast.identifier("bar"),
            parameters=jast.params(
                parameters=[
                    jast.param(
                        type=jast.Int(),
                        id=jast.variabledeclaratorid(jast.identifier("baz")),
                    ),
                    jast.param(
                        type=jast.Int(),
                        id=jast.variabledeclaratorid(jast.identifier("qux")),
                    ),
                ],
            ),
            throws=[jast.qname([jast.identifier("quux")])],
            body=jast.Block(),
        )
        self.assertEqual(
            "public <T> bar(int baz, int qux) throws quux {}", jast.unparse(tree)
        )

    def test_Constructor_no_params(self):
        tree = jast.Constructor(
            id=jast.identifier("bar"),
            body=jast.Block(),
        )
        self.assertEqual("bar {}", jast.unparse(tree))

    def test_Initializer(self):
        tree = jast.Initializer(
            body=jast.Block(
                body=[jast.Expression(value=jast.Constant(jast.IntLiteral(42)))]
            ),
        )
        self.assertEqual("{\n    42;\n}", jast.unparse(tree))

    def test_Initializer_static(self):
        tree = jast.Initializer(
            static=True,
            body=jast.Block(
                body=[jast.Expression(value=jast.Constant(jast.IntLiteral(42)))]
            ),
        )
        self.assertEqual("static {\n    42;\n}", jast.unparse(tree))

    def test_Interface(self):
        tree = jast.Interface(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            extends=jast.Coit(id=jast.identifier("bar")),
            implements=[jast.Coit(id=jast.identifier("baz"))],
            body=[jast.Method(return_type=jast.Int(), id=jast.identifier("qux"))],
        )
        self.assertEqual(
            "public interface foo<T> extends bar implements baz {\n    int qux();\n}",
            jast.unparse(tree),
        )

    def test_AnnotationMethod(self):
        tree = jast.AnnotationMethod(
            modifiers=[jast.Public()],
            type=jast.Int(),
            id=jast.identifier("foo"),
            default=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertEqual("public int foo() default 42;", jast.unparse(tree))

    def test_AnnotationMethod_no_default(self):
        tree = jast.AnnotationMethod(
            modifiers=[jast.Public()],
            type=jast.Int(),
            id=jast.identifier("foo"),
        )
        self.assertEqual("public int foo();", jast.unparse(tree))

    def test_AnnotationDecl(self):
        tree = jast.AnnotationDecl(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            body=[jast.AnnotationMethod(type=jast.Int(), id=jast.identifier("qux"))],
        )
        self.assertEqual(
            "public @interface foo {\n    int qux();\n}",
            jast.unparse(tree),
        )

    def test_Class(self):
        tree = jast.Class(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            extends=jast.Coit(id=jast.identifier("bar")),
            implements=[jast.Coit(id=jast.identifier("baz"))],
            permits=[jast.Coit(id=jast.identifier("qux"))],
            body=[
                jast.Initializer(
                    body=jast.Block(
                        body=[
                            jast.Expression(value=jast.Constant(jast.IntLiteral(42))),
                            jast.Block(),
                        ]
                    ),
                ),
                jast.Method(
                    return_type=jast.Int(),
                    id=jast.identifier("quux"),
                    body=jast.Block(),
                ),
            ],
        )
        self.assertEqual(
            "public class foo<T> extends bar implements baz permits qux {\n"
            "    {\n"
            "        42;\n"
            "        {}\n"
            "    }\n"
            "    \n"
            "    int quux() {}\n"
            "}",
            jast.unparse(tree),
        )

    def test_enumconstant(self):
        tree = jast.enumconstant(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
            args=[jast.Constant(jast.IntLiteral(42))],
            body=[jast.Method(return_type=jast.Int(), id=jast.identifier("qux"))],
        )
        self.assertEqual("@foo bar(42) {\n    int qux();\n}", jast.unparse(tree))

    def test_Enum(self):
        tree = jast.Enum(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            implements=[jast.Coit(id=jast.identifier("bar"))],
            constants=[
                jast.enumconstant(id=jast.identifier("A")),
                jast.enumconstant(id=jast.identifier("B")),
            ],
            body=[
                jast.Method(
                    return_type=jast.Int(), id=jast.identifier("qux"), body=jast.Block()
                )
            ],
        )
        self.assertEqual(
            "public enum foo implements bar {\n    A,\n    B;\n    int qux() {}\n}",
            jast.unparse(tree),
        )

    def test_Enum_no_body(self):
        tree = jast.Enum(
            id=jast.identifier("foo"),
            constants=[
                jast.enumconstant(id=jast.identifier("A")),
                jast.enumconstant(id=jast.identifier("B")),
            ],
        )
        self.assertEqual("enum foo {\n    A,\n    B\n}", jast.unparse(tree))

    def test_Enum_no_constants(self):
        tree = jast.Enum(
            id=jast.identifier("foo"),
            body=[
                jast.Method(
                    return_type=jast.Int(), id=jast.identifier("qux"), body=jast.Block()
                )
            ],
        )
        self.assertEqual("enum foo {\n    ;\n    int qux() {}\n}", jast.unparse(tree))

    def test_recordcomponent(self):
        tree = jast.recordcomponent(
            type=jast.Int(),
            id=jast.identifier("foo"),
        )
        self.assertEqual("int foo", jast.unparse(tree))

    def test_Record(self):
        tree = jast.Record(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            components=[
                jast.recordcomponent(type=jast.Int(), id=jast.identifier("bar")),
                jast.recordcomponent(type=jast.Int(), id=jast.identifier("baz")),
            ],
            implements=[jast.Coit(id=jast.identifier("qux"))],
            body=[
                jast.Method(
                    return_type=jast.Int(),
                    id=jast.identifier("quux"),
                    body=jast.Block(),
                )
            ],
        )
        self.assertEqual(
            "public record foo<T>(int bar, int baz) implements qux {\n    int quux() {}\n}",
            jast.unparse(tree),
        )

    def test_CompilationUnit(self):
        tree = jast.CompilationUnit(
            package=jast.Package(
                annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
                name=jast.qname([jast.identifier("bar"), jast.identifier("baz")]),
            ),
            imports=[
                jast.Import(
                    static=True,
                    name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
                )
            ],
            body=[
                jast.Class(
                    modifiers=[jast.Public()],
                    id=jast.identifier("foo"),
                    type_params=jast.typeparams(
                        parameters=[jast.typeparam(id=jast.identifier("T"))],
                    ),
                    extends=jast.Coit(id=jast.identifier("bar")),
                    implements=[jast.Coit(id=jast.identifier("baz"))],
                    permits=[jast.Coit(id=jast.identifier("qux"))],
                    body=[
                        jast.Method(
                            return_type=jast.Int(),
                            id=jast.identifier("quux"),
                            body=jast.Block(),
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            "@foo package bar.baz;\n"
            "\n"
            "import static foo.bar;\n"
            "\n"
            "public class foo<T> extends bar implements baz permits qux {\n"
            "    int quux() {}\n"
            "}",
            jast.unparse(tree),
        )

    def test_CompilationUnit_no_package(self):
        tree = jast.CompilationUnit(
            imports=[
                jast.Import(
                    static=True,
                    name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
                ),
                jast.Import(
                    name=jast.qname([jast.identifier("baz")]),
                ),
            ],
            body=[
                jast.Class(
                    modifiers=[jast.Public()],
                    id=jast.identifier("qux"),
                    body=[
                        jast.Method(
                            return_type=jast.Int(),
                            id=jast.identifier("quux"),
                            body=jast.Block(),
                        )
                    ],
                ),
                jast.Enum(
                    id=jast.identifier("A"),
                    constants=[
                        jast.enumconstant(id=jast.identifier("B")),
                        jast.enumconstant(id=jast.identifier("C")),
                    ],
                ),
            ],
        )
        self.assertEqual(
            "import static foo.bar;\n"
            "import baz;\n"
            "\n"
            "public class qux {\n"
            "    int quux() {}\n"
            "}\n"
            "\n"
            "enum A {\n"
            "    B,\n"
            "    C\n"
            "}",
            jast.unparse(tree),
        )

    def test_ModularUnit(self):
        tree = jast.ModularUnit(
            imports=[
                jast.Import(
                    static=True,
                    name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
                )
            ],
            body=jast.Module(
                open=True,
                name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
                body=[jast.Uses(name=jast.qname([jast.identifier("baz")]))],
            ),
        )
        self.assertEqual(
            "import static foo.bar;\n"
            "\n"
            "open module foo.bar {\n"
            "    uses baz;\n"
            "}",
            jast.unparse(tree),
        )
