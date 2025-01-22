import unittest
from typing import List

import jast


class TestConstructors(unittest.TestCase):
    def _test_iteration(self, tree):
        for field, value in tree:
            self.assertIsInstance(field, str)
            self.assertIsInstance(value, jast.JAST | List)
            self.assertTrue(hasattr(tree, field))
            self.assertEqual(getattr(tree, field), value)

    def test_identifier(self):
        identifier = jast.identifier("foo")
        self.assertIsInstance(identifier, str)
        self.assertEqual("foo", identifier)
        self.assertIsInstance(identifier, jast.JAST)
        self._test_iteration(identifier)

    def test_qname(self):
        qname = jast.qname([jast.identifier("foo"), jast.identifier("bar")])
        self.assertIsInstance(qname, jast.qname)
        self.assertEqual(2, len(qname.identifiers))
        self.assertIsInstance(qname.identifiers[0], str)
        self.assertIsInstance(qname.identifiers[0], jast.JAST)
        self.assertIsInstance(qname.identifiers[1], str)
        self.assertIsInstance(qname.identifiers[1], jast.JAST)
        self.assertEqual("foo", qname.identifiers[0])
        self.assertEqual("bar", qname.identifiers[1])
        self._test_iteration(qname)

    def test_qname_error(self):
        self.assertRaises(ValueError, jast.qname, [])
        self.assertRaises(ValueError, jast.qname)

    def test_IntLiteral(self):
        int_literal = jast.IntLiteral(42)
        self.assertIsInstance(int_literal, jast.IntLiteral)
        self.assertIsInstance(int_literal, int)
        self.assertEqual(42, int_literal)
        self.assertFalse(int_literal.long)
        self._test_iteration(int_literal)

    def test_IntLiteral_long(self):
        int_literal = jast.IntLiteral(42, True)
        self.assertIsInstance(int_literal, jast.IntLiteral)
        self.assertIsInstance(int_literal, int)
        self.assertEqual(42, int_literal)
        self.assertTrue(int_literal.long)
        self._test_iteration(int_literal)

    def test_FloatLiteral(self):
        float_literal = jast.FloatLiteral(3.14)
        self.assertIsInstance(float_literal, jast.FloatLiteral)
        self.assertIsInstance(float_literal, float)
        self.assertEqual(3.14, float_literal)
        self.assertFalse(float_literal.double)
        self._test_iteration(float_literal)

    def test_FloatLiteral_double(self):
        float_literal = jast.FloatLiteral(3.14, True)
        self.assertIsInstance(float_literal, jast.FloatLiteral)
        self.assertIsInstance(float_literal, float)
        self.assertEqual(3.14, float_literal)
        self.assertTrue(float_literal.double)
        self._test_iteration(float_literal)

    def test_BoolLiteral(self):
        bool_literal = jast.BoolLiteral(True)
        self.assertIsInstance(bool_literal, jast.BoolLiteral)
        self.assertIsInstance(bool_literal, int)
        self.assertTrue(bool_literal)
        self._test_iteration(bool_literal)

    def test_CharLiteral(self):
        char_literal = jast.CharLiteral("a")
        self.assertIsInstance(char_literal, jast.CharLiteral)
        self.assertIsInstance(char_literal, str)
        self.assertEqual("a", char_literal)
        self._test_iteration(char_literal)

    def test_StringLiteral(self):
        string_literal = jast.StringLiteral("foo")
        self.assertIsInstance(string_literal, jast.StringLiteral)
        self.assertIsInstance(string_literal, str)
        self.assertEqual("foo", string_literal)
        self._test_iteration(string_literal)

    def test_TextBlock(self):
        text_block = jast.TextBlock("foo")
        self.assertIsInstance(text_block, jast.TextBlock)
        self.assertIsInstance(text_block, str)
        self.assertEqual("foo", text_block)
        self._test_iteration(text_block)

    def test_NullLiteral(self):
        null_literal = jast.NullLiteral()
        self.assertIsInstance(null_literal, jast.NullLiteral)
        self.assertIsNone(null_literal.value)
        self._test_iteration(null_literal)

    def test_Abstract(self):
        abstract = jast.Abstract()
        self.assertIsInstance(abstract, jast.Abstract)
        self.assertIsInstance(abstract, jast.JAST)
        self._test_iteration(abstract)

    def test_Default(self):
        default = jast.Default()
        self.assertIsInstance(default, jast.Default)
        self.assertIsInstance(default, jast.JAST)
        self._test_iteration(default)

    def test_Final(self):
        final = jast.Final()
        self.assertIsInstance(final, jast.Final)
        self.assertIsInstance(final, jast.JAST)
        self._test_iteration(final)

    def test_Native(self):
        native = jast.Native()
        self.assertIsInstance(native, jast.Native)
        self.assertIsInstance(native, jast.JAST)
        self._test_iteration(native)

    def test_Public(self):
        public = jast.Public()
        self.assertIsInstance(public, jast.Public)
        self.assertIsInstance(public, jast.JAST)
        self._test_iteration(public)

    def test_Protected(self):
        protected = jast.Protected()
        self.assertIsInstance(protected, jast.Protected)
        self.assertIsInstance(protected, jast.JAST)
        self._test_iteration(protected)

    def test_Private(self):
        private = jast.Private()
        self.assertIsInstance(private, jast.Private)
        self.assertIsInstance(private, jast.JAST)
        self._test_iteration(private)

    def test_Static(self):
        static = jast.Static()
        self.assertIsInstance(static, jast.Static)
        self.assertIsInstance(static, jast.JAST)
        self._test_iteration(static)

    def test_Sealed(self):
        sealed = jast.Sealed()
        self.assertIsInstance(sealed, jast.Sealed)
        self.assertIsInstance(sealed, jast.JAST)
        self._test_iteration(sealed)

    def test_NonSealed(self):
        non_sealed = jast.NonSealed()
        self.assertIsInstance(non_sealed, jast.NonSealed)
        self.assertIsInstance(non_sealed, jast.JAST)
        self._test_iteration(non_sealed)

    def test_Strictfp(self):
        strictfp = jast.Strictfp()
        self.assertIsInstance(strictfp, jast.Strictfp)
        self.assertIsInstance(strictfp, jast.JAST)

    def test_Synchronized(self):
        synchronized = jast.Synchronized()
        self.assertIsInstance(synchronized, jast.Synchronized)
        self.assertIsInstance(synchronized, jast.JAST)
        self._test_iteration(synchronized)

    def test_Transient(self):
        transient = jast.Transient()
        self.assertIsInstance(transient, jast.Transient)
        self.assertIsInstance(transient, jast.JAST)
        self._test_iteration(transient)

    def test_Transitive(self):
        transitive = jast.Transitive()
        self.assertIsInstance(transitive, jast.Transitive)
        self.assertIsInstance(transitive, jast.JAST)
        self._test_iteration(transitive)

    def test_elementvaluepair(self):
        elementvaluepair = jast.elementvaluepair(
            jast.identifier("foo"), jast.Constant(jast.IntLiteral(42))
        )
        self.assertIsInstance(elementvaluepair, jast.elementvaluepair)
        self.assertIsInstance(elementvaluepair, jast.JAST)
        self.assertEqual("foo", elementvaluepair.id)
        self.assertIsInstance(elementvaluepair.value, jast.Constant)
        self.assertIsInstance(elementvaluepair.value.value, jast.IntLiteral)
        self.assertEqual(42, elementvaluepair.value.value)
        self._test_iteration(elementvaluepair)

    def test_elementvaluepair_error(self):
        self.assertRaises(ValueError, jast.elementvaluepair, jast.identifier("foo"))
        self.assertRaises(
            ValueError, jast.elementvaluepair, value=jast.Constant(jast.IntLiteral(42))
        )

    def test_elementarrayinit(self):
        elementarrayinit = jast.elementarrayinit([jast.Constant(jast.IntLiteral(42))])
        self.assertIsInstance(elementarrayinit, jast.elementarrayinit)
        self.assertIsInstance(elementarrayinit, jast.JAST)
        self.assertEqual(1, len(elementarrayinit.values))
        self.assertIsInstance(elementarrayinit.values[0], jast.Constant)
        self.assertIsInstance(elementarrayinit.values[0].value, jast.IntLiteral)
        self.assertEqual(42, elementarrayinit.values[0].value)
        self._test_iteration(elementarrayinit)

    def test_Annotation(self):
        annotation = jast.Annotation(
            jast.qname([jast.identifier("foo")]),
            [
                jast.elementvaluepair(
                    jast.identifier("foo"), jast.Constant(jast.IntLiteral(42))
                ),
            ],
        )
        self.assertIsInstance(annotation, jast.Annotation)
        self.assertIsInstance(annotation, jast.JAST)
        self.assertIsInstance(annotation.name, jast.qname)
        self.assertEqual(1, len(annotation.elements))
        self.assertIsInstance(annotation.elements[0], jast.elementvaluepair)
        self.assertEqual("foo", annotation.elements[0].id)
        value = annotation.elements[0].value
        self.assertIsInstance(value, jast.Constant)
        self.assertIsInstance(value.value, jast.IntLiteral)
        self.assertEqual(42, value.value)
        self._test_iteration(annotation)

    def test_Annotation_error(self):
        self.assertRaises(
            ValueError,
            jast.Annotation,
            elements=[
                jast.elementvaluepair(
                    jast.identifier("foo"), jast.Constant(jast.IntLiteral(42))
                )
            ],
        )

    def test_Void(self):
        void = jast.Void()
        self.assertIsInstance(void, jast.Void)
        self.assertIsInstance(void, jast.JAST)
        self._test_iteration(void)

    def test_Var(self):
        var = jast.Var()
        self.assertIsInstance(var, jast.Var)
        self.assertIsInstance(var, jast.JAST)
        self._test_iteration(var)

    def test_Boolean(self):
        boolean = jast.Boolean()
        self.assertIsInstance(boolean, jast.Boolean)
        self.assertIsInstance(boolean, jast.JAST)
        self._test_iteration(boolean)

    def test_Byte(self):
        byte = jast.Byte()
        self.assertIsInstance(byte, jast.Byte)
        self.assertIsInstance(byte, jast.JAST)
        self._test_iteration(byte)

    def test_Short(self):
        short = jast.Short()
        self.assertIsInstance(short, jast.Short)
        self.assertIsInstance(short, jast.JAST)
        self._test_iteration(short)

    def test_Int(self):
        int_ = jast.Int()
        self.assertIsInstance(int_, jast.Int)
        self.assertIsInstance(int_, jast.JAST)
        self._test_iteration(int_)

    def test_Long(self):
        long = jast.Long()
        self.assertIsInstance(long, jast.Long)
        self.assertIsInstance(long, jast.JAST)
        self._test_iteration(long)

    def test_Char(self):
        char = jast.Char()
        self.assertIsInstance(char, jast.Char)
        self.assertIsInstance(char, jast.JAST)
        self._test_iteration(char)

    def test_Float(self):
        float_ = jast.Float()
        self.assertIsInstance(float_, jast.Float)
        self.assertIsInstance(float_, jast.JAST)
        self._test_iteration(float_)

    def test_Double(self):
        double = jast.Double()
        self.assertIsInstance(double, jast.Double)
        self.assertIsInstance(double, jast.JAST)
        self._test_iteration(double)

    def test_Int_annotation(self):
        int_ = jast.Int([jast.Annotation(jast.qname([jast.identifier("foo")]))])
        self.assertIsInstance(int_, jast.Int)
        self.assertIsInstance(int_, jast.JAST)
        self.assertEqual(1, len(int_.annotations))
        self.assertIsInstance(int_.annotations[0], jast.Annotation)
        self._test_iteration(int_)
