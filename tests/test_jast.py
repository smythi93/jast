import unittest

import jast


class TestConstructors(unittest.TestCase):
    def test_identifier(self):
        identifier = jast.identifier("foo")
        self.assertIsInstance(identifier, str)
        self.assertEqual("foo", identifier)
        self.assertIsInstance(identifier, jast.JAST)

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

    def test_IntLiteral(self):
        int_literal = jast.IntLiteral(42)
        self.assertIsInstance(int_literal, jast.IntLiteral)
        self.assertIsInstance(int_literal, int)
        self.assertEqual(42, int_literal)
        self.assertFalse(int_literal.long)

    def test_IntLiteral_long(self):
        int_literal = jast.IntLiteral(42, True)
        self.assertIsInstance(int_literal, jast.IntLiteral)
        self.assertIsInstance(int_literal, int)
        self.assertEqual(42, int_literal)
        self.assertTrue(int_literal.long)

    def test_FloatLiteral(self):
        float_literal = jast.FloatLiteral(3.14)
        self.assertIsInstance(float_literal, jast.FloatLiteral)
        self.assertIsInstance(float_literal, float)
        self.assertEqual(3.14, float_literal)
        self.assertFalse(float_literal.double)

    def test_FloatLiteral_double(self):
        float_literal = jast.FloatLiteral(3.14, True)
        self.assertIsInstance(float_literal, jast.FloatLiteral)
        self.assertIsInstance(float_literal, float)
        self.assertEqual(3.14, float_literal)
        self.assertTrue(float_literal.double)

    def test_BoolLiteral(self):
        bool_literal = jast.BoolLiteral(True)
        self.assertIsInstance(bool_literal, jast.BoolLiteral)
        self.assertIsInstance(bool_literal, int)
        self.assertTrue(bool_literal)

    def test_CharLiteral(self):
        char_literal = jast.CharLiteral("a")
        self.assertIsInstance(char_literal, jast.CharLiteral)
        self.assertIsInstance(char_literal, str)
        self.assertEqual("a", char_literal)

    def test_StringLiteral(self):
        string_literal = jast.StringLiteral("foo")
        self.assertIsInstance(string_literal, jast.StringLiteral)
        self.assertIsInstance(string_literal, str)
        self.assertEqual("foo", string_literal)

    def test_TextBlock(self):
        text_block = jast.TextBlock("foo")
        self.assertIsInstance(text_block, jast.TextBlock)
        self.assertIsInstance(text_block, str)
        self.assertEqual("foo", text_block)

    def test_NullLiteral(self):
        null_literal = jast.NullLiteral()
        self.assertIsInstance(null_literal, jast.NullLiteral)
        self.assertIsNone(null_literal.value)

    def test_Abstract(self):
        abstract = jast.Abstract()
        self.assertIsInstance(abstract, jast.Abstract)
        self.assertIsInstance(abstract, jast.JAST)

    def test_Default(self):
        default = jast.Default()
        self.assertIsInstance(default, jast.Default)
        self.assertIsInstance(default, jast.JAST)

    def test_Final(self):
        final = jast.Final()
        self.assertIsInstance(final, jast.Final)
        self.assertIsInstance(final, jast.JAST)

    def test_Native(self):
        native = jast.Native()
        self.assertIsInstance(native, jast.Native)
        self.assertIsInstance(native, jast.JAST)

    def test_Public(self):
        public = jast.Public()
        self.assertIsInstance(public, jast.Public)
        self.assertIsInstance(public, jast.JAST)

    def test_Protected(self):
        protected = jast.Protected()
        self.assertIsInstance(protected, jast.Protected)
        self.assertIsInstance(protected, jast.JAST)

    def test_Private(self):
        private = jast.Private()
        self.assertIsInstance(private, jast.Private)
        self.assertIsInstance(private, jast.JAST)

    def test_Static(self):
        static = jast.Static()
        self.assertIsInstance(static, jast.Static)
        self.assertIsInstance(static, jast.JAST)

    def test_Sealed(self):
        sealed = jast.Sealed()
        self.assertIsInstance(sealed, jast.Sealed)
        self.assertIsInstance(sealed, jast.JAST)

    def test_NonSealed(self):
        non_sealed = jast.NonSealed()
        self.assertIsInstance(non_sealed, jast.NonSealed)
        self.assertIsInstance(non_sealed, jast.JAST)

    def test_Strictfp(self):
        strictfp = jast.Strictfp()
        self.assertIsInstance(strictfp, jast.Strictfp)
        self.assertIsInstance(strictfp, jast.JAST)

    def test_Synchronized(self):
        synchronized = jast.Synchronized()
        self.assertIsInstance(synchronized, jast.Synchronized)
        self.assertIsInstance(synchronized, jast.JAST)

    def test_Transient(self):
        transient = jast.Transient()
        self.assertIsInstance(transient, jast.Transient)
        self.assertIsInstance(transient, jast.JAST)

    def test_Transitive(self):
        transitive = jast.Transitive()
        self.assertIsInstance(transitive, jast.Transitive)
        self.assertIsInstance(transitive, jast.JAST)
