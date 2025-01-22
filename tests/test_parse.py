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
