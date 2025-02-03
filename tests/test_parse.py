import itertools

from parameterized import parameterized

import jast
from utils import (
    LEFT_PRECEDENCE_FOR_RIGHT,
    RIGHT_PRECEDENCE_FOR_LEFT,
    OPERATORS,
    OPERATORS_ASSIGN,
    INSTANCEOF_HIGHER_SAME_PRECEDENCE,
    INSTANCEOF_LOWER_PRECEDENCE,
    INSTANCEOF_LOWER_SAME_PRECEDENCE,
    UNARY_OPERATORS,
    BaseTest,
    POST_OPERATORS,
)


class TestParse(BaseTest):
    def test_identifier(self):
        name = jast.parse("foo", jast.ParseMode.EXPR)
        self._test_name(name, "foo")

    def test_qname(self):
        qname = jast.parse("package foo.bar;", jast.ParseMode.DECL)
        self.assertIsInstance(qname, jast.Package)
        name = qname.name
        self.assertIsInstance(name, jast.qname)
        self.assertEqual(2, len(name.identifiers))
        self._test_identifier(name.identifiers[0], "foo")
        self._test_identifier(name.identifiers[1], "bar")

    def _test_int_literal_long(self, value, long=False):
        self.assertIsInstance(value, jast.Constant)
        int_literal = value.value
        self.assertIsInstance(int_literal, jast.IntLiteral)
        self.assertEqual(42, int_literal.value)
        if long:
            self.assertTrue(int_literal.long)
        else:
            self.assertFalse(int_literal.long)

    def test_IntLiteral(self):
        int_literal = jast.parse("42", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal)

    def test_IntLiteral_long(self):
        int_literal = jast.parse("42L", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal, long=True)

    def test_IntLiteral_bin(self):
        int_literal = jast.parse("0b101010", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal)

    def test_IntLiteral_bin_long(self):
        int_literal = jast.parse("0b101010L", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal, long=True)

    def test_IntLiteral_oct(self):
        int_literal = jast.parse("0_52", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal)

    def test_IntLiteral_oct_long(self):
        int_literal = jast.parse("0_52L", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal, long=True)

    def test_IntLiteral_hex(self):
        int_literal = jast.parse("0x2A", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal)

    def test_IntLiteral_hex_long(self):
        int_literal = jast.parse("0x2AL", jast.ParseMode.EXPR)
        self._test_int_literal_long(int_literal, long=True)

    def _test_FloatLiteral(self, value, double=False):
        self.assertIsInstance(value, jast.Constant)
        float_literal = value.value
        self.assertIsInstance(float_literal, jast.FloatLiteral)
        self.assertAlmostEqual(3.14, float_literal.value)
        if double:
            self.assertTrue(float_literal.double)
        else:
            self.assertFalse(float_literal.double)

    def test_FloatLiteral(self):
        float_literal = jast.parse("3.14", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal)

    def test_FloatLiteral_double(self):
        float_literal = jast.parse("3.14D", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal, double=True)

    def test_FloatLiteral_exp(self):
        float_literal = jast.parse("3.14E0", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal)

    def test_FloatLiteral_exp_double(self):
        float_literal = jast.parse("3.14e0D", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal, double=True)

    def test_FloatLiteral_exp_neg(self):
        float_literal = jast.parse("3.14E-0", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal)

    def test_FloatLiteral_exp_neg_double(self):
        float_literal = jast.parse("3.14e-0D", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal, double=True)

    def test_FloatLiteral_exp_pos(self):
        float_literal = jast.parse("3.14E+0", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal)

    def test_FloatLiteral_exp_pos_double(self):
        float_literal = jast.parse("3.14e+0D", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal, double=True)

    def test_FloatLiteral_hex(self):
        float_literal = jast.parse("0x1.91eb851eb851fp+1", jast.ParseMode.EXPR)
        self._test_FloatLiteral(float_literal)

    def test_CharLiteral(self):
        char_literal = jast.parse("'a'", jast.ParseMode.EXPR)
        self.assertIsInstance(char_literal, jast.Constant)
        self.assertIsInstance(char_literal.value, jast.CharLiteral)
        self.assertEqual("a", char_literal.value.value)

    def test_StringLiteral(self):
        string_literal = jast.parse('"foo"', jast.ParseMode.EXPR)
        self.assertIsInstance(string_literal, jast.Constant)
        self.assertIsInstance(string_literal.value, jast.StringLiteral)
        self.assertEqual("foo", string_literal.value.value)

    def test_TextBlock(self):
        text_block = jast.parse('"""\nfoo"""', jast.ParseMode.EXPR)
        self.assertIsInstance(text_block, jast.Constant)
        self.assertIsInstance(text_block.value, jast.TextBlock)
        self.assertEqual(["foo"], text_block.value.value)

    def test_TextBlock_new_line(self):
        text_block = jast.parse('"""\nfoo\n"""', jast.ParseMode.EXPR)
        self.assertIsInstance(text_block, jast.Constant)
        self.assertIsInstance(text_block.value, jast.TextBlock)
        self.assertEqual(["foo", ""], text_block.value.value)

    def test_TextBlock_different_indents(self):
        text_block = jast.parse(
            '"""\n  foo\n\t  bar\n    \n\t\t\tbaz\n  """', jast.ParseMode.EXPR
        )
        self.assertIsInstance(text_block, jast.Constant)
        self.assertIsInstance(text_block.value, jast.TextBlock)
        self.assertEqual(["foo", " bar", "", "\tbaz", ""], text_block.value.value)

    def test_Null(self):
        null = jast.parse("null", jast.ParseMode.EXPR)
        self.assertIsInstance(null, jast.Constant)
        self.assertIsInstance(null.value, jast.NullLiteral)
        self.assertIsNone(null.value.value)

    def _test_modifier_class(self, tree, expected):
        self.assertIsInstance(tree, jast.Class)
        modifiers = tree.modifiers
        self.assertEqual(1, len(modifiers))
        modifier = modifiers[0]
        self.assertIsInstance(modifier, expected)

    def _test_modifier_method(self, tree, expected):
        self.assertIsInstance(tree, jast.Method)
        modifiers = tree.modifiers
        self.assertEqual(1, len(modifiers))
        modifier = modifiers[0]
        self.assertIsInstance(modifier, expected)

    def test_Abstract(self):
        self._test_modifier_class(
            jast.parse("abstract class A {}", jast.ParseMode.DECL), jast.Abstract
        )

    def test_Default(self):
        self._test_modifier_method(
            jast.parse("default int foo();", jast.ParseMode.DECL), jast.Default
        )

    def test_Final(self):
        self._test_modifier_class(
            jast.parse("final class A {}", jast.ParseMode.DECL), jast.Final
        )

    def test_Native(self):
        self._test_modifier_class(
            jast.parse("native class A {}", jast.ParseMode.DECL), jast.Native
        )

    def test_Public(self):
        self._test_modifier_class(
            jast.parse("public class A {}", jast.ParseMode.DECL), jast.Public
        )

    def test_Protected(self):
        self._test_modifier_class(
            jast.parse("protected class A {}", jast.ParseMode.DECL), jast.Protected
        )

    def test_Private(self):
        self._test_modifier_class(
            jast.parse("private class A {}", jast.ParseMode.DECL), jast.Private
        )

    def test_Static(self):
        self._test_modifier_class(
            jast.parse("static class A {}", jast.ParseMode.DECL), jast.Static
        )

    def test_Sealed(self):
        self._test_modifier_class(
            jast.parse("sealed class A {}", jast.ParseMode.DECL), jast.Sealed
        )

    def test_NonSealed(self):
        self._test_modifier_class(
            jast.parse("non-sealed class A {}", jast.ParseMode.DECL), jast.NonSealed
        )

    def test_Strictfp(self):
        self._test_modifier_class(
            jast.parse("strictfp class A {}", jast.ParseMode.DECL), jast.Strictfp
        )

    def test_Synchronized(self):
        self._test_modifier_method(
            jast.parse("synchronized int foo();", jast.ParseMode.DECL),
            jast.Synchronized,
        )

    def test_Transient(self):
        self._test_modifier_class(
            jast.parse("transient class A {}", jast.ParseMode.DECL), jast.Transient
        )

    def test_Transitive(self):
        tree = jast.parse("module A { requires transitive a; }", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Module)
        self.assertEqual(1, len(tree.directives))
        directive = tree.directives[0]
        self.assertIsInstance(directive, jast.Requires)
        self.assertEqual(1, len(directive.modifiers))
        modifier = directive.modifiers[0]
        self.assertIsInstance(modifier, jast.Transitive)

    def test_Volatile(self):
        self._test_modifier_class(
            jast.parse("volatile class A {}", jast.ParseMode.DECL), jast.Volatile
        )

    def test_Annotation(self):
        tree = jast.parse(
            "@foo({1, 42}) @bar(x=1, y=42) class A {}", jast.ParseMode.DECL
        )
        self.assertIsInstance(tree, jast.Class)
        self.assertEqual(2, len(tree.modifiers))
        annotation = tree.modifiers[0]
        self.assertIsInstance(annotation, jast.Annotation)
        self.assertEqual("foo", jast.unparse(annotation.name))
        self.assertEqual(1, len(annotation.elements))
        element = annotation.elements[0]
        self.assertIsInstance(element, jast.elementarrayinit)
        self.assertEqual(2, len(element.values))
        self._test_int_constant(element.values[0], 1)
        self._test_int_constant(element.values[1], 42)
        annotation = tree.modifiers[1]
        self.assertIsInstance(annotation, jast.Annotation)
        self.assertEqual("bar", jast.unparse(annotation.name))
        self.assertEqual(2, len(annotation.elements))
        element = annotation.elements[0]
        self.assertIsInstance(element, jast.elementvaluepair)
        self.assertEqual("x", element.id)
        self._test_int_constant(element.value, 1)
        element = annotation.elements[1]
        self.assertIsInstance(element, jast.elementvaluepair)
        self.assertEqual("y", element.id)
        self._test_int_constant(element.value, 42)

    def test_Void(self):
        tree = jast.parse("void foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Void)

    def test_Var(self):
        tree = jast.parse("var x = 42;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalVariable)
        self.assertIsInstance(tree.type, jast.Var)

    def test_Boolean(self):
        tree = jast.parse("boolean foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Boolean)

    def test_Byte(self):
        tree = jast.parse("byte foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Byte)

    def test_Short(self):
        tree = jast.parse("short foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Short)

    def test_Int(self):
        tree = jast.parse("int foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Int)

    def test_Long(self):
        tree = jast.parse("long foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Long)

    def test_Char(self):
        tree = jast.parse("char foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Char)

    def test_Float(self):
        tree = jast.parse("float foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Float)

    def test_Double(self):
        tree = jast.parse("double foo() {}", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Double)

    def _test_Wildcard(self, tree, extends, super_):
        self.assertIsInstance(tree, jast.LocalVariable)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("List", coit.id)
        self.assertEqual(1, len(coit.type_args.types))
        type_arg = coit.type_args.types[0]
        self.assertIsInstance(type_arg, jast.Wildcard)
        if extends or super_:
            self.assertIsNotNone(type_arg.bound)
            self.assertIsInstance(type_arg.bound, jast.wildcardbound)
            if extends:
                self.assertTrue(type_arg.bound.extends)
                self.assertFalse(type_arg.bound.super_)
            else:
                self.assertFalse(type_arg.bound.extends)
                self.assertTrue(type_arg.bound.super_)
            self.assertIsInstance(type_arg.bound.type, jast.ClassType)
            self.assertEqual(1, len(type_arg.bound.type.coits))
            coit = type_arg.bound.type.coits[0]
            self.assertIsInstance(coit, jast.Coit)
            self.assertEqual("Int", coit.id)
        else:
            self.assertIsNone(type_arg.bound)

    def test_Wildcard(self):
        self._test_Wildcard(
            jast.parse("List<?> list;", jast.ParseMode.STMT), False, False
        )

    def test_Wildcard_extends(self):
        self._test_Wildcard(
            jast.parse("List<? extends Int> list;", jast.ParseMode.STMT), True, False
        )

    def test_Wildcard_super(self):
        self._test_Wildcard(
            jast.parse("List<? super Int> list;", jast.ParseMode.STMT), False, True
        )

    def test_typeargs(self):
        tree = jast.parse("List<int, boolean> list;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalVariable)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("List", coit.id)
        self.assertEqual(2, len(coit.type_args.types))
        self.assertIsInstance(coit.type_args.types[0], jast.Int)
        self.assertIsInstance(coit.type_args.types[1], jast.Boolean)

    def test_ClassType(self):
        tree = jast.parse("List.ArrayList<int> list;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalVariable)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(2, len(tree.type.coits))
        self.assertIsInstance(tree.type.coits[0], jast.Coit)
        self.assertEqual("List", tree.type.coits[0].id)
        self.assertIsNone(tree.type.coits[0].type_args)
        self.assertIsInstance(tree.type.coits[1], jast.Coit)
        self.assertEqual("ArrayList", tree.type.coits[1].id)
        self.assertIsNotNone(tree.type.coits[1].type_args)
        self.assertEqual(1, len(tree.type.coits[1].type_args.types))
        self.assertIsInstance(tree.type.coits[1].type_args.types[0], jast.Int)

    def test_Coit_annotation(self):
        tree = jast.parse("List.@foo()ArrayList::<int>new", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(2, len(tree.type.coits))
        self.assertIsInstance(tree.type.coits[0], jast.Coit)
        self.assertEqual("List", tree.type.coits[0].id)
        self.assertIsInstance(tree.type.coits[1], jast.Coit)
        self.assertEqual("ArrayList", tree.type.coits[1].id)
        self.assertIsNotNone(tree.type.coits[1].annotations)
        self.assertEqual(1, len(tree.type.coits[1].annotations))
        annotation = tree.type.coits[1].annotations[0]
        self.assertIsInstance(annotation, jast.Annotation)
        self.assertEqual("foo", jast.unparse(annotation.name))

    def test_ArrayType(self):
        tree = jast.parse("int[][] array;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalVariable)
        self.assertIsInstance(tree.type, jast.ArrayType)
        self.assertIsInstance(tree.type.type, jast.Int)
        self.assertEqual(2, len(tree.type.dims))
        self.assertIsInstance(tree.type.dims[0], jast.dim)
        self.assertIsInstance(tree.type.dims[1], jast.dim)

    def test_variabledeclaratorid(self):
        tree = jast.parse("int x, y[][];", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Field)
        self.assertEqual(2, len(tree.declarators))
        self.assertIsInstance(tree.declarators[0], jast.declarator)
        x = tree.declarators[0].id
        self.assertIsInstance(x, jast.variabledeclaratorid)
        self.assertEqual("x", x.id)
        self.assertEqual(0, len(x.dims))
        y = tree.declarators[1].id
        self.assertIsInstance(y, jast.variabledeclaratorid)
        self.assertEqual("y", y.id)
        self.assertEqual(2, len(y.dims))
        self.assertIsInstance(y.dims[0], jast.dim)
        self.assertIsInstance(y.dims[1], jast.dim)

    def test_typeparams(self):
        tree = jast.parse(
            "class A<@foo B, C extends @bar int & float> {}", jast.ParseMode.DECL
        )
        self.assertIsInstance(tree, jast.Class)
        self.assertIsNotNone(tree.type_params)
        self.assertIsInstance(tree.type_params, jast.typeparams)
        self.assertEqual(2, len(tree.type_params.parameters))
        b = tree.type_params.parameters[0]
        self.assertIsInstance(b, jast.typeparam)
        self.assertEqual(1, len(b.annotations))
        self.assertIsInstance(b.annotations[0], jast.Annotation)
        self.assertEqual("foo", jast.unparse(b.annotations[0].name))
        self.assertIsNone(b.annotations[0].elements)
        self.assertEqual("B", b.id)
        self.assertIsNone(b.bound)
        c = tree.type_params.parameters[1]
        self.assertIsInstance(c, jast.typeparam)
        self.assertEqual(0, len(c.annotations))
        self.assertEqual("C", c.id)
        self.assertIsNotNone(c.bound)
        self.assertEqual(1, len(c.bound.annotations))
        self.assertIsInstance(c.bound.annotations[0], jast.Annotation)
        self.assertEqual("bar", jast.unparse(c.bound.annotations[0].name))
        self.assertEqual(2, len(c.bound.types))
        self.assertIsInstance(c.bound.types[0], jast.Int)
        self.assertIsInstance(c.bound.types[1], jast.Float)

    def test_pattern(self):
        tree = jast.parse("x instanceof final int @foo y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.InstanceOf)
        pattern = tree.type
        self.assertIsInstance(pattern, jast.pattern)
        self.assertEqual(1, len(pattern.modifiers))
        self.assertIsInstance(pattern.modifiers[0], jast.Final)
        self.assertIsInstance(pattern.type, jast.Int)
        self.assertEqual(1, len(pattern.annotations))
        self.assertIsInstance(pattern.annotations[0], jast.Annotation)
        self.assertEqual("foo", jast.unparse(pattern.annotations[0].name))
        self.assertIsInstance(pattern.id, jast.identifier)
        self.assertEqual("y", pattern.id)

    def test_guardedpattern(self):
        tree = jast.parse(
            "switch (x) {case (final int @foo y && true) && 42: ;}", jast.ParseMode.EXPR
        )
        self.assertIsInstance(tree, jast.SwitchExp)
        self.assertEqual(1, len(tree.rules))
        rule = tree.rules[0]
        self.assertEqual(1, len(rule.cases))
        guardedpattern = rule.cases[0]
        self.assertIsInstance(guardedpattern, jast.guardedpattern)
        pattern = guardedpattern.value
        self.assertIsInstance(pattern, jast.pattern)
        self.assertEqual(1, len(pattern.modifiers))
        self.assertIsInstance(pattern.modifiers[0], jast.Final)
        self.assertIsInstance(pattern.type, jast.Int)
        self.assertEqual(1, len(pattern.annotations))
        self.assertIsInstance(pattern.annotations[0], jast.Annotation)
        self.assertEqual("foo", jast.unparse(pattern.annotations[0].name))
        self.assertIsInstance(pattern.id, jast.identifier)
        self.assertEqual("y", pattern.id)
        self.assertEqual(2, len(guardedpattern.conditions))
        self._test_bool_constant(guardedpattern.conditions[0], True)
        self._test_int_constant(guardedpattern.conditions[1], 42)

    def _test_operator(self, tree, operator):
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, operator)

    def _test_unaryop(self, tree, operator):
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, operator)

    def _test_postop(self, tree, operator):
        self.assertIsInstance(tree, jast.PostOp)
        self.assertIsInstance(tree.op, operator)

    def test_Or(self):
        self._test_operator(jast.parse("x || y", jast.ParseMode.EXPR), jast.Or)

    def test_And(self):
        self._test_operator(jast.parse("x && y", jast.ParseMode.EXPR), jast.And)

    def test_BitOr(self):
        self._test_operator(jast.parse("x | y", jast.ParseMode.EXPR), jast.BitOr)

    def test_BitXor(self):
        self._test_operator(jast.parse("x ^ y", jast.ParseMode.EXPR), jast.BitXor)

    def test_BitAnd(self):
        self._test_operator(jast.parse("x & y", jast.ParseMode.EXPR), jast.BitAnd)

    def test_Eq(self):
        self._test_operator(jast.parse("x == y", jast.ParseMode.EXPR), jast.Eq)

    def test_NotEq(self):
        self._test_operator(jast.parse("x != y", jast.ParseMode.EXPR), jast.NotEq)

    def test_Lt(self):
        self._test_operator(jast.parse("x < y", jast.ParseMode.EXPR), jast.Lt)

    def test_LtE(self):
        self._test_operator(jast.parse("x <= y", jast.ParseMode.EXPR), jast.LtE)

    def test_Gt(self):
        self._test_operator(jast.parse("x > y", jast.ParseMode.EXPR), jast.Gt)

    def test_GtE(self):
        self._test_operator(jast.parse("x >= y", jast.ParseMode.EXPR), jast.GtE)

    def test_LShift(self):
        self._test_operator(jast.parse("x << y", jast.ParseMode.EXPR), jast.LShift)

    def test_RShift(self):
        self._test_operator(jast.parse("x >> y", jast.ParseMode.EXPR), jast.RShift)

    def test_URShift(self):
        self._test_operator(jast.parse("x >>> y", jast.ParseMode.EXPR), jast.URShift)

    def test_Add(self):
        self._test_operator(jast.parse("x + y", jast.ParseMode.EXPR), jast.Add)

    def test_Sub(self):
        self._test_operator(jast.parse("x - y", jast.ParseMode.EXPR), jast.Sub)

    def test_Mult(self):
        self._test_operator(jast.parse("x * y", jast.ParseMode.EXPR), jast.Mult)

    def test_Div(self):
        self._test_operator(jast.parse("x / y", jast.ParseMode.EXPR), jast.Div)

    def test_Mod(self):
        self._test_operator(jast.parse("x % y", jast.ParseMode.EXPR), jast.Mod)

    def test_PreInc(self):
        self._test_unaryop(jast.parse("++x", jast.ParseMode.EXPR), jast.PreInc)

    def test_PreDec(self):
        self._test_unaryop(jast.parse("--x", jast.ParseMode.EXPR), jast.PreDec)

    def test_UAdd(self):
        self._test_unaryop(jast.parse("+x", jast.ParseMode.EXPR), jast.UAdd)

    def test_USub(self):
        self._test_unaryop(jast.parse("-x", jast.ParseMode.EXPR), jast.USub)

    def test_Invert(self):
        self._test_unaryop(jast.parse("~x", jast.ParseMode.EXPR), jast.Invert)

    def test_Not(self):
        self._test_unaryop(jast.parse("!x", jast.ParseMode.EXPR), jast.Not)

    def test_PostInc(self):
        self._test_postop(jast.parse("x++", jast.ParseMode.EXPR), jast.PostInc)

    def test_PostDec(self):
        self._test_postop(jast.parse("x--", jast.ParseMode.EXPR), jast.PostDec)

    def test_Lambda_identifier(self):
        tree = jast.parse("x -> x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Lambda)
        self.assertIsInstance(tree.args, jast.identifier)
        self.assertEqual("x", tree.args)
        self.assertIsInstance(tree.body, jast.Name)
        self.assertEqual("x", tree.body.id)

    def test_Lambda_identifiers(self):
        tree = jast.parse("(x, y) -> x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Lambda)
        self.assertIsInstance(tree.args, list)
        self.assertEqual(2, len(tree.args))
        self.assertIsInstance(tree.args[0], jast.identifier)
        self.assertEqual("x", tree.args[0])
        self.assertIsInstance(tree.args[1], jast.identifier)
        self.assertEqual("y", tree.args[1])
        self.assertIsInstance(tree.body, jast.Name)
        self.assertEqual("x", tree.body.id)

    def test_Lambda_identifiers_empty(self):
        tree = jast.parse("() -> x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Lambda)
        self.assertIsInstance(tree.args, list)
        self.assertEqual(0, len(tree.args))
        self.assertIsInstance(tree.body, jast.Name)
        self.assertEqual("x", tree.body.id)

    def test_Lambda_parameters(self):
        tree = jast.parse("(int x, boolean y) -> x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Lambda)
        self.assertIsInstance(tree.args, jast.params)
        self.assertIsNone(tree.args.receiver_param)
        self.assertEqual(2, len(tree.args.parameters))
        param = tree.args.parameters[0]
        self.assertIsInstance(param, jast.param)
        self.assertIsInstance(param.type, jast.Int)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self.assertEqual("x", jast.unparse(param.id))
        param = tree.args.parameters[1]
        self.assertIsInstance(param, jast.param)
        self.assertIsInstance(param.type, jast.Boolean)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self.assertEqual("y", jast.unparse(param.id))

    def test_Lambda_var_parameters(self):
        tree = jast.parse("(var x, var y) -> x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Lambda)
        self.assertIsInstance(tree.args, jast.params)
        self.assertIsNone(tree.args.receiver_param)
        self.assertEqual(2, len(tree.args.parameters))
        param = tree.args.parameters[0]
        self.assertIsInstance(param, jast.param)
        self.assertIsInstance(param.type, jast.Var)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self.assertEqual("x", jast.unparse(param.id))
        param = tree.args.parameters[1]
        self.assertIsInstance(param, jast.param)
        self.assertIsInstance(param.type, jast.Var)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self.assertEqual("y", jast.unparse(param.id))

    def test_Assign(self):
        tree = jast.parse("x = y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Assign)
        self.assertIsInstance(tree.target, jast.Name)
        self.assertEqual("x", tree.target.id)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("y", tree.value.id)

    def test_Assign_parens_left(self):
        tree = jast.parse("x = y = z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Assign)
        self.assertIsInstance(tree.target, jast.Name)
        self.assertEqual("x", tree.target.id)
        self.assertIsInstance(tree.value, jast.Assign)
        self.assertIsInstance(tree.value.target, jast.Name)
        self.assertEqual("y", tree.value.target.id)
        self.assertIsInstance(tree.value.value, jast.Name)
        self.assertEqual("z", tree.value.value.id)

    def test_Assign_parens_right(self):
        tree = jast.parse("(x = y) = z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Assign)
        self.assertIsInstance(tree.target, jast.Assign)
        self.assertIsInstance(tree.target.target, jast.Name)
        self.assertEqual("x", tree.target.target.id)
        self.assertIsInstance(tree.target.value, jast.Name)
        self.assertEqual("y", tree.target.value.id)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("z", tree.value.id)

    def _test_assign_op(self, tree, operator):
        self.assertIsInstance(tree, jast.Assign)
        self.assertIsInstance(tree, jast.Assign)
        self.assertIsInstance(tree.target, jast.Name)
        self.assertEqual("x", tree.target.id)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("y", tree.value.id)
        self.assertIsInstance(tree.op, operator)

    @parameterized.expand(OPERATORS_ASSIGN)
    def test_Assign_op(self, _, rep, operator):
        self._test_assign_op(jast.parse(f"x {rep}= y", jast.ParseMode.EXPR), operator)

    def test_IfExp(self):
        tree = jast.parse("x ? y : z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.IfExp)
        self.assertIsInstance(tree.test, jast.Name)
        self.assertEqual("x", tree.test.id)
        self.assertIsInstance(tree.body, jast.Name)
        self.assertEqual("y", tree.body.id)
        self.assertIsInstance(tree.orelse, jast.Name)
        self.assertEqual("z", tree.orelse.id)

    def test_IfExp_parens_right(self):
        tree = jast.parse("x ? y : z ? a : b", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.IfExp)
        self.assertIsInstance(tree.test, jast.Name)
        self.assertEqual("x", tree.test.id)
        self.assertIsInstance(tree.body, jast.Name)
        self.assertEqual("y", tree.body.id)
        self.assertIsInstance(tree.orelse, jast.IfExp)
        self.assertIsInstance(tree.orelse.test, jast.Name)
        self.assertEqual("z", tree.orelse.test.id)
        self.assertIsInstance(tree.orelse.body, jast.Name)
        self.assertEqual("a", tree.orelse.body.id)
        self.assertIsInstance(tree.orelse.orelse, jast.Name)
        self.assertEqual("b", tree.orelse.orelse.id)

    def test_IfExp_parens_left(self):
        tree = jast.parse("(x ? y : z) ? a : b", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.IfExp)
        self.assertIsInstance(tree.test, jast.IfExp)
        self.assertIsInstance(tree.test.test, jast.Name)
        self.assertEqual("x", tree.test.test.id)
        self.assertIsInstance(tree.test.body, jast.Name)
        self.assertEqual("y", tree.test.body.id)
        self.assertIsInstance(tree.test.orelse, jast.Name)
        self.assertEqual("z", tree.test.orelse.id)
        self.assertIsInstance(tree.body, jast.Name)
        self.assertEqual("a", tree.body.id)
        self.assertIsInstance(tree.orelse, jast.Name)
        self.assertEqual("b", tree.orelse.id)

    # noinspection PyUnusedLocal
    @parameterized.expand(OPERATORS)
    def test_BinOp(self, name, rep, operator):
        tree = jast.parse("x " + rep + " y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, operator)
        self.assertIsInstance(tree.left, jast.Name)
        self.assertEqual("x", tree.left.id)
        self.assertIsInstance(tree.right, jast.Name)
        self.assertEqual("y", tree.right.id)

    def _test_BinOp_right(self, tree, operator1, operator2):
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, operator1)
        self.assertIsInstance(tree.left, jast.Name)
        self.assertEqual("x", tree.left.id)
        self.assertIsInstance(tree.right, jast.BinOp)
        self.assertIsInstance(tree.right.op, operator2)
        self.assertIsInstance(tree.right.left, jast.Name)
        self.assertEqual("y", tree.right.left.id)
        self.assertIsInstance(tree.right.right, jast.Name)
        self.assertEqual("z", tree.right.right.id)

    @parameterized.expand(RIGHT_PRECEDENCE_FOR_LEFT)
    def test_BinOp_order(self, _, rep1, rep2, operator1, operator2):
        self._test_BinOp_right(
            jast.parse(f"x {rep1} y {rep2} z", jast.ParseMode.EXPR),
            operator1,
            operator2,
        )

    @parameterized.expand(LEFT_PRECEDENCE_FOR_RIGHT)
    def test_BinOp_order_parens(self, _, rep1, rep2, operator1, operator2):
        self._test_BinOp_right(
            jast.parse(f"x {rep1} (y {rep2} z)", jast.ParseMode.EXPR),
            operator1,
            operator2,
        )

    def _test_BinOp_left(self, tree, operator1, operator2):
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, operator2)
        self.assertIsInstance(tree.left, jast.BinOp)
        self.assertIsInstance(tree.left.op, operator1)
        self.assertIsInstance(tree.left.left, jast.Name)
        self.assertEqual("x", tree.left.left.id)
        self.assertIsInstance(tree.left.right, jast.Name)
        self.assertEqual("y", tree.left.right.id)
        self.assertIsInstance(tree.right, jast.Name)
        self.assertEqual("z", tree.right.id)

    @parameterized.expand(LEFT_PRECEDENCE_FOR_RIGHT)
    def test_BinOp_reversed(self, _, rep1, rep2, operator1, operator2):
        self._test_BinOp_left(
            jast.parse(f"x {rep1} y {rep2} z", jast.ParseMode.EXPR),
            operator1,
            operator2,
        )

    @parameterized.expand(RIGHT_PRECEDENCE_FOR_LEFT)
    def test_BinOp_reversed_parens(self, _, rep1, rep2, operator1, operator2):
        self._test_BinOp_left(
            jast.parse(f"(x {rep1} y) {rep2} z", jast.ParseMode.EXPR),
            operator1,
            operator2,
        )

    def test_Instanceof(self):
        tree = jast.parse("x instanceof y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.InstanceOf)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("x", tree.value.id)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("y", coit.id)

    def _test_Instanceof_left(self, tree, operator):
        self.assertIsInstance(tree, jast.InstanceOf)
        self.assertIsInstance(tree.value, jast.BinOp)
        self.assertIsInstance(tree.value.op, operator)
        self.assertIsInstance(tree.value.left, jast.Name)
        self.assertEqual("x", tree.value.left.id)
        self.assertIsInstance(tree.value.right, jast.Name)
        self.assertEqual("y", tree.value.right.id)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("z", coit.id)

    @parameterized.expand(INSTANCEOF_HIGHER_SAME_PRECEDENCE)
    def test_Instanceof_order(self, _, rep, operator):
        self._test_Instanceof_left(
            jast.parse(f"x {rep} y instanceof z", jast.ParseMode.EXPR), operator
        )

    @parameterized.expand(INSTANCEOF_LOWER_PRECEDENCE)
    def test_Instanceof_order_parens(self, _, rep, operator):
        self._test_Instanceof_left(
            jast.parse(f"(x {rep} y) instanceof z", jast.ParseMode.EXPR), operator
        )

    def test_Instanceof_left(self):
        tree = jast.parse("x instanceof y instanceof z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.InstanceOf)
        self.assertIsInstance(tree.value, jast.InstanceOf)
        self.assertIsInstance(tree.value.value, jast.Name)
        self.assertEqual("x", tree.value.value.id)
        self.assertIsInstance(tree.value.type, jast.ClassType)
        self.assertEqual(1, len(tree.value.type.coits))
        coit = tree.value.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("y", coit.id)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("z", coit.id)

    def _test_Instanceof_right(self, tree, operator):
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, operator)
        self.assertIsInstance(tree.left, jast.Name)
        self.assertEqual("x", tree.left.id)
        self.assertIsInstance(tree.right, jast.InstanceOf)
        self.assertIsInstance(tree.right.value, jast.Name)
        self.assertEqual("y", tree.right.value.id)
        self.assertIsInstance(tree.right.type, jast.ClassType)
        self.assertEqual(1, len(tree.right.type.coits))
        coit = tree.right.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("z", coit.id)

    @parameterized.expand(INSTANCEOF_HIGHER_SAME_PRECEDENCE)
    def test_Instanceof_reversed(self, _, rep, operator):
        self._test_Instanceof_right(
            jast.parse(f"x {rep} (y instanceof z)", jast.ParseMode.EXPR), operator
        )

    @parameterized.expand(INSTANCEOF_LOWER_PRECEDENCE)
    def test_Instanceof_reversed_parens(self, _, rep, operator):
        self._test_Instanceof_right(
            jast.parse(f"x {rep} y instanceof z", jast.ParseMode.EXPR), operator
        )

    @parameterized.expand(INSTANCEOF_LOWER_SAME_PRECEDENCE)
    def test_Instanceof_BinOp(self, _, rep, operator):
        tree = jast.parse(f"x instanceof y {rep} z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, operator)
        self.assertIsInstance(tree.left, jast.InstanceOf)
        self.assertIsInstance(tree.left.value, jast.Name)
        self.assertEqual("x", tree.left.value.id)
        self.assertIsInstance(tree.left.type, jast.ClassType)
        self.assertEqual(1, len(tree.left.type.coits))
        coit = tree.left.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("y", coit.id)
        self.assertIsInstance(tree.right, jast.Name)
        self.assertEqual("z", tree.right.id)

    @parameterized.expand(UNARY_OPERATORS)
    def test_UnaryOp(self, _, rep, operator):
        tree = jast.parse(f"{rep}x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, operator)
        self.assertIsInstance(tree.operand, jast.Name)
        self.assertEqual("x", tree.operand.id)

    def test_UnaryOp_twice(self):
        tree = jast.parse(f"+-x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, jast.UAdd)
        self.assertIsInstance(tree.operand, jast.UnaryOp)
        self.assertIsInstance(tree.operand.op, jast.USub)
        self.assertIsInstance(tree.operand.operand, jast.Name)
        self.assertEqual("x", tree.operand.operand.id)

    def test_UnaryOp_parens(self):
        tree = jast.parse(f"-(x * y)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, jast.USub)
        self.assertIsInstance(tree.operand, jast.BinOp)
        self.assertIsInstance(tree.operand.op, jast.Mult)
        self.assertIsInstance(tree.operand.left, jast.Name)
        self.assertEqual("x", tree.operand.left.id)
        self.assertIsInstance(tree.operand.right, jast.Name)
        self.assertEqual("y", tree.operand.right.id)

    def test_UnaryOp_no_parens(self):
        tree = jast.parse(f"-x * y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, jast.Mult)
        self.assertIsInstance(tree.left, jast.UnaryOp)
        self.assertIsInstance(tree.left.op, jast.USub)
        self.assertIsInstance(tree.left.operand, jast.Name)
        self.assertEqual("x", tree.left.operand.id)
        self.assertIsInstance(tree.right, jast.Name)
        self.assertEqual("y", tree.right.id)

    def test_UnaryOp_cast(self):
        tree = jast.parse(f"(int) -x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Cast)
        self.assertIsInstance(tree.type, jast.typebound)
        self.assertEqual(1, len(tree.type.types))
        self.assertIsInstance(tree.type.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.UnaryOp)
        self.assertIsInstance(tree.value.op, jast.USub)
        self.assertIsInstance(tree.value.operand, jast.Name)
        self.assertEqual("x", tree.value.operand.id)

    def test_UnaryOp_cast_parens(self):
        tree = jast.parse(f"-((int) x)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, jast.USub)
        self.assertIsInstance(tree.operand, jast.Cast)
        self.assertIsInstance(tree.operand.type, jast.typebound)
        self.assertEqual(1, len(tree.operand.type.types))
        self.assertIsInstance(tree.operand.type.types[0], jast.Int)
        self.assertIsInstance(tree.operand.value, jast.Name)
        self.assertEqual("x", tree.operand.value.id)

    def test_Cast(self):
        tree = jast.parse("(int) x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Cast)
        self.assertIsInstance(tree.type, jast.typebound)
        self.assertEqual(1, len(tree.type.types))
        self.assertIsInstance(tree.type.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("x", tree.value.id)

    def test_Cast_twice(self):
        tree = jast.parse("(int) (long) x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Cast)
        self.assertIsInstance(tree.type, jast.typebound)
        self.assertEqual(1, len(tree.type.types))
        self.assertIsInstance(tree.type.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Cast)
        self.assertIsInstance(tree.value.type, jast.typebound)
        self.assertEqual(1, len(tree.value.type.types))
        self.assertIsInstance(tree.value.type.types[0], jast.Long)
        self.assertIsInstance(tree.value.value, jast.Name)
        self.assertEqual("x", tree.value.value.id)

    def test_Cast_type_bounds(self):
        tree = jast.parse("(int & long) x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Cast)
        self.assertIsInstance(tree.type, jast.typebound)
        self.assertEqual(2, len(tree.type.types))
        self.assertIsInstance(tree.type.types[0], jast.Int)
        self.assertIsInstance(tree.type.types[1], jast.Long)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("x", tree.value.id)

    def test_Cast_parens(self):
        tree = jast.parse("(int) (x * y)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Cast)
        self.assertIsInstance(tree.type, jast.typebound)
        self.assertEqual(1, len(tree.type.types))
        self.assertIsInstance(tree.type.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.BinOp)
        self.assertIsInstance(tree.value.op, jast.Mult)
        self.assertIsInstance(tree.value.left, jast.Name)
        self.assertEqual("x", tree.value.left.id)
        self.assertIsInstance(tree.value.right, jast.Name)
        self.assertEqual("y", tree.value.right.id)

    def test_Cast_no_parens(self):
        tree = jast.parse("(int) x * y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.BinOp)
        self.assertIsInstance(tree.op, jast.Mult)
        self.assertIsInstance(tree.left, jast.Cast)
        self.assertIsInstance(tree.left.type, jast.typebound)
        self.assertEqual(1, len(tree.left.type.types))
        self.assertIsInstance(tree.left.type.types[0], jast.Int)
        self.assertIsInstance(tree.left.value, jast.Name)
        self.assertEqual("x", tree.left.value.id)
        self.assertIsInstance(tree.right, jast.Name)
        self.assertEqual("y", tree.right.id)

    def test_Cast_annotation(self):
        tree = jast.parse("(@foo int) x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Cast)
        self.assertIsInstance(tree.annotations, list)
        self.assertEqual(1, len(tree.annotations))
        annotation = tree.annotations[0]
        self.assertIsInstance(annotation, jast.Annotation)
        self.assertEqual("foo", jast.unparse(annotation.name))
        self.assertIsInstance(tree.type, jast.typebound)
        self.assertEqual(1, len(tree.type.types))
        self.assertIsInstance(tree.type.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("x", tree.value.id)

    def test_NewObject(self):
        tree = jast.parse("new X()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewObject)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("X", coit.id)
        self.assertEqual(0, len(tree.args))
        self.assertIsNone(tree.body)

    def test_NewObject_args(self):
        tree = jast.parse("new X(y, z)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewObject)
        self.assertIsNone(tree.type_args)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("X", coit.id)
        self.assertEqual(2, len(tree.args))
        self.assertIsInstance(tree.args[0], jast.Name)
        self.assertEqual("y", tree.args[0].id)
        self.assertIsInstance(tree.args[1], jast.Name)
        self.assertEqual("z", tree.args[1].id)
        self.assertIsNone(tree.body)

    def test_NewObject_type_args(self):
        tree = jast.parse("new <int, boolean>X()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewObject)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(2, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.type_args.types[1], jast.Boolean)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("X", coit.id)
        self.assertEqual(0, len(tree.args))
        self.assertIsNone(tree.body)

    def test_NewObject_body(self):
        tree = jast.parse("new X() {;;}", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewObject)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("X", coit.id)
        self.assertIsNotNone(tree.body)
        self.assertEqual(2, len(tree.body))
        self.assertIsInstance(tree.body[0], jast.EmptyDecl)
        self.assertIsInstance(tree.body[1], jast.EmptyDecl)

    def test_NewArray(self):
        tree = jast.parse("new int[42]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewArray)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertEqual(1, len(tree.expr_dims))
        expr_dim = tree.expr_dims[0]
        self.assertIsInstance(expr_dim, jast.Constant)
        self.assertIsInstance(expr_dim.value, jast.IntLiteral)
        self.assertEqual(42, expr_dim.value.value)
        self.assertEqual(0, len(tree.dims))
        self.assertIsNone(tree.init)

    def test_NewArray_dims(self):
        tree = jast.parse("new int[42][24][][]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewArray)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertEqual(2, len(tree.expr_dims))
        expr_dim = tree.expr_dims[0]
        self.assertIsInstance(expr_dim, jast.Constant)
        self.assertIsInstance(expr_dim.value, jast.IntLiteral)
        self.assertEqual(42, expr_dim.value.value)
        expr_dim = tree.expr_dims[1]
        self.assertIsInstance(expr_dim, jast.Constant)
        self.assertIsInstance(expr_dim.value, jast.IntLiteral)
        self.assertEqual(24, expr_dim.value.value)
        self.assertEqual(2, len(tree.dims))
        self.assertIsInstance(tree.dims[0], jast.dim)
        self.assertIsInstance(tree.dims[1], jast.dim)
        self.assertIsNone(tree.init)

    def test_NewArray_initializer(self):
        tree = jast.parse("new int[]{42, 24}", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.NewArray)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertEqual(0, len(tree.expr_dims))
        self.assertEqual(1, len(tree.dims))
        self.assertIsInstance(tree.dims[0], jast.dim)
        self.assertIsNotNone(tree.init)
        self.assertIsInstance(tree.init, jast.arrayinit)
        self.assertEqual(2, len(tree.init.values))
        self._test_int_constant(tree.init.values[0], 42)
        self._test_int_constant(tree.init.values[1], 24)

    @parameterized.expand(POST_OPERATORS)
    def test_PostOp(self, _, rep, operator):
        tree = jast.parse(f"x{rep}", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.PostOp)
        self.assertIsInstance(tree.op, operator)
        self._test_name(tree.operand, "x")

    def test_PostOp_twice(self):
        tree = jast.parse(f"x++++", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.PostOp)
        self.assertIsInstance(tree.op, jast.PostInc)
        self.assertIsInstance(tree.operand, jast.PostOp)
        self.assertIsInstance(tree.operand.op, jast.PostInc)
        self._test_name(tree.operand.operand, "x")

    @parameterized.expand(
        [
            [*first, *second]
            for first, second in itertools.product(POST_OPERATORS, UNARY_OPERATORS)
        ]
    )
    def test_postOp_parens(self, _, rep, operator, __, rep2, operator2):
        tree = jast.parse(f"{rep2}x{rep}", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, operator2)
        self.assertIsInstance(tree.operand, jast.PostOp)
        self.assertIsInstance(tree.operand.op, operator)
        self._test_name(tree.operand.operand, "x")

    @parameterized.expand(
        [
            [*first, *second]
            for first, second in itertools.product(POST_OPERATORS, UNARY_OPERATORS)
        ]
    )
    def test_postOp_parens(self, _, rep, operator, __, rep2, operator2):
        tree = jast.parse(f"({rep2}x){rep}", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.PostOp)
        self.assertIsInstance(tree.op, operator)
        self.assertIsInstance(tree.operand, jast.UnaryOp)
        self.assertIsInstance(tree.operand.op, operator2)
        self._test_name(tree.operand.operand, "x")

    def test_SwitchExp(self):
        tree = jast.parse(
            "switch (x) {case y, z: ; case a: {} default:}", jast.ParseMode.EXPR
        )
        self.assertIsInstance(tree, jast.SwitchExp)
        self.assertIsInstance(tree.value, jast.Name)
        self.assertEqual("x", tree.value.id)
        self.assertEqual(3, len(tree.rules))
        rule = tree.rules[0]
        self.assertIsInstance(rule, jast.switchexprule)
        self.assertIsInstance(rule.label, jast.ExpCase)
        self.assertEqual(2, len(rule.cases))
        y = rule.cases[0]
        self.assertIsInstance(y, jast.Name)
        self.assertEqual("y", y.id)
        z = rule.cases[1]
        self.assertIsInstance(z, jast.Name)
        self.assertEqual("z", z.id)
        self.assertEqual(1, len(rule.body))
        self.assertIsInstance(rule.body[0], jast.Empty)
        rule = tree.rules[1]
        self.assertIsInstance(rule, jast.switchexprule)
        self.assertIsInstance(rule.label, jast.ExpCase)
        self.assertEqual(1, len(rule.cases))
        a = rule.cases[0]
        self.assertIsInstance(a, jast.Name)
        self.assertEqual(1, len(rule.body))
        self.assertIsInstance(rule.body[0], jast.Block)
        rule = tree.rules[2]
        self.assertIsInstance(rule, jast.switchexprule)
        self.assertIsInstance(rule.label, jast.ExpDefault)
        self.assertIsNone(rule.cases)
        self.assertEqual(0, len(rule.body))

    def test_This(self):
        tree = jast.parse("this", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.This)

    def test_Super(self):
        tree = jast.parse("super", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Super)
        self.assertIsNone(tree.type_args)
        self.assertIsNone(tree.id)

    def test_Super_in_ExplicitGenericInvocation(self):
        tree = jast.parse("<int> super.<int>x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.ExplicitGenericInvocation)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Super)
        self.assertIsInstance(tree.value.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.value.type_args.types))
        self.assertIsInstance(tree.value.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.value.id, jast.identifier)
        self.assertEqual("x", tree.value.id)

    def test_Super_in_ExplicitGenericInvocation_with_args(self):
        tree = jast.parse("<int> super(42)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.ExplicitGenericInvocation)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Call)
        self.assertIsInstance(tree.value.func, jast.Super)
        self.assertIsNone(tree.value.func.type_args)
        self.assertIsNone(tree.value.func.id)
        self.assertEqual(1, len(tree.value.args))
        self._test_int_constant(tree.value.args[0], 42)

    def test_Constant(self):
        tree = jast.parse("42", jast.ParseMode.EXPR)
        self._test_int_constant(tree, 42)

    def test_Constant_boolean(self):
        tree = jast.parse("true", jast.ParseMode.EXPR)
        self._test_bool_constant(tree, True)

    def test_Name(self):
        tree = jast.parse("x", jast.ParseMode.EXPR)
        self._test_name(tree, "x")

    def test_ClassExpr(self):
        tree = jast.parse("int.class", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.ClassExpr)
        self.assertIsInstance(tree.type, jast.Int)

    def test_ExplicitGenericInvocation(self):
        tree = jast.parse("<int>x()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.ExplicitGenericInvocation)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Call)
        self._test_name(tree.value.func, "x")
        self.assertEqual(0, len(tree.value.args))

    def test_ExplicitGenericInvocation_args(self):
        tree = jast.parse("<int>x(42, 24)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.ExplicitGenericInvocation)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Call)
        self._test_name(tree.value.func, "x")
        self.assertEqual(2, len(tree.value.args))
        self._test_int_constant(tree.value.args[0], 42)
        self._test_int_constant(tree.value.args[1], 24)

    def test_ExplicitGenericInvocation_this(self):
        tree = jast.parse("<int>this(42)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.ExplicitGenericInvocation)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.value, jast.Call)
        self.assertIsInstance(tree.value.func, jast.This)
        self.assertEqual(1, len(tree.value.args))
        self._test_int_constant(tree.value.args[0], 42)

    def test_Subscript(self):
        tree = jast.parse("x[y]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Subscript)
        self._test_name(tree.value, "x")
        self._test_name(tree.index, "y")

    def test_Subscript_primary(self):
        tree = jast.parse("x.y[z]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Subscript)
        self.assertIsInstance(tree.value, jast.Member)
        self._test_name(tree.value.value, "x")
        self._test_name(tree.value.member, "y")
        self._test_name(tree.index, "z")

    def test_Subscript_parens(self):
        tree = jast.parse("(++x)[z]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Subscript)
        self.assertIsInstance(tree.value, jast.UnaryOp)
        self.assertIsInstance(tree.value.op, jast.PreInc)
        self._test_name(tree.value.operand, "x")
        self._test_name(tree.index, "z")

    def test_Subscript_no_parens(self):
        tree = jast.parse("++x[z]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, jast.PreInc)
        self.assertIsInstance(tree.operand, jast.Subscript)
        self._test_name(tree.operand.value, "x")
        self._test_name(tree.operand.index, "z")

    def test_Member(self):
        tree = jast.parse("x.y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self._test_name(tree.member, "y")

    def test_Member_call(self):
        tree = jast.parse("x.y()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self.assertIsInstance(tree.member, jast.Call)
        self._test_name(tree.member.func, "y")
        self.assertEqual(0, len(tree.member.args))

    def test_Member_this(self):
        tree = jast.parse("x.this", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self.assertIsInstance(tree.member, jast.This)

    def test_Member_inner_creation(self):
        tree = jast.parse("x.new <int> Y<>(42) {;}", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self.assertIsInstance(tree.member, jast.NewObject)
        self.assertIsInstance(tree.member.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.member.type_args.types))
        self.assertIsInstance(tree.member.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.member.type, jast.Coit)
        self._test_identifier(tree.member.type.id, "Y")
        self.assertIsInstance(tree.member.type.type_args, jast.typeargs)
        self.assertEqual(0, len(tree.member.type.type_args.types))
        self.assertEqual(1, len(tree.member.args))
        self._test_int_constant(tree.member.args[0], 42)
        self.assertIsNotNone(tree.member.body)
        self.assertEqual(1, len(tree.member.body))
        self.assertIsInstance(tree.member.body[0], jast.EmptyDecl)

    def test_Member_super(self):
        tree = jast.parse("x.super.y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self.assertIsInstance(tree.member, jast.Super)
        self._test_identifier(tree.member.id, "y")

    def test_Member_super_args(self):
        tree = jast.parse("x.super(42)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self.assertIsInstance(tree.member, jast.Call)
        self.assertIsInstance(tree.member.func, jast.Super)
        self.assertEqual(1, len(tree.member.args))
        self._test_int_constant(tree.member.args[0], 42)

    def test_Member_ExplicitGenericInvocation(self):
        tree = jast.parse("x.<int>y()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self._test_name(tree.value, "x")
        self.assertIsInstance(tree.member, jast.ExplicitGenericInvocation)
        self.assertIsInstance(tree.member.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.member.type_args.types))
        self.assertIsInstance(tree.member.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.member.value, jast.Call)
        self._test_name(tree.member.value.func, "y")
        self.assertEqual(0, len(tree.member.value.args))

    def test_Member_primary(self):
        tree = jast.parse("x[42].z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self.assertIsInstance(tree.value, jast.Subscript)
        self._test_name(tree.value.value, "x")
        self._test_int_constant(tree.value.index, 42)
        self._test_name(tree.member, "z")

    def test_Member_primary_reversed(self):
        tree = jast.parse("x.z[42]", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Subscript)
        self.assertIsInstance(tree.value, jast.Member)
        self._test_name(tree.value.value, "x")
        self._test_name(tree.value.member, "z")
        self._test_int_constant(tree.index, 42)

    def test_Member_parens(self):
        tree = jast.parse("(++x).y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Member)
        self.assertIsInstance(tree.value, jast.UnaryOp)
        self.assertIsInstance(tree.value.op, jast.PreInc)
        self._test_name(tree.value.operand, "x")
        self._test_name(tree.member, "y")

    def test_Member_no_parens(self):
        tree = jast.parse("++x.y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, jast.PreInc)
        self.assertIsInstance(tree.operand, jast.Member)
        self._test_name(tree.operand.value, "x")
        self._test_name(tree.operand.member, "y")

    def test_Call(self):
        tree = jast.parse("x()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Call)
        self._test_name(tree.func, "x")
        self.assertEqual(0, len(tree.args))

    def test_Call_args(self):
        tree = jast.parse("x(42, 24)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Call)
        self._test_name(tree.func, "x")
        self.assertEqual(2, len(tree.args))
        self._test_int_constant(tree.args[0], 42)
        self._test_int_constant(tree.args[1], 24)

    def test_Call_this(self):
        tree = jast.parse("this(42)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Call)
        self.assertIsInstance(tree.func, jast.This)
        self.assertEqual(1, len(tree.args))
        self._test_int_constant(tree.args[0], 42)

    def test_Call_super(self):
        tree = jast.parse("super(42)", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Call)
        self.assertIsInstance(tree.func, jast.Super)
        self.assertEqual(1, len(tree.args))
        self._test_int_constant(tree.args[0], 42)

    def test_Call_no_parens(self):
        tree = jast.parse("++x()", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.UnaryOp)
        self.assertIsInstance(tree.op, jast.PreInc)
        self.assertIsInstance(tree.operand, jast.Call)
        self._test_name(tree.operand.func, "x")
        self.assertEqual(0, len(tree.operand.args))

    def test_Reference(self):
        tree = jast.parse("x::<int>y", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self._test_name(tree.type, "x")
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self._test_identifier(tree.id, "y")
        self.assertFalse(tree.new)

    def test_Reference_primary(self):
        tree = jast.parse("x.y::z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self.assertIsInstance(tree.type, jast.Member)
        self._test_name(tree.type.value, "x")
        self._test_name(tree.type.member, "y")
        self._test_identifier(tree.id, "z")
        self.assertFalse(tree.new)

    def test_Reference_twice(self):
        tree = jast.parse("x::<int>y::z", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self.assertIsInstance(tree.type, jast.Reference)
        self._test_name(tree.type.type, "x")
        self.assertIsInstance(tree.type.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type.type_args.types))
        self.assertIsInstance(tree.type.type_args.types[0], jast.Int)
        self._test_identifier(tree.type.id, "y")
        self.assertFalse(tree.type.new)
        self._test_identifier(tree.id, "z")
        self.assertFalse(tree.new)

    def test_Reference_type(self):
        tree = jast.parse("int::<int>x", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self._test_identifier(tree.id, "x")
        self.assertFalse(tree.new)

    def test_Reference_new(self):
        tree = jast.parse("int::new", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertIsNone(tree.id)
        self.assertTrue(tree.new)

    def test_Reference_class_type(self):
        tree = jast.parse("X<int>::<int>new", jast.ParseMode.EXPR)
        self.assertIsInstance(tree, jast.Reference)
        self.assertIsInstance(tree.type, jast.ClassType)
        self.assertEqual(1, len(tree.type.coits))
        coit = tree.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("X", coit.id)
        self.assertIsInstance(coit.type_args, jast.typeargs)
        self.assertEqual(1, len(coit.type_args.types))
        self.assertIsInstance(coit.type_args.types[0], jast.Int)
        self.assertIsInstance(tree.type_args, jast.typeargs)
        self.assertEqual(1, len(tree.type_args.types))
        self.assertIsInstance(tree.type_args.types[0], jast.Int)
        self.assertIsNone(tree.id)
        self.assertTrue(tree.new)

    def test_arrayinit(self):
        tree = jast.parse("int[] x = {42, 24};", jast.ParseMode.DECL)
        self.assertIsInstance(tree, jast.Field)
        self.assertIsInstance(tree.type, jast.ArrayType)
        self.assertIsInstance(tree.type.type, jast.Int)
        self.assertEqual(1, len(tree.type.dims))
        self.assertIsInstance(tree.type.dims[0], jast.dim)
        self.assertEqual(1, len(tree.declarators))
        declarator = tree.declarators[0]
        self.assertIsInstance(declarator, jast.declarator)
        self.assertIsInstance(declarator.id, jast.variabledeclaratorid)
        self._test_identifier(declarator.id.id, "x")
        self.assertEqual(0, len(declarator.id.dims))
        self.assertIsNotNone(declarator.init)
        self.assertIsInstance(declarator.init, jast.arrayinit)
        self.assertEqual(2, len(declarator.init.values))
        self._test_int_constant(declarator.init.values[0], 42)
        self._test_int_constant(declarator.init.values[1], 24)

    def test_params(self):
        tree = jast.parse(
            "int foo(int x.y.this, final int a, final int @bar ... b[][]) {}",
            jast.ParseMode.DECL,
        )
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Int)
        self.assertIsInstance(tree.parameters, jast.params)
        self.assertIsNotNone(tree.parameters.receiver_param)
        self.assertIsInstance(tree.parameters.receiver_param, jast.receiver)
        self.assertIsInstance(tree.parameters.receiver_param.type, jast.Int)
        self.assertEqual(2, len(tree.parameters.receiver_param.identifiers))
        self._test_identifier(tree.parameters.receiver_param.identifiers[0], "x")
        self._test_identifier(tree.parameters.receiver_param.identifiers[1], "y")
        self.assertEqual(2, len(tree.parameters.parameters))
        param = tree.parameters.parameters[0]
        self.assertIsInstance(param, jast.param)
        self.assertEqual(1, len(param.modifiers))
        self.assertIsInstance(param.modifiers[0], jast.Final)
        self.assertIsInstance(param.type, jast.Int)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self._test_identifier(param.id.id, "a")
        self.assertEqual(0, len(param.id.dims))
        param = tree.parameters.parameters[1]
        self.assertIsInstance(param, jast.arity)
        self.assertEqual(1, len(param.modifiers))
        self.assertIsInstance(param.modifiers[0], jast.Final)
        self.assertIsInstance(param.type, jast.Int)
        self.assertEqual(1, len(param.annotations))
        self.assertIsInstance(param.annotations[0], jast.Annotation)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self._test_identifier(param.id.id, "b")
        self.assertEqual(2, len(param.id.dims))
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))

    def test_params_no_receiver(self):
        tree = jast.parse(
            "int foo(int a, int ... b[][]) {}",
            jast.ParseMode.DECL,
        )
        self.assertIsInstance(tree, jast.Method)
        self.assertIsInstance(tree.return_type, jast.Int)
        self.assertIsInstance(tree.parameters, jast.params)
        self.assertIsNone(tree.parameters.receiver_param)
        self.assertEqual(2, len(tree.parameters.parameters))
        param = tree.parameters.parameters[0]
        self.assertIsInstance(param, jast.param)
        self.assertEqual(0, len(param.modifiers))
        self.assertIsInstance(param.type, jast.Int)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self._test_identifier(param.id.id, "a")
        self.assertEqual(0, len(param.id.dims))
        param = tree.parameters.parameters[1]
        self.assertIsInstance(param, jast.arity)
        self.assertEqual(0, len(param.modifiers))
        self.assertIsInstance(param.type, jast.Int)
        self.assertEqual(0, len(param.annotations))
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self._test_identifier(param.id.id, "b")
        self.assertEqual(2, len(param.id.dims))
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))

    def test_Empty(self):
        tree = jast.parse(";", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Empty)

    def test_Block(self):
        tree = jast.parse("{;;}", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Block)
        self.assertEqual(2, len(tree.body))
        self.assertIsInstance(tree.body[0], jast.Empty)
        self.assertIsInstance(tree.body[1], jast.Empty)

    def test_LocalType_class(self):
        tree = jast.parse("class X {}", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalType)
        self.assertIsInstance(tree.decl, jast.Class)
        self._test_identifier(tree.decl.id, "X")
        self.assertIsNone(tree.decl.type_params)
        self.assertEqual(0, len(tree.decl.modifiers))
        self.assertIsNone(tree.decl.extends)
        self.assertEqual(0, len(tree.decl.implements))
        self.assertEqual(0, len(tree.decl.permits))
        self.assertEqual(0, len(tree.decl.body))

    def test_LocalType_interface(self):
        tree = jast.parse("interface X {}", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalType)
        self.assertIsInstance(tree.decl, jast.Interface)
        self._test_identifier(tree.decl.id, "X")
        self.assertIsNone(tree.decl.type_params)
        self.assertEqual(0, len(tree.decl.modifiers))
        self.assertEqual(0, len(tree.decl.extends))
        self.assertEqual(0, len(tree.decl.permits))
        self.assertEqual(0, len(tree.decl.body))

    def test_LocalType_record(self):
        tree = jast.parse("record X() {}", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalType)
        self.assertIsInstance(tree.decl, jast.Record)
        self._test_identifier(tree.decl.id, "X")
        self.assertIsNone(tree.decl.type_params)
        self.assertEqual(0, len(tree.decl.modifiers))
        self.assertEqual(0, len(tree.decl.components))
        self.assertEqual(0, len(tree.decl.implements))
        self.assertEqual(0, len(tree.decl.body))

    def test_LocalVariable(self):
        tree = jast.parse("final int x = 24, y, z = 42;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.LocalVariable)
        self.assertEqual(1, len(tree.modifiers))
        self.assertIsInstance(tree.modifiers[0], jast.Final)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertEqual(3, len(tree.declarators))
        declarator = tree.declarators[0]
        self.assertIsInstance(declarator, jast.declarator)
        self.assertIsInstance(declarator.id, jast.variabledeclaratorid)
        self._test_identifier(declarator.id.id, "x")
        self.assertEqual(0, len(declarator.id.dims))
        self.assertIsNotNone(declarator.init)
        self._test_int_constant(declarator.init, 24)
        declarator = tree.declarators[1]
        self.assertIsInstance(declarator, jast.declarator)
        self.assertIsInstance(declarator.id, jast.variabledeclaratorid)
        self._test_identifier(declarator.id.id, "y")
        self.assertEqual(0, len(declarator.id.dims))
        self.assertIsNone(declarator.init)
        declarator = tree.declarators[2]
        self.assertIsInstance(declarator, jast.declarator)
        self.assertIsInstance(declarator.id, jast.variabledeclaratorid)
        self._test_identifier(declarator.id.id, "z")
        self.assertEqual(0, len(declarator.id.dims))
        self.assertIsNotNone(declarator.init)
        self._test_int_constant(declarator.init, 42)

    def test_Labeled(self):
        tree = jast.parse("foo: ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Labeled)
        self._test_identifier(tree.label, "foo")
        self.assertIsInstance(tree.body, jast.Empty)

    def test_Expression(self):
        tree = jast.parse("x;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Expression)
        self._test_name(tree.value, "x")

    def test_If(self):
        tree = jast.parse("if (x) ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.If)
        self._test_name(tree.test, "x")
        self.assertIsInstance(tree.body, jast.Empty)
        self.assertIsNone(tree.orelse)

    def test_If_orelse(self):
        tree = jast.parse("if (x) ; else ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.If)
        self._test_name(tree.test, "x")
        self.assertIsInstance(tree.body, jast.Empty)
        self.assertIsInstance(tree.orelse, jast.Empty)

    def test_If_orelse_block(self):
        tree = jast.parse("if (x) ; else {;;}", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.If)
        self._test_name(tree.test, "x")
        self.assertIsInstance(tree.body, jast.Empty)
        self.assertIsInstance(tree.orelse, jast.Block)
        self.assertEqual(2, len(tree.orelse.body))
        self.assertIsInstance(tree.orelse.body[0], jast.Empty)
        self.assertIsInstance(tree.orelse.body[1], jast.Empty)

    def test_Assert(self):
        tree = jast.parse("assert x;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Assert)
        self._test_name(tree.test, "x")
        self.assertIsNone(tree.msg)

    def test_Assert_msg(self):
        tree = jast.parse("assert x : y;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Assert)
        self._test_name(tree.test, "x")
        self._test_name(tree.msg, "y")

    def test_Switch(self):
        tree = jast.parse(
            "switch (x) {\n"
            "   case 42:\n"
            "   case 24:\n"
            "       y = x;\n"
            "       return x;\n"
            "   case int z:\n"
            "       return z;\n"
            "   case 0:\n"
            "   default:\n"
            "}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.Switch)
        self._test_name(tree.value, "x")
        self.assertIsNotNone(tree.body)
        block = tree.body
        self.assertEqual(2, len(block.groups))
        group = block.groups[0]
        self.assertIsInstance(group, jast.switchgroup)
        self.assertEqual(2, len(group.labels))
        label = group.labels[0]
        self.assertIsInstance(label, jast.Case)
        self._test_int_constant(label.guard, 42)
        label = group.labels[1]
        self.assertIsInstance(label, jast.Case)
        self._test_int_constant(label.guard, 24)
        self.assertEqual(2, len(group.body))
        self.assertIsInstance(group.body[0], jast.Expression)
        self.assertIsInstance(group.body[1], jast.Return)
        group = block.groups[1]
        self.assertIsInstance(group, jast.switchgroup)
        self.assertEqual(1, len(group.labels))
        label = group.labels[0]
        self.assertIsInstance(label, jast.Case)
        self.assertIsInstance(label.guard, jast.Match)
        self.assertIsInstance(label.guard.type, jast.Int)
        self._test_identifier(label.guard.id, "z")
        self.assertEqual(1, len(group.body))
        self.assertIsInstance(group.body[0], jast.Return)
        self.assertEqual(2, len(block.labels))
        label = block.labels[0]
        self.assertIsInstance(label, jast.Case)
        self._test_int_constant(label.guard, 0)
        label = block.labels[1]
        self.assertIsInstance(label, jast.DefaultCase)

    def test_Throw(self):
        tree = jast.parse("throw x;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Throw)
        self._test_name(tree.exc, "x")

    def test_While(self):
        tree = jast.parse("while (x) ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.While)
        self._test_name(tree.test, "x")
        self.assertIsInstance(tree.body, jast.Empty)

    def test_DoWhile(self):
        tree = jast.parse("do ; while (x);", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.DoWhile)
        self.assertIsInstance(tree.body, jast.Empty)
        self._test_name(tree.test, "x")

    def test_For(self):
        tree = jast.parse("for (int x = 0; x < 10; x++) ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.For)
        self.assertIsInstance(tree.init, jast.LocalVariable)
        self.assertIsInstance(tree.test, jast.BinOp)
        self.assertIsInstance(tree.update, list)
        self.assertEqual(1, len(tree.update))
        self.assertIsInstance(tree.update[0], jast.PostOp)
        self.assertIsInstance(tree.body, jast.Empty)

    def test_For_multiple_init_updated(self):
        tree = jast.parse("for (x = 0, y = 0; x < 10; x++, y++) ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.For)
        self.assertIsInstance(tree.init, list)
        self.assertEqual(2, len(tree.init))
        self.assertIsInstance(tree.init[0], jast.Assign)
        self._test_name(tree.init[0].target, "x")
        self.assertIsNone(tree.init[0].op)
        self._test_int_constant(tree.init[0].value, 0)
        self.assertIsInstance(tree.init[1], jast.Assign)
        self._test_name(tree.init[1].target, "y")
        self.assertIsNone(tree.init[1].op)
        self._test_int_constant(tree.init[1].value, 0)
        self.assertIsInstance(tree.test, jast.BinOp)
        self._test_name(tree.test.left, "x")
        self.assertIsInstance(tree.test.op, jast.Lt)
        self._test_int_constant(tree.test.right, 10)
        self.assertIsInstance(tree.update, list)
        self.assertEqual(2, len(tree.update))
        self.assertIsInstance(tree.update[0], jast.PostOp)
        self._test_name(tree.update[0].operand, "x")
        self.assertIsInstance(tree.update[0].op, jast.PostInc)
        self.assertIsInstance(tree.update[1], jast.PostOp)
        self._test_name(tree.update[1].operand, "y")
        self.assertIsInstance(tree.update[1].op, jast.PostInc)
        self.assertIsInstance(tree.body, jast.Empty)

    def test_ForEach(self):
        tree = jast.parse("for (final int x : y) ;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.ForEach)
        self.assertEqual(1, len(tree.modifiers))
        self.assertIsInstance(tree.modifiers[0], jast.Final)
        self.assertIsInstance(tree.type, jast.Int)
        self.assertIsInstance(tree.id, jast.variabledeclaratorid)
        self._test_identifier(tree.id.id, "x")
        self.assertEqual(0, len(tree.id.dims))
        self._test_name(tree.iter, "y")

    def test_Break(self):
        tree = jast.parse("break;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Break)
        self.assertIsNone(tree.label)

    def test_Break_label(self):
        tree = jast.parse("break foo;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Break)
        self._test_identifier(tree.label, "foo")

    def test_Continue(self):
        tree = jast.parse("continue;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Continue)
        self.assertIsNone(tree.label)

    def test_Continue_label(self):
        tree = jast.parse("continue foo;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Continue)
        self._test_identifier(tree.label, "foo")

    def test_Return(self):
        tree = jast.parse("return;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Return)
        self.assertIsNone(tree.value)

    def test_Return_value(self):
        tree = jast.parse("return x;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Return)
        self._test_name(tree.value, "x")

    def test_Synch(self):
        tree = jast.parse("synchronized (x) {;;}", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Synch)
        self._test_name(tree.lock, "x")
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(2, len(tree.body.body))

    def test_Try(self):
        tree = jast.parse(
            "try {;;} catch (Exception e) {;;} catch (final A | B | C.D f) {;;} finally {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.Try)
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(2, len(tree.body.body))
        self.assertEqual(2, len(tree.catches))
        catch = tree.catches[0]
        self.assertIsInstance(catch, jast.catch)
        self.assertEqual(0, len(catch.modifiers))
        self.assertEqual(1, len(catch.excs))
        self.assertEqual("Exception", jast.unparse(catch.excs[0]))
        self._test_identifier(catch.id, "e")
        self.assertIsInstance(catch.body, jast.Block)
        self.assertEqual(2, len(catch.body.body))
        catch = tree.catches[1]
        self.assertIsInstance(catch, jast.catch)
        self.assertEqual(1, len(catch.modifiers))
        self.assertIsInstance(catch.modifiers[0], jast.Final)
        self.assertEqual(3, len(catch.excs))
        self.assertEqual("A", jast.unparse(catch.excs[0]))
        self.assertEqual("B", jast.unparse(catch.excs[1]))
        self.assertEqual("C.D", jast.unparse(catch.excs[2]))
        self._test_identifier(catch.id, "f")
        self.assertIsInstance(catch.body, jast.Block)
        self.assertEqual(2, len(catch.body.body))
        self.assertIsNotNone(tree.final)
        self.assertIsInstance(tree.final, jast.Block)

    def test_Try_only_final(self):
        tree = jast.parse(
            "try {} finally {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.Try)
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))
        self.assertEqual(0, len(tree.catches))
        self.assertIsNotNone(tree.final)
        self.assertIsInstance(tree.final, jast.Block)

    def test_Try_only_catch(self):
        tree = jast.parse(
            "try {} catch (Exception e) {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.Try)
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))
        self.assertEqual(1, len(tree.catches))
        catch = tree.catches[0]
        self.assertIsInstance(catch, jast.catch)
        self.assertEqual(0, len(catch.modifiers))
        self.assertEqual(1, len(catch.excs))
        self.assertEqual("Exception", jast.unparse(catch.excs[0]))
        self._test_identifier(catch.id, "e")
        self.assertIsInstance(catch.body, jast.Block)
        self.assertEqual(0, len(catch.body.body))
        self.assertIsNone(tree.final)

    def test_TryWithResources(self):
        tree = jast.parse(
            "try (A a = c; final B b = d) {;;} catch (Exception e) {;;} catch (final A | B | C.D f) {;;} finally {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.TryWithResources)
        self.assertEqual(2, len(tree.resources))
        resource = tree.resources[0]
        self.assertIsInstance(resource, jast.resource)
        self.assertIsInstance(resource.type, jast.ClassType)
        self.assertEqual(1, len(resource.type.coits))
        coit = resource.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("A", coit.id)
        self.assertIsNone(coit.type_args)
        self.assertIsInstance(resource.variable, jast.declarator)
        self._test_variabledeclaratorid(resource.variable.id, "a")
        self._test_name(resource.variable.init, "c")
        resource = tree.resources[1]
        self.assertIsInstance(resource, jast.resource)
        self.assertEqual(1, len(resource.modifiers))
        self.assertIsInstance(resource.modifiers[0], jast.Final)
        self.assertIsInstance(resource.type, jast.ClassType)
        self.assertEqual(1, len(resource.type.coits))
        coit = resource.type.coits[0]
        self.assertIsInstance(coit, jast.Coit)
        self.assertEqual("B", coit.id)
        self.assertIsNone(coit.type_args)
        self.assertIsInstance(resource.variable, jast.declarator)
        self._test_variabledeclaratorid(resource.variable.id, "b")
        self._test_name(resource.variable.init, "d")
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(2, len(tree.body.body))
        self.assertEqual(2, len(tree.catches))
        catch = tree.catches[0]
        self.assertIsInstance(catch, jast.catch)
        self.assertEqual(0, len(catch.modifiers))
        self.assertEqual(1, len(catch.excs))
        self.assertEqual("Exception", jast.unparse(catch.excs[0]))
        self._test_identifier(catch.id, "e")
        self.assertIsInstance(catch.body, jast.Block)
        self.assertEqual(2, len(catch.body.body))
        catch = tree.catches[1]
        self.assertIsInstance(catch, jast.catch)
        self.assertEqual(1, len(catch.modifiers))
        self.assertIsInstance(catch.modifiers[0], jast.Final)
        self.assertEqual(3, len(catch.excs))
        self.assertEqual("A", jast.unparse(catch.excs[0]))
        self.assertEqual("B", jast.unparse(catch.excs[1]))
        self.assertEqual("C.D", jast.unparse(catch.excs[2]))
        self._test_identifier(catch.id, "f")
        self.assertIsInstance(catch.body, jast.Block)
        self.assertEqual(2, len(catch.body.body))
        self.assertIsNotNone(tree.final)
        self.assertIsInstance(tree.final, jast.Block)
        self.assertEqual(0, len(tree.final.body))

    def test_TryWithResources_only_final(self):
        tree = jast.parse(
            "try (var a = c) {} finally {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.TryWithResources)
        self.assertEqual(1, len(tree.resources))
        resource = tree.resources[0]
        self.assertIsInstance(resource, jast.resource)
        self.assertIsInstance(resource.type, jast.Var)
        self.assertIsInstance(resource.variable, jast.declarator)
        self._test_variabledeclaratorid(resource.variable.id, "a")
        self._test_name(resource.variable.init, "c")
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))
        self.assertEqual(0, len(tree.catches))
        self.assertIsNotNone(tree.final)
        self.assertIsInstance(tree.final, jast.Block)
        self.assertEqual(0, len(tree.final.body))

    def test_TryWithResources_only_catch(self):
        tree = jast.parse(
            "try (var a = c) {} catch (Exception e) {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.TryWithResources)
        self.assertEqual(1, len(tree.resources))
        resource = tree.resources[0]
        self.assertIsInstance(resource, jast.resource)
        self.assertIsInstance(resource.type, jast.Var)
        self.assertIsInstance(resource.variable, jast.declarator)
        self._test_variabledeclaratorid(resource.variable.id, "a")
        self._test_name(resource.variable.init, "c")
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))
        self.assertIsNotNone(tree.catches)
        catch = tree.catches[0]
        self.assertIsInstance(catch, jast.catch)
        self.assertEqual(0, len(catch.modifiers))
        self.assertEqual(1, len(catch.excs))
        self.assertEqual("Exception", jast.unparse(catch.excs[0]))
        self._test_identifier(catch.id, "e")
        self.assertIsInstance(catch.body, jast.Block)
        self.assertEqual(0, len(catch.body.body))
        self.assertIsNone(tree.final)

    def test_TryWithResources_no_catch_and_final(self):
        tree = jast.parse(
            "try (A.B) {}",
            jast.ParseMode.STMT,
        )
        self.assertIsInstance(tree, jast.TryWithResources)
        self.assertEqual(1, len(tree.resources))
        resource = tree.resources[0]
        self.assertIsInstance(resource, jast.qname)
        self.assertEqual("A.B", jast.unparse(resource))
        self.assertIsInstance(tree.body, jast.Block)
        self.assertEqual(0, len(tree.body.body))
        self.assertEqual(0, len(tree.catches))
        self.assertIsNone(tree.final)

    def test_Yield(self):
        tree = jast.parse("yield x;", jast.ParseMode.STMT)
        self.assertIsInstance(tree, jast.Yield)
        self._test_name(tree.value, "x")
