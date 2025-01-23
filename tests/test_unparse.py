import unittest

import jast


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
        self.assertEqual("extends int", jast.unparse(tree))

    def test_wildcardbound_super(self):
        tree = jast.wildcardbound(jast.Int(), super_=True)
        self.assertEqual("super int", jast.unparse(tree))

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
