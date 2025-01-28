import unittest
from typing import List

import jast


class TestConstructors(unittest.TestCase):
    def _test_iteration(self, tree):
        for field, value in tree:
            self.assertIsInstance(field, str)
            self.assertIsInstance(value, jast.JAST | List)
            self.assertTrue(hasattr(tree, field), f"{field} not in {tree.__class__}")
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

    def test_wildcardbound(self):
        wildcardbound = jast.wildcardbound(jast.Int(), extends=True)
        self.assertIsInstance(wildcardbound, jast.wildcardbound)
        self.assertIsInstance(wildcardbound, jast.JAST)
        self.assertIsInstance(wildcardbound.type, jast.Int)
        self.assertTrue(wildcardbound.extends)
        self.assertFalse(wildcardbound.super_)
        self._test_iteration(wildcardbound)

    def test_wildcardbound_error(self):
        self.assertRaises(ValueError, jast.wildcardbound, extends=True)
        self.assertRaises(ValueError, jast.wildcardbound, jast.Int())
        self.assertRaises(ValueError, jast.wildcardbound, jast.Int(), True, True)

    def test_Wildcard(self):
        wildcard = jast.Wildcard(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            bound=jast.wildcardbound(jast.Int(), extends=True),
        )
        self.assertIsInstance(wildcard, jast.Wildcard)
        self.assertIsInstance(wildcard, jast.JAST)
        self.assertEqual(1, len(wildcard.annotations))
        self.assertIsInstance(wildcard.annotations[0], jast.Annotation)
        self.assertIsInstance(wildcard.bound, jast.wildcardbound)
        self._test_iteration(wildcard)

    def test_typeargs(self):
        typeargs = jast.typeargs([jast.Int(), jast.Boolean()])
        self.assertIsInstance(typeargs, jast.typeargs)
        self.assertIsInstance(typeargs, jast.JAST)
        self.assertEqual(2, len(typeargs.types))
        self.assertIsInstance(typeargs.types[0], jast.Int)
        self.assertIsInstance(typeargs.types[1], jast.Boolean)
        self._test_iteration(typeargs)

    def test_typeargs_error(self):
        self.assertRaises(ValueError, jast.typeargs)

    def test_Coit(self):
        coit = jast.Coit(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("foo"),
            type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
        )
        self.assertIsInstance(coit, jast.Coit)
        self.assertIsInstance(coit, jast.JAST)
        self.assertEqual(1, len(coit.annotations))
        self.assertIsInstance(coit.annotations[0], jast.Annotation)
        self.assertIsInstance(coit.id, jast.identifier)
        self.assertEqual("foo", coit.id)
        self.assertIsInstance(coit.type_args, jast.typeargs)
        self._test_iteration(coit)

    def test_Coit_error(self):
        self.assertRaises(
            ValueError, jast.Coit, typeargs=jast.typeargs([jast.Int(), jast.Boolean()])
        )

    def test_ClassType(self):
        class_type = jast.ClassType(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            coits=[
                jast.Coit(
                    id=jast.identifier("foo"),
                    type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
                ),
                jast.Coit(
                    id=jast.identifier("bar"),
                ),
            ],
        )
        self.assertIsInstance(class_type, jast.ClassType)
        self.assertIsInstance(class_type, jast.JAST)
        self.assertEqual(1, len(class_type.annotations))
        self.assertIsInstance(class_type.annotations[0], jast.Annotation)
        self.assertEqual(2, len(class_type.coits))
        self.assertIsInstance(class_type.coits[0], jast.Coit)
        self.assertIsInstance(class_type.coits[1], jast.Coit)
        self._test_iteration(class_type)

    def test_ClassType_error(self):
        self.assertRaises(ValueError, jast.ClassType)
        self.assertRaises(ValueError, jast.ClassType, coits=[])

    def test_dim(self):
        dim = jast.dim(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))]
        )
        self.assertIsInstance(dim, jast.dim)
        self.assertIsInstance(dim, jast.JAST)
        self.assertEqual(1, len(dim.annotations))
        self._test_iteration(dim)

    def test_ArrayType(self):
        array_type = jast.ArrayType(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            type=jast.Int(),
            dims=[jast.dim(), jast.dim()],
        )
        self.assertIsInstance(array_type, jast.ArrayType)
        self.assertIsInstance(array_type, jast.JAST)
        self.assertEqual(1, len(array_type.annotations))
        self.assertIsInstance(array_type.annotations[0], jast.Annotation)
        self.assertIsInstance(array_type.type, jast.Int)
        self.assertEqual(2, len(array_type.dims))
        self.assertIsInstance(array_type.dims[0], jast.dim)
        self.assertIsInstance(array_type.dims[1], jast.dim)
        self._test_iteration(array_type)

    def test_ArrayType_error(self):
        self.assertRaises(
            ValueError,
            jast.ArrayType,
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            dims=[jast.dim()],
        )

    def test_variabledeclaratorid(self):
        variabledeclaratorid = jast.variabledeclaratorid(
            jast.identifier("foo"), [jast.dim(), jast.dim()]
        )
        self.assertIsInstance(variabledeclaratorid, jast.variabledeclaratorid)
        self.assertIsInstance(variabledeclaratorid, jast.JAST)
        self.assertEqual("foo", variabledeclaratorid.id)
        self.assertEqual(2, len(variabledeclaratorid.dims))
        self.assertIsInstance(variabledeclaratorid.dims[0], jast.dim)
        self.assertIsInstance(variabledeclaratorid.dims[1], jast.dim)
        self._test_iteration(variabledeclaratorid)

    def test_variabledeclaratorid_error(self):
        self.assertRaises(ValueError, jast.variabledeclaratorid, dims=[jast.dim()])

    def test_typebound(self):
        typebound = jast.typebound(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            types=[jast.Int(), jast.Boolean()],
        )
        self.assertIsInstance(typebound, jast.typebound)
        self.assertIsInstance(typebound, jast.JAST)
        self.assertEqual(1, len(typebound.annotations))
        self.assertIsInstance(typebound.annotations[0], jast.Annotation)
        self.assertEqual(2, len(typebound.types))
        self.assertIsInstance(typebound.types[0], jast.Int)
        self.assertIsInstance(typebound.types[1], jast.Boolean)
        self._test_iteration(typebound)

    def test_typebound_error(self):
        self.assertRaises(ValueError, jast.typebound, types=[])
        self.assertRaises(
            ValueError,
            jast.typebound,
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
        )

    def test_typeparam(self):
        typeparam = jast.typeparam(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("foo"),
            bound=jast.typebound(types=[jast.Int(), jast.Boolean()]),
        )
        self.assertIsInstance(typeparam, jast.typeparam)
        self.assertIsInstance(typeparam, jast.JAST)
        self.assertEqual(1, len(typeparam.annotations))
        self.assertIsInstance(typeparam.annotations[0], jast.Annotation)
        self.assertEqual("foo", typeparam.id)
        self.assertIsInstance(typeparam.bound, jast.typebound)
        self._test_iteration(typeparam)

    def test_typeparam_error(self):
        self.assertRaises(
            ValueError,
            jast.typeparam,
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            bound=jast.typebound(types=[jast.Int(), jast.Boolean()]),
        )

    def test_typeparams(self):
        typeparams = jast.typeparams(
            [
                jast.typeparam(id=jast.identifier("foo")),
                jast.typeparam(id=jast.identifier("bar")),
            ]
        )
        self.assertIsInstance(typeparams, jast.typeparams)
        self.assertIsInstance(typeparams, jast.JAST)
        self.assertEqual(2, len(typeparams.parameters))
        self.assertIsInstance(typeparams.parameters[0], jast.typeparam)
        self.assertIsInstance(typeparams.parameters[1], jast.typeparam)
        self._test_iteration(typeparams)

    def test_typeparams_error(self):
        self.assertRaises(ValueError, jast.typeparams, parameters=[])
        self.assertRaises(ValueError, jast.typeparams)

    def test_pattern(self):
        pattern = jast.pattern(
            modifiers=[jast.Final()],
            type=jast.Int(),
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
        )
        self.assertIsInstance(pattern, jast.pattern)
        self.assertIsInstance(pattern, jast.JAST)
        self.assertEqual(1, len(pattern.modifiers))
        self.assertIsInstance(pattern.modifiers[0], jast.Final)
        self.assertIsInstance(pattern.type, jast.Int)
        self.assertEqual(1, len(pattern.annotations))
        self.assertIsInstance(pattern.annotations[0], jast.Annotation)
        self.assertEqual("bar", pattern.id)
        self._test_iteration(pattern)

    def test_pattern_error(self):
        self.assertRaises(ValueError, jast.pattern, id=jast.identifier("bar"))
        self.assertRaises(ValueError, jast.pattern, type=jast.Int())

    def test_guardedpattern(self):
        guardedpattern = jast.guardedpattern(
            value=jast.pattern(
                type=jast.Int(),
                id=jast.identifier("bar"),
            ),
            conditions=[
                jast.Constant(jast.BoolLiteral(True)),
                jast.Constant(jast.IntLiteral(42)),
            ],
        )
        self.assertIsInstance(guardedpattern, jast.guardedpattern)
        self.assertIsInstance(guardedpattern, jast.JAST)
        self.assertIsInstance(guardedpattern.value, jast.pattern)
        self.assertEqual(2, len(guardedpattern.conditions))
        boolean = guardedpattern.conditions[0]
        self.assertIsInstance(boolean, jast.Constant)
        self.assertTrue(boolean.value.value)
        number = guardedpattern.conditions[1]
        self.assertIsInstance(number, jast.Constant)
        self.assertEqual(42, number.value)
        self._test_iteration(guardedpattern)

    def test_guardedpattern_error(self):
        self.assertRaises(
            ValueError,
            jast.guardedpattern,
            conditions=[jast.Constant(jast.BoolLiteral(True))],
        )

    def test_Or(self):
        or_ = jast.Or()
        self.assertIsInstance(or_, jast.Or)
        self.assertIsInstance(or_, jast.JAST)
        self._test_iteration(or_)

    def test_And(self):
        and_ = jast.And()
        self.assertIsInstance(and_, jast.And)
        self.assertIsInstance(and_, jast.JAST)
        self._test_iteration(and_)

    def test_BitOr(self):
        bit_or = jast.BitOr()
        self.assertIsInstance(bit_or, jast.BitOr)
        self.assertIsInstance(bit_or, jast.JAST)
        self._test_iteration(bit_or)

    def test_BitAnd(self):
        bit_and = jast.BitAnd()
        self.assertIsInstance(bit_and, jast.BitAnd)
        self.assertIsInstance(bit_and, jast.JAST)
        self._test_iteration(bit_and)

    def test_BitXor(self):
        bit_xor = jast.BitXor()
        self.assertIsInstance(bit_xor, jast.BitXor)
        self.assertIsInstance(bit_xor, jast.JAST)
        self._test_iteration(bit_xor)

    def test_Eq(self):
        equal = jast.Eq()
        self.assertIsInstance(equal, jast.Eq)
        self.assertIsInstance(equal, jast.JAST)
        self._test_iteration(equal)

    def test_NotEq(self):
        not_eq = jast.NotEq()
        self.assertIsInstance(not_eq, jast.NotEq)
        self.assertIsInstance(not_eq, jast.JAST)
        self._test_iteration(not_eq)

    def test_Lt(self):
        lt = jast.Lt()
        self.assertIsInstance(lt, jast.Lt)
        self.assertIsInstance(lt, jast.JAST)
        self._test_iteration(lt)

    def test_LtE(self):
        lte = jast.LtE()
        self.assertIsInstance(lte, jast.LtE)
        self.assertIsInstance(lte, jast.JAST)
        self._test_iteration(lte)

    def test_Gt(self):
        gt = jast.Gt()
        self.assertIsInstance(gt, jast.Gt)
        self.assertIsInstance(gt, jast.JAST)
        self._test_iteration(gt)

    def test_GtE(self):
        gte = jast.GtE()
        self.assertIsInstance(gte, jast.GtE)
        self.assertIsInstance(gte, jast.JAST)
        self._test_iteration(gte)

    def test_LShift(self):
        lshift = jast.LShift()
        self.assertIsInstance(lshift, jast.LShift)
        self.assertIsInstance(lshift, jast.JAST)
        self._test_iteration(lshift)

    def test_RShift(self):
        rshift = jast.RShift()
        self.assertIsInstance(rshift, jast.RShift)
        self.assertIsInstance(rshift, jast.JAST)
        self._test_iteration(rshift)

    def test_URShift(self):
        u_rshift = jast.URShift()
        self.assertIsInstance(u_rshift, jast.URShift)
        self.assertIsInstance(u_rshift, jast.JAST)
        self._test_iteration(u_rshift)

    def test_Add(self):
        add = jast.Add()
        self.assertIsInstance(add, jast.Add)
        self.assertIsInstance(add, jast.JAST)
        self._test_iteration(add)

    def test_Sub(self):
        sub = jast.Sub()
        self.assertIsInstance(sub, jast.Sub)
        self.assertIsInstance(sub, jast.JAST)
        self._test_iteration(sub)

    def test_Mult(self):
        mult = jast.Mult()
        self.assertIsInstance(mult, jast.Mult)
        self.assertIsInstance(mult, jast.JAST)
        self._test_iteration(mult)

    def test_Div(self):
        div = jast.Div()
        self.assertIsInstance(div, jast.Div)
        self.assertIsInstance(div, jast.JAST)
        self._test_iteration(div)

    def test_Mod(self):
        mod = jast.Mod()
        self.assertIsInstance(mod, jast.Mod)
        self.assertIsInstance(mod, jast.JAST)
        self._test_iteration(mod)

    def test_PreInc(self):
        pre_inc = jast.PreInc()
        self.assertIsInstance(pre_inc, jast.PreInc)
        self.assertIsInstance(pre_inc, jast.JAST)
        self._test_iteration(pre_inc)

    def test_PreDec(self):
        pre_dec = jast.PreDec()
        self.assertIsInstance(pre_dec, jast.PreDec)
        self.assertIsInstance(pre_dec, jast.JAST)
        self._test_iteration(pre_dec)

    def test_UAdd(self):
        u_add = jast.UAdd()
        self.assertIsInstance(u_add, jast.UAdd)
        self.assertIsInstance(u_add, jast.JAST)
        self._test_iteration(u_add)

    def test_USub(self):
        u_sub = jast.USub()
        self.assertIsInstance(u_sub, jast.USub)
        self.assertIsInstance(u_sub, jast.JAST)
        self._test_iteration(u_sub)

    def test_Invert(self):
        invert = jast.Invert()
        self.assertIsInstance(invert, jast.Invert)
        self.assertIsInstance(invert, jast.JAST)
        self._test_iteration(invert)

    def test_Not(self):
        not_ = jast.Not()
        self.assertIsInstance(not_, jast.Not)
        self.assertIsInstance(not_, jast.JAST)
        self._test_iteration(not_)

    def test_PostInc(self):
        post_inc = jast.PostInc()
        self.assertIsInstance(post_inc, jast.PostInc)
        self.assertIsInstance(post_inc, jast.JAST)
        self._test_iteration(post_inc)

    def test_PostDec(self):
        post_dec = jast.PostDec()
        self.assertIsInstance(post_dec, jast.PostDec)
        self.assertIsInstance(post_dec, jast.JAST)
        self._test_iteration(post_dec)

    def test_Lambda(self):
        lambda_ = jast.Lambda(
            args=[jast.identifier("foo"), jast.identifier("bar")],
            body=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(lambda_, jast.Lambda)
        self.assertIsInstance(lambda_, jast.JAST)
        self.assertEqual(2, len(lambda_.args))
        self.assertIsInstance(lambda_.args[0], jast.identifier)
        self.assertIsInstance(lambda_.args[1], jast.identifier)
        self.assertEqual("foo", lambda_.args[0])
        self.assertEqual("bar", lambda_.args[1])
        self.assertIsInstance(lambda_.body, jast.Constant)
        self.assertIsInstance(lambda_.body.value, jast.IntLiteral)
        self.assertEqual(42, lambda_.body.value)
        self._test_iteration(lambda_)

    def test_Lambda_error(self):
        self.assertRaises(
            ValueError, jast.Lambda, body=jast.Constant(jast.IntLiteral(42))
        )
        self.assertRaises(ValueError, jast.Lambda, args=[jast.identifier("foo")])
        self.assertRaises(
            ValueError,
            jast.Lambda,
            args=jast.params(jast.receiver(jast.Int())),
            body=jast.Constant(jast.IntLiteral(42)),
        ),

    def test_Assign(self):
        assign = jast.Assign(
            target=jast.identifier("foo"),
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(assign, jast.Assign)
        self.assertIsInstance(assign, jast.JAST)
        self.assertIsInstance(assign.target, jast.identifier)
        self.assertEqual("foo", assign.target)
        self.assertIsInstance(assign.value, jast.Constant)
        self.assertIsInstance(assign.value.value, jast.IntLiteral)
        self.assertEqual(42, assign.value.value)
        self.assertIsNone(assign.op)
        self._test_iteration(assign)

    def test_Assign_op(self):
        assign = jast.Assign(
            target=jast.identifier("foo"),
            value=jast.Constant(jast.IntLiteral(42)),
            op=jast.Add(),
        )
        self.assertIsInstance(assign, jast.Assign)
        self.assertIsInstance(assign, jast.JAST)
        self.assertIsInstance(assign.target, jast.identifier)
        self.assertEqual("foo", assign.target)
        self.assertIsInstance(assign.value, jast.Constant)
        self.assertIsInstance(assign.value.value, jast.IntLiteral)
        self.assertEqual(42, assign.value.value)
        self.assertIsInstance(assign.op, jast.Add)
        self._test_iteration(assign)

    def test_Assign_error(self):
        self.assertRaises(
            ValueError, jast.Assign, value=jast.Constant(jast.IntLiteral(42))
        )
        self.assertRaises(ValueError, jast.Assign, target=jast.identifier("foo"))

    def test_IfExp(self):
        if_exp = jast.IfExp(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Constant(jast.IntLiteral(42)),
            orelse=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertIsInstance(if_exp, jast.IfExp)
        self.assertIsInstance(if_exp, jast.JAST)
        self.assertIsInstance(if_exp.test, jast.Constant)
        self.assertIsInstance(if_exp.test.value, jast.BoolLiteral)
        self.assertTrue(if_exp.test.value)
        self.assertIsInstance(if_exp.body, jast.Constant)
        self.assertIsInstance(if_exp.body.value, jast.IntLiteral)
        self.assertEqual(42, if_exp.body.value)
        self.assertIsInstance(if_exp.orelse, jast.Constant)
        self.assertIsInstance(if_exp.orelse.value, jast.IntLiteral)
        self.assertEqual(0, if_exp.orelse.value)
        self._test_iteration(if_exp)

    def test_IfExp_error(self):
        self.assertRaises(
            ValueError,
            jast.IfExp,
            test=jast.Constant(
                jast.BoolLiteral(True), body=jast.Constant(jast.IntLiteral(42))
            ),
        )
        self.assertRaises(
            ValueError,
            jast.IfExp,
            test=jast.Constant(
                jast.BoolLiteral(True), orelse=jast.Constant(jast.IntLiteral(0))
            ),
        )
        self.assertRaises(
            ValueError,
            jast.IfExp,
            body=jast.Constant(
                jast.IntLiteral(42), orelse=jast.Constant(jast.IntLiteral(0))
            ),
        )

    def test_BinOp(self):
        bin_op = jast.BinOp(
            left=jast.Constant(jast.IntLiteral(42)),
            op=jast.Add(),
            right=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertIsInstance(bin_op, jast.BinOp)
        self.assertIsInstance(bin_op, jast.JAST)
        self.assertIsInstance(bin_op.left, jast.Constant)
        self.assertIsInstance(bin_op.left.value, jast.IntLiteral)
        self.assertEqual(42, bin_op.left.value)
        self.assertIsInstance(bin_op.op, jast.Add)
        self.assertIsInstance(bin_op.right, jast.Constant)
        self.assertIsInstance(bin_op.right.value, jast.IntLiteral)
        self.assertEqual(0, bin_op.right.value)
        self._test_iteration(bin_op)

    def test_BinOp_error(self):
        self.assertRaises(
            ValueError,
            jast.BinOp,
            op=jast.Add(),
            right=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertRaises(
            ValueError,
            jast.BinOp,
            left=jast.Constant(jast.IntLiteral(42)),
            op=jast.Add(),
        )
        self.assertRaises(
            ValueError,
            jast.BinOp,
            left=jast.Constant(jast.IntLiteral(42)),
            right=jast.Constant(jast.IntLiteral(0)),
        )

    def test_InstanceOf(self):
        instance_of = jast.InstanceOf(
            value=jast.identifier("foo"),
            type=jast.Int(),
        )
        self.assertIsInstance(instance_of, jast.InstanceOf)
        self.assertIsInstance(instance_of, jast.JAST)
        self.assertIsInstance(instance_of.value, jast.identifier)
        self.assertEqual("foo", instance_of.value)
        self.assertIsInstance(instance_of.type, jast.Int)
        self._test_iteration(instance_of)

    def test_InstanceOf_error(self):
        self.assertRaises(
            ValueError,
            jast.InstanceOf,
            type=jast.Int(),
        )
        self.assertRaises(
            ValueError,
            jast.InstanceOf,
            value=jast.identifier("foo"),
        )

    def test_UnaryOp(self):
        unary_op = jast.UnaryOp(
            op=jast.USub(),
            operand=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(unary_op, jast.UnaryOp)
        self.assertIsInstance(unary_op, jast.JAST)
        self.assertIsInstance(unary_op.op, jast.USub)
        self.assertIsInstance(unary_op.operand, jast.Constant)
        self.assertIsInstance(unary_op.operand.value, jast.IntLiteral)
        self.assertEqual(42, unary_op.operand.value)
        self._test_iteration(unary_op)

    def test_UnaryOp_error(self):
        self.assertRaises(
            ValueError,
            jast.UnaryOp,
            operand=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertRaises(
            ValueError,
            jast.UnaryOp,
            op=jast.USub(),
        )

    def test_PostOp(self):
        post_op = jast.PostOp(
            operand=jast.identifier("foo"),
            op=jast.PostInc(),
        )
        self.assertIsInstance(post_op, jast.PostOp)
        self.assertIsInstance(post_op, jast.JAST)
        self.assertIsInstance(post_op.operand, jast.identifier)
        self.assertEqual("foo", post_op.operand)
        self.assertIsInstance(post_op.op, jast.PostInc)
        self._test_iteration(post_op)

    def test_PostOp_error(self):
        self.assertRaises(
            ValueError,
            jast.PostOp,
            op=jast.PostInc(),
        )
        self.assertRaises(
            ValueError,
            jast.PostOp,
            operand=jast.identifier("foo"),
        )

    def test_Cast(self):
        cast = jast.Cast(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            type=jast.Int(),
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(cast, jast.Cast)
        self.assertIsInstance(cast, jast.JAST)
        self.assertEqual(1, len(cast.annotations))
        self.assertIsInstance(cast.annotations[0], jast.Annotation)
        self.assertIsInstance(cast.type, jast.Int)
        self.assertIsInstance(cast.value, jast.Constant)
        self.assertIsInstance(cast.value.value, jast.IntLiteral)
        self.assertEqual(42, cast.value.value)
        self._test_iteration(cast)

    def test_Cast_error(self):
        self.assertRaises(
            ValueError,
            jast.Cast,
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertRaises(
            ValueError,
            jast.Cast,
            type=jast.Int(),
        )

    def test_NewObject(self):
        new_object = jast.NewObject(
            type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
            type=jast.Coit(id=jast.identifier("A")),
            args=[jast.Constant(jast.IntLiteral(42))],
            body=[jast.EmptyDecl()],
        )
        self.assertIsInstance(new_object, jast.NewObject)
        self.assertIsInstance(new_object, jast.JAST)
        self.assertIsInstance(new_object.type_args, jast.typeargs)
        self.assertEqual(2, len(new_object.type_args.types))
        self.assertIsInstance(new_object.type_args.types[0], jast.Int)
        self.assertIsInstance(new_object.type_args.types[1], jast.Boolean)
        self.assertIsInstance(new_object.type, jast.Coit)
        self.assertEqual("A", new_object.type.id)
        self.assertEqual(1, len(new_object.args))
        self.assertIsInstance(new_object.args[0], jast.Constant)
        self.assertIsInstance(new_object.args[0].value, jast.IntLiteral)
        self.assertEqual(42, new_object.args[0].value)
        self.assertEqual(1, len(new_object.body))
        self.assertIsInstance(new_object.body[0], jast.EmptyDecl)
        self._test_iteration(new_object)

    def test_NewObject_error(self):
        self.assertRaises(
            ValueError,
            jast.NewObject,
            type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
            args=[jast.Constant(jast.IntLiteral(42))],
            body=[jast.EmptyDecl()],
        )

    def test_NewArray(self):
        new_array = jast.NewArray(
            type=jast.Int(),
            expr_dims=[jast.Constant(jast.IntLiteral(1))],
            dims=[jast.dim(), jast.dim()],
        )
        self.assertIsInstance(new_array, jast.NewArray)
        self.assertIsInstance(new_array, jast.JAST)
        self.assertIsInstance(new_array.type, jast.Int)
        self.assertEqual(1, len(new_array.expr_dims))
        expr_dim = new_array.expr_dims[0]
        self.assertIsInstance(expr_dim, jast.Constant)
        self.assertIsInstance(expr_dim.value, jast.IntLiteral)
        self.assertEqual(1, expr_dim.value)
        self.assertEqual(2, len(new_array.dims))
        self.assertIsInstance(new_array.dims[0], jast.dim)
        self.assertIsInstance(new_array.dims[1], jast.dim)
        self._test_iteration(new_array)

    def test_NewArray_initializer(self):
        new_array = jast.NewArray(
            type=jast.Int(),
            dims=[jast.dim()],
            initializer=jast.arrayinit(values=[jast.Constant(jast.IntLiteral(1))]),
        )
        self.assertIsInstance(new_array, jast.NewArray)
        self.assertIsInstance(new_array, jast.JAST)
        self.assertIsInstance(new_array.type, jast.Int)
        self.assertEqual(1, len(new_array.dims))
        self.assertIsInstance(new_array.dims[0], jast.dim)
        self.assertIsInstance(new_array.initializer, jast.arrayinit)
        self.assertEqual(1, len(new_array.initializer.values))
        self.assertIsInstance(new_array.initializer.values[0], jast.Constant)
        self.assertIsInstance(new_array.initializer.values[0].value, jast.IntLiteral)
        self.assertEqual(1, new_array.initializer.values[0].value)
        self._test_iteration(new_array)

    def test_NewArray_error(self):
        self.assertRaises(
            ValueError,
            jast.NewArray,
            dims=[jast.dim()],
        )
        self.assertRaises(
            ValueError,
            jast.NewArray,
            type=jast.Int(),
            expr_dims=[jast.Constant(jast.IntLiteral(1))],
            initializer=jast.arrayinit(values=[jast.Constant(jast.IntLiteral(1))]),
        )

    def test_ExpCase(self):
        exp_case = jast.ExpCase()
        self.assertIsInstance(exp_case, jast.ExpCase)
        self.assertIsInstance(exp_case, jast.JAST)
        self._test_iteration(exp_case)

    def test_ExpDefault(self):
        exp_default = jast.ExpDefault()
        self.assertIsInstance(exp_default, jast.ExpDefault)
        self.assertIsInstance(exp_default, jast.JAST)
        self._test_iteration(exp_default)

    def test_switchexprule(self):
        switchexprule = jast.switchexprule(
            label=jast.ExpCase(),
            cases=[jast.Constant(jast.IntLiteral(42))],
            arrow=True,
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )
        self.assertIsInstance(switchexprule, jast.switchexprule)
        self.assertIsInstance(switchexprule, jast.JAST)
        self.assertIsInstance(switchexprule.label, jast.ExpCase)
        self.assertEqual(1, len(switchexprule.cases))
        self.assertIsInstance(switchexprule.cases[0], jast.Constant)
        self.assertIsInstance(switchexprule.cases[0].value, jast.IntLiteral)
        self.assertEqual(42, switchexprule.cases[0].value)
        self.assertTrue(switchexprule.arrow)
        self.assertEqual(1, len(switchexprule.body))
        ret = switchexprule.body[0]
        self.assertIsInstance(ret, jast.Return)
        self.assertIsInstance(ret.value, jast.Constant)
        self.assertIsInstance(ret.value.value, jast.IntLiteral)
        self.assertEqual(24, ret.value.value)
        self._test_iteration(switchexprule)

    def test_switchexprule_default(self):
        switchexprule = jast.switchexprule(
            label=jast.ExpDefault(),
            body=[jast.Empty()],
        )
        self.assertIsInstance(switchexprule, jast.switchexprule)
        self.assertIsInstance(switchexprule, jast.JAST)
        self.assertIsInstance(switchexprule.label, jast.ExpDefault)
        self.assertIsNone(switchexprule.cases)
        self.assertFalse(switchexprule.arrow)
        self.assertEqual(1, len(switchexprule.body))
        self.assertIsInstance(switchexprule.body[0], jast.Empty)
        self._test_iteration(switchexprule)

    def test_switchexprule_error(self):
        self.assertRaises(
            ValueError,
            jast.switchexprule,
            cases=[jast.Constant(jast.IntLiteral(42))],
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )
        self.assertRaises(
            ValueError,
            jast.switchexprule,
            label=jast.ExpCase(),
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )

    def test_SwitchExp(self):
        switch_exp = jast.SwitchExp(
            value=jast.identifier("foo"),
            rules=[
                jast.switchexprule(
                    label=jast.ExpCase(),
                    cases=[jast.Constant(jast.IntLiteral(42))],
                    arrow=True,
                    body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
                )
            ],
        )
        self.assertIsInstance(switch_exp, jast.SwitchExp)
        self.assertIsInstance(switch_exp, jast.JAST)
        self.assertIsInstance(switch_exp.value, jast.identifier)
        self.assertEqual("foo", switch_exp.value)
        self.assertEqual(1, len(switch_exp.rules))
        self.assertIsInstance(switch_exp.rules[0], jast.switchexprule)
        self._test_iteration(switch_exp)

    def test_SwitchExp_error(self):
        self.assertRaises(
            ValueError,
            jast.SwitchExp,
            rules=[
                jast.switchexprule(
                    label=jast.ExpCase(),
                    cases=[jast.Constant(jast.IntLiteral(42))],
                    arrow=True,
                    body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
                )
            ],
        )
