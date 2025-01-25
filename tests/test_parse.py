import unittest

import jast


class TestParse(unittest.TestCase):
    def test_identifier(self):
        name = jast.parse("foo", jast.ParseMode.EXPR)
        self.assertIsInstance(name, jast.Name)
        identifier = name.id
        self.assertIsInstance(identifier, str)
        self.assertEqual(identifier, "foo")
        self.assertIsInstance(identifier, jast.JAST)

    def test_qname(self):
        qname = jast.parse("package foo.bar;", jast.ParseMode.DECL)
        self.assertIsInstance(qname, jast.Package)
        name = qname.name
        self.assertIsInstance(name, jast.qname)
        self.assertEqual(2, len(name.identifiers))
        self.assertEqual("foo", name.identifiers[0])
        self.assertEqual("bar", name.identifiers[1])

    def _test_IntLiteral(self, value, long=False):
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
        self._test_IntLiteral(int_literal)

    def test_IntLiteral_long(self):
        int_literal = jast.parse("42L", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal, long=True)

    def test_IntLiteral_bin(self):
        int_literal = jast.parse("0b101010", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal)

    def test_IntLiteral_bin_long(self):
        int_literal = jast.parse("0b101010L", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal, long=True)

    def test_IntLiteral_oct(self):
        int_literal = jast.parse("0_52", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal)

    def test_IntLiteral_oct_long(self):
        int_literal = jast.parse("0_52L", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal, long=True)

    def test_IntLiteral_hex(self):
        int_literal = jast.parse("0x2A", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal)

    def test_IntLiteral_hex_long(self):
        int_literal = jast.parse("0x2AL", jast.ParseMode.EXPR)
        self._test_IntLiteral(int_literal, long=True)

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
        self.assertIsInstance(element.values[0], jast.Constant)
        self.assertIsInstance(element.values[0].value, jast.IntLiteral)
        self.assertEqual(1, element.values[0].value.value)
        self.assertIsInstance(element.values[1], jast.Constant)
        self.assertIsInstance(element.values[1].value, jast.IntLiteral)
        self.assertEqual(42, element.values[1].value.value)
        annotation = tree.modifiers[1]
        self.assertIsInstance(annotation, jast.Annotation)
        self.assertEqual("bar", jast.unparse(annotation.name))
        self.assertEqual(2, len(annotation.elements))
        element = annotation.elements[0]
        self.assertIsInstance(element, jast.elementvaluepair)
        self.assertEqual("x", element.id)
        self.assertIsInstance(element.value, jast.Constant)
        self.assertIsInstance(element.value.value, jast.IntLiteral)
        self.assertEqual(1, element.value.value)
        element = annotation.elements[1]
        self.assertIsInstance(element, jast.elementvaluepair)
        self.assertEqual("y", element.id)
        self.assertIsInstance(element.value, jast.Constant)
        self.assertIsInstance(element.value.value, jast.IntLiteral)
        self.assertEqual(42, element.value.value)

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
        self.assertIsInstance(guardedpattern.conditions[0], jast.Constant)
        self.assertIsInstance(guardedpattern.conditions[0].value, jast.BoolLiteral)
        self.assertTrue(guardedpattern.conditions[0].value.value)
        self.assertIsInstance(guardedpattern.conditions[1], jast.Constant)
        self.assertIsInstance(guardedpattern.conditions[1].value, jast.IntLiteral)
        self.assertEqual(42, guardedpattern.conditions[1].value.value)

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
        self.assertIsNone(tree.args.receiver_parameter)
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
        self.assertIsNone(tree.args.receiver_parameter)
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
