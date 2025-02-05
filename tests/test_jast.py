from typing import List

import jast
from jast import JASTError
from utils import BaseTest


class TestJAST(BaseTest):
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
        self._test_identifier(qname.identifiers[0], "foo")
        self._test_identifier(qname.identifiers[1], "bar")
        self._test_iteration(qname)

    def test_qname_error(self):
        self.assertRaises(JASTError, jast.qname, [])
        self.assertRaises(JASTError, jast.qname)

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
        text_block = jast.TextBlock(["foo"])
        self.assertIsInstance(text_block, jast.TextBlock)
        self.assertEqual(["foo"], text_block.value)
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
        self._test_identifier(elementvaluepair.id, "foo")
        self._test_int_constant(elementvaluepair.value, 42)
        self._test_iteration(elementvaluepair)

    def test_elementvaluepair_error(self):
        self.assertRaises(JASTError, jast.elementvaluepair, jast.identifier("foo"))
        self.assertRaises(
            JASTError, jast.elementvaluepair, value=jast.Constant(jast.IntLiteral(42))
        )

    def test_elementarrayinit(self):
        elementarrayinit = jast.elementarrayinit([jast.Constant(jast.IntLiteral(42))])
        self.assertIsInstance(elementarrayinit, jast.elementarrayinit)
        self.assertIsInstance(elementarrayinit, jast.JAST)
        self.assertEqual(1, len(elementarrayinit.values))
        self._test_int_constant(elementarrayinit.values[0], 42)
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
        self._test_identifier(annotation.name.identifiers[0], "foo")
        self._test_int_constant(annotation.elements[0].value, 42)
        self._test_iteration(annotation)

    def test_Annotation_error(self):
        self.assertRaises(
            JASTError,
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
        self.assertRaises(JASTError, jast.wildcardbound, extends=True)
        self.assertRaises(JASTError, jast.wildcardbound, jast.Int())
        self.assertRaises(JASTError, jast.wildcardbound, jast.Int(), True, True)

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
        self.assertRaises(JASTError, jast.typeargs)

    def test_Coit(self):
        coit = jast.Coit(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
            type_args=jast.typeargs([jast.Int(), jast.Boolean()]),
        )
        self.assertIsInstance(coit, jast.Coit)
        self.assertIsInstance(coit, jast.JAST)
        self.assertEqual(1, len(coit.annotations))
        self.assertIsInstance(coit.annotations[0], jast.Annotation)
        self._test_identifier(coit.id, "bar")
        self.assertIsInstance(coit.type_args, jast.typeargs)
        self._test_iteration(coit)

    def test_Coit_error(self):
        self.assertRaises(
            JASTError, jast.Coit, typeargs=jast.typeargs([jast.Int(), jast.Boolean()])
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
        self.assertRaises(JASTError, jast.ClassType)
        self.assertRaises(JASTError, jast.ClassType, coits=[])

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
            JASTError,
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
        self._test_identifier(variabledeclaratorid.id, "foo")
        self.assertEqual(2, len(variabledeclaratorid.dims))
        self.assertIsInstance(variabledeclaratorid.dims[0], jast.dim)
        self.assertIsInstance(variabledeclaratorid.dims[1], jast.dim)
        self._test_iteration(variabledeclaratorid)

    def test_variabledeclaratorid_error(self):
        self.assertRaises(JASTError, jast.variabledeclaratorid, dims=[jast.dim()])

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
        self.assertRaises(JASTError, jast.typebound, types=[])
        self.assertRaises(
            JASTError,
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
        self._test_identifier(typeparam.id, "foo")
        self.assertIsInstance(typeparam.bound, jast.typebound)
        self._test_iteration(typeparam)

    def test_typeparam_error(self):
        self.assertRaises(
            JASTError,
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
        self.assertRaises(JASTError, jast.typeparams, parameters=[])
        self.assertRaises(JASTError, jast.typeparams)

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
        self._test_identifier(pattern.id, "bar")
        self._test_iteration(pattern)

    def test_pattern_error(self):
        self.assertRaises(JASTError, jast.pattern, id=jast.identifier("bar"))
        self.assertRaises(JASTError, jast.pattern, type=jast.Int())

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
        self._test_int_constant(guardedpattern.conditions[1], 42)
        self._test_iteration(guardedpattern)

    def test_guardedpattern_error(self):
        self.assertRaises(
            JASTError,
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
        self._test_identifier(lambda_.args[0], "foo")
        self._test_identifier(lambda_.args[1], "bar")
        self._test_int_constant(lambda_.body, 42)
        self._test_iteration(lambda_)

    def test_Lambda_error(self):
        self.assertRaises(
            JASTError, jast.Lambda, body=jast.Constant(jast.IntLiteral(42))
        )
        self.assertRaises(JASTError, jast.Lambda, args=[jast.identifier("foo")])
        self.assertRaises(
            JASTError,
            jast.Lambda,
            args=jast.params(jast.receiver(jast.Int())),
            body=jast.Constant(jast.IntLiteral(42)),
        ),

    def test_Assign(self):
        assign = jast.Assign(
            target=jast.Name(jast.identifier("foo")),
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(assign, jast.Assign)
        self.assertIsInstance(assign, jast.JAST)
        self._test_name(assign.target, "foo")
        self._test_int_constant(assign.value, 42)
        self.assertIsNone(assign.op)
        self._test_iteration(assign)

    def test_Assign_op(self):
        assign = jast.Assign(
            target=jast.Name(jast.identifier("foo")),
            value=jast.Constant(jast.IntLiteral(42)),
            op=jast.Add(),
        )
        self.assertIsInstance(assign, jast.Assign)
        self.assertIsInstance(assign, jast.JAST)
        self._test_name(assign.target, "foo")
        self._test_int_constant(assign.value, 42)
        self.assertIsInstance(assign.op, jast.Add)
        self._test_iteration(assign)

    def test_Assign_error(self):
        self.assertRaises(
            JASTError, jast.Assign, value=jast.Constant(jast.IntLiteral(42))
        )
        self.assertRaises(JASTError, jast.Assign, target=jast.identifier("foo"))

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
        self._test_int_constant(if_exp.body, 42)
        self._test_int_constant(if_exp.orelse, 0)
        self._test_iteration(if_exp)

    def test_IfExp_error(self):
        self.assertRaises(
            JASTError,
            jast.IfExp,
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertRaises(
            JASTError,
            jast.IfExp,
            test=jast.Constant(jast.BoolLiteral(True)),
            orelse=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertRaises(
            JASTError,
            jast.IfExp,
            body=jast.Constant(jast.IntLiteral(42)),
            orelse=jast.Constant(jast.IntLiteral(0)),
        )

    def test_BinOp(self):
        bin_op = jast.BinOp(
            left=jast.Constant(jast.IntLiteral(42)),
            op=jast.Add(),
            right=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertIsInstance(bin_op, jast.BinOp)
        self.assertIsInstance(bin_op, jast.JAST)
        self._test_int_constant(bin_op.left, 42)
        self.assertIsInstance(bin_op.op, jast.Add)
        self._test_int_constant(bin_op.right, 0)
        self._test_iteration(bin_op)

    def test_BinOp_error(self):
        self.assertRaises(
            JASTError,
            jast.BinOp,
            op=jast.Add(),
            right=jast.Constant(jast.IntLiteral(0)),
        )
        self.assertRaises(
            JASTError,
            jast.BinOp,
            left=jast.Constant(jast.IntLiteral(42)),
            op=jast.Add(),
        )
        self.assertRaises(
            JASTError,
            jast.BinOp,
            left=jast.Constant(jast.IntLiteral(42)),
            right=jast.Constant(jast.IntLiteral(0)),
        )

    def test_InstanceOf(self):
        instance_of = jast.InstanceOf(
            value=jast.Name(jast.identifier("foo")),
            type=jast.Int(),
        )
        self.assertIsInstance(instance_of, jast.InstanceOf)
        self.assertIsInstance(instance_of, jast.JAST)
        self._test_name(instance_of.value, "foo")
        self.assertIsInstance(instance_of.type, jast.Int)
        self._test_iteration(instance_of)

    def test_InstanceOf_error(self):
        self.assertRaises(
            JASTError,
            jast.InstanceOf,
            type=jast.Int(),
        )
        self.assertRaises(
            JASTError,
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
        self._test_int_constant(unary_op.operand, 42)
        self._test_iteration(unary_op)

    def test_UnaryOp_error(self):
        self.assertRaises(
            JASTError,
            jast.UnaryOp,
            operand=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertRaises(
            JASTError,
            jast.UnaryOp,
            op=jast.USub(),
        )

    def test_PostOp(self):
        post_op = jast.PostOp(
            operand=jast.Name(jast.identifier("foo")),
            op=jast.PostInc(),
        )
        self.assertIsInstance(post_op, jast.PostOp)
        self.assertIsInstance(post_op, jast.JAST)
        self._test_name(post_op.operand, "foo")
        self.assertIsInstance(post_op.op, jast.PostInc)
        self._test_iteration(post_op)

    def test_PostOp_error(self):
        self.assertRaises(
            JASTError,
            jast.PostOp,
            op=jast.PostInc(),
        )
        self.assertRaises(
            JASTError,
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
        self._test_int_constant(cast.value, 42)
        self._test_iteration(cast)

    def test_Cast_error(self):
        self.assertRaises(
            JASTError,
            jast.Cast,
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertRaises(
            JASTError,
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
        self._test_identifier(new_object.type.id, "A")
        self.assertEqual(1, len(new_object.args))
        self._test_int_constant(new_object.args[0], 42)
        self.assertEqual(1, len(new_object.body))
        self.assertIsInstance(new_object.body[0], jast.EmptyDecl)
        self._test_iteration(new_object)

    def test_NewObject_error(self):
        self.assertRaises(
            JASTError,
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
        self._test_int_constant(new_array.expr_dims[0], 1)
        self.assertEqual(2, len(new_array.dims))
        self.assertIsInstance(new_array.dims[0], jast.dim)
        self.assertIsInstance(new_array.dims[1], jast.dim)
        self._test_iteration(new_array)

    def test_NewArray_initializer(self):
        new_array = jast.NewArray(
            type=jast.Int(),
            dims=[jast.dim()],
            init=jast.arrayinit(values=[jast.Constant(jast.IntLiteral(1))]),
        )
        self.assertIsInstance(new_array, jast.NewArray)
        self.assertIsInstance(new_array, jast.JAST)
        self.assertIsInstance(new_array.type, jast.Int)
        self.assertEqual(1, len(new_array.dims))
        self.assertIsInstance(new_array.dims[0], jast.dim)
        self.assertIsInstance(new_array.init, jast.arrayinit)
        self.assertEqual(1, len(new_array.init.values))
        self._test_int_constant(new_array.init.values[0], 1)
        self._test_iteration(new_array)

    def test_NewArray_error(self):
        self.assertRaises(
            JASTError,
            jast.NewArray,
            dims=[jast.dim()],
        )
        self.assertRaises(
            JASTError,
            jast.NewArray,
            type=jast.Int(),
            expr_dims=[jast.Constant(jast.IntLiteral(1))],
            init=jast.arrayinit(values=[jast.Constant(jast.IntLiteral(1))]),
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
        self._test_int_constant(switchexprule.cases[0], 42)
        self.assertTrue(switchexprule.arrow)
        self.assertEqual(1, len(switchexprule.body))
        self.assertIsInstance(switchexprule.body[0], jast.Return)
        self._test_int_constant(switchexprule.body[0].value, 24)
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
            JASTError,
            jast.switchexprule,
            cases=[jast.Constant(jast.IntLiteral(42))],
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )
        self.assertRaises(
            JASTError,
            jast.switchexprule,
            label=jast.ExpCase(),
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )
        self.assertRaises(
            JASTError,
            jast.switchexprule,
            label=jast.ExpDefault(),
            cases=[jast.Constant(jast.IntLiteral(42))],
            body=[jast.Return(jast.Constant(jast.IntLiteral(24)))],
        )

    def test_SwitchExp(self):
        switch_exp = jast.SwitchExp(
            value=jast.Name(jast.identifier("foo")),
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
        self._test_name(switch_exp.value, "foo")
        self.assertEqual(1, len(switch_exp.rules))
        self.assertIsInstance(switch_exp.rules[0], jast.switchexprule)
        self._test_iteration(switch_exp)

    def test_SwitchExp_error(self):
        self.assertRaises(
            JASTError,
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

    def test_This(self):
        this = jast.This()
        self.assertIsInstance(this, jast.This)
        self.assertIsInstance(this, jast.JAST)
        self._test_iteration(this)

    def test_Super(self):
        super_ = jast.Super(
            type_args=jast.typeargs(types=[jast.Int()]),
            id=jast.identifier("foo"),
        )
        self.assertIsInstance(super_, jast.Super)
        self.assertIsInstance(super_, jast.JAST)
        self.assertIsInstance(super_.type_args, jast.typeargs)
        self.assertEqual(1, len(super_.type_args.types))
        self.assertIsInstance(super_.type_args.types[0], jast.Int)
        self._test_identifier(super_.id, "foo")
        self._test_iteration(super_)

    def test_Constant(self):
        constant = jast.Constant(jast.IntLiteral(42))
        self.assertIsInstance(constant, jast.JAST)
        self._test_int_constant(constant, 42)
        self._test_iteration(constant)

    def test_Constant_error(self):
        self.assertRaises(JASTError, jast.Constant)

    def test_Name(self):
        name = jast.Name(jast.identifier("foo"))
        self.assertIsInstance(name, jast.JAST)
        self._test_name(name, "foo")
        self._test_iteration(name)

    def test_Name_error(self):
        self.assertRaises(JASTError, jast.Name)

    def test_ClassExpr(self):
        class_expr = jast.ClassExpr(type=jast.Int())
        self.assertIsInstance(class_expr, jast.ClassExpr)
        self.assertIsInstance(class_expr, jast.JAST)
        self.assertIsInstance(class_expr.type, jast.Int)
        self._test_iteration(class_expr)

    def test_ClassExpr_error(self):
        self.assertRaises(JASTError, jast.ClassExpr)

    def test_ExplicitGenericInvocation(self):
        explicit_generic_invocation = jast.ExplicitGenericInvocation(
            type_args=jast.typeargs(types=[jast.Int()]),
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(
            explicit_generic_invocation, jast.ExplicitGenericInvocation
        )
        self.assertIsInstance(explicit_generic_invocation, jast.JAST)
        self.assertIsInstance(explicit_generic_invocation.type_args, jast.typeargs)
        self.assertEqual(1, len(explicit_generic_invocation.type_args.types))
        self.assertIsInstance(explicit_generic_invocation.type_args.types[0], jast.Int)
        self._test_int_constant(explicit_generic_invocation.value, 42)
        self._test_iteration(explicit_generic_invocation)

    def test_ExplicitGenericInvocation_error(self):
        self.assertRaises(
            JASTError,
            jast.ExplicitGenericInvocation,
            type_args=jast.typeargs(types=[jast.Int()]),
        )
        self.assertRaises(
            JASTError,
            jast.ExplicitGenericInvocation,
            value=jast.Constant(jast.IntLiteral(42)),
        )

    def test_Subscript(self):
        subscript = jast.Subscript(
            value=jast.Name(jast.identifier("foo")),
            index=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(subscript, jast.Subscript)
        self.assertIsInstance(subscript, jast.JAST)
        self._test_name(subscript.value, "foo")
        self._test_int_constant(subscript.index, 42)
        self._test_iteration(subscript)

    def test_Subscript_error(self):
        self.assertRaises(
            JASTError,
            jast.Subscript,
            value=jast.Name(jast.identifier("foo")),
        )
        self.assertRaises(
            JASTError,
            jast.Subscript,
            index=jast.Constant(jast.IntLiteral(42)),
        )

    def test_Member(self):
        member = jast.Member(
            value=jast.Name(jast.identifier("foo")),
            member=jast.Name(jast.identifier("bar")),
        )
        self.assertIsInstance(member, jast.Member)
        self.assertIsInstance(member, jast.JAST)
        self._test_name(member.value, "foo")
        self._test_name(member.member, "bar")
        self._test_iteration(member)

    def test_Member_error(self):
        self.assertRaises(
            JASTError,
            jast.Member,
            member=jast.Name(jast.identifier("bar")),
        )
        self.assertRaises(
            JASTError,
            jast.Member,
            value=jast.Name(jast.identifier("foo")),
        )

    def test_Call(self):
        call = jast.Call(
            func=jast.Name(jast.identifier("foo")),
            args=[jast.Constant(jast.IntLiteral(42))],
        )
        self.assertIsInstance(call, jast.Call)
        self.assertIsInstance(call, jast.JAST)
        self._test_name(call.func, "foo")
        self.assertEqual(1, len(call.args))
        self._test_int_constant(call.args[0], 42)
        self._test_iteration(call)

    def test_Call_error(self):
        self.assertRaises(
            JASTError,
            jast.Call,
            args=[jast.Constant(jast.IntLiteral(42))],
        )

    def test_Reference(self):
        reference = jast.Reference(
            type=jast.Name(jast.identifier("foo")),
            type_args=jast.typeargs(types=[jast.Int()]),
            id=jast.identifier("bar"),
        )
        self.assertIsInstance(reference, jast.Reference)
        self.assertIsInstance(reference, jast.JAST)
        self._test_name(reference.type, "foo")
        self.assertIsInstance(reference.type_args, jast.typeargs)
        self.assertEqual(1, len(reference.type_args.types))
        self.assertIsInstance(reference.type_args.types[0], jast.Int)
        self._test_identifier(reference.id, "bar")
        self.assertFalse(reference.new)
        self._test_iteration(reference)

    def test_Reference_new(self):
        reference = jast.Reference(
            type=jast.Name(jast.identifier("foo")),
            type_args=jast.typeargs(types=[jast.Int()]),
            new=True,
        )
        self.assertIsInstance(reference, jast.Reference)
        self.assertIsInstance(reference, jast.JAST)
        self._test_name(reference.type, "foo")
        self.assertIsInstance(reference.type_args, jast.typeargs)
        self.assertEqual(1, len(reference.type_args.types))
        self.assertIsInstance(reference.type_args.types[0], jast.Int)
        self.assertIsNone(reference.id)
        self.assertTrue(reference.new)
        self._test_iteration(reference)

    def test_Reference_error(self):
        self.assertRaises(
            JASTError,
            jast.Reference,
            type=jast.Name(jast.identifier("foo")),
            type_args=jast.typeargs(types=[jast.Int()]),
        )
        self.assertRaises(
            JASTError,
            jast.Reference,
            type=jast.Name(jast.identifier("foo")),
            id=jast.identifier("bar"),
            new=True,
        )
        self.assertRaises(
            JASTError,
            jast.Reference,
            new=True,
        )

    def test_arrayinit(self):
        arrayinit = jast.arrayinit(values=[jast.Constant(jast.IntLiteral(42))])
        self.assertIsInstance(arrayinit, jast.arrayinit)
        self.assertIsInstance(arrayinit, jast.JAST)
        self.assertEqual(1, len(arrayinit.values))
        self._test_int_constant(arrayinit.values[0], 42)
        self._test_iteration(arrayinit)

    def test_receiver(self):
        receiver = jast.receiver(type=jast.Int(), identifiers=[jast.identifier("foo")])
        self.assertIsInstance(receiver, jast.receiver)
        self.assertIsInstance(receiver, jast.JAST)
        self.assertIsInstance(receiver.type, jast.Int)
        self.assertEqual(1, len(receiver.identifiers))
        self._test_identifier(receiver.identifiers[0], "foo")
        self._test_iteration(receiver)

    def test_receiver_error(self):
        self.assertRaises(
            JASTError, jast.receiver, identifiers=[jast.identifier("foo")]
        )

    def test_param(self):
        param = jast.param(
            modifiers=[jast.Final()],
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("bar")),
        )
        self.assertIsInstance(param, jast.param)
        self.assertIsInstance(param, jast.JAST)
        self.assertEqual(1, len(param.modifiers))
        self.assertIsInstance(param.modifiers[0], jast.Final)
        self.assertIsInstance(param.type, jast.Int)
        self.assertIsInstance(param.id, jast.variabledeclaratorid)
        self._test_identifier(param.id.id, "bar")
        self.assertEqual(0, len(param.id.dims))
        self._test_iteration(param)

    def test_param_error(self):
        self.assertRaises(
            JASTError, jast.param, id=jast.variabledeclaratorid(jast.identifier("bar"))
        )
        self.assertRaises(JASTError, jast.param, type=jast.Int())

    def test_arity(self):
        arity = jast.arity(
            modifiers=[jast.Final()],
            type=jast.Int(),
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.variabledeclaratorid(jast.identifier("bar")),
        )
        self.assertIsInstance(arity, jast.arity)
        self.assertIsInstance(arity, jast.JAST)
        self.assertEqual(1, len(arity.modifiers))
        self.assertIsInstance(arity.modifiers[0], jast.Final)
        self.assertIsInstance(arity.type, jast.Int)
        self.assertEqual(1, len(arity.annotations))
        self.assertIsInstance(arity.annotations[0], jast.Annotation)
        self.assertIsInstance(arity.id, jast.variabledeclaratorid)
        self._test_identifier(arity.id.id, "bar")
        self.assertEqual(0, len(arity.id.dims))
        self._test_iteration(arity)

    def test_arity_error(self):
        self.assertRaises(JASTError, jast.arity, id=jast.identifier("bar"))
        self.assertRaises(JASTError, jast.arity, type=jast.Int())

    def test_params(self):
        params = jast.params(
            receiver_param=jast.receiver(jast.Int()),
            parameters=[
                jast.param(
                    modifiers=[jast.Final()],
                    type=jast.Int(),
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                ),
                jast.param(
                    modifiers=[jast.Final()],
                    type=jast.Int(),
                    id=jast.variabledeclaratorid(jast.identifier("bar")),
                ),
            ],
        )
        self.assertIsInstance(params, jast.params)
        self.assertIsInstance(params, jast.JAST)
        self.assertIsInstance(params.receiver_param, jast.receiver)
        self.assertEqual(2, len(params.parameters))
        self.assertIsInstance(params.parameters[0], jast.param)
        self.assertIsInstance(params.parameters[1], jast.param)
        self._test_iteration(params)

    def test_Empty(self):
        empty = jast.Empty()
        self.assertIsInstance(empty, jast.Empty)
        self.assertIsInstance(empty, jast.JAST)
        self._test_iteration(empty)

    def test_Block(self):
        block = jast.Block(body=[jast.Empty(), jast.Empty()])
        self.assertIsInstance(block, jast.Block)
        self.assertIsInstance(block, jast.JAST)
        self.assertEqual(2, len(block.body))
        self.assertIsInstance(block.body[0], jast.Empty)
        self.assertIsInstance(block.body[1], jast.Empty)
        self._test_iteration(block)

    def test_Compound(self):
        compound = jast.Compound(body=[jast.Empty(), jast.Empty()])
        self.assertIsInstance(compound, jast.Compound)
        self.assertIsInstance(compound, jast.JAST)
        self.assertEqual(2, len(compound.body))
        self.assertIsInstance(compound.body[0], jast.Empty)
        self.assertIsInstance(compound.body[1], jast.Empty)
        self._test_iteration(compound)

    def test_LocalType_class(self):
        local_class = jast.LocalType(
            decl=jast.Class(
                id=jast.identifier("A"),
                body=[jast.EmptyDecl()],
            )
        )
        self.assertIsInstance(local_class, jast.LocalType)
        self.assertIsInstance(local_class, jast.JAST)
        self.assertIsInstance(local_class.decl, jast.Class)
        self._test_iteration(local_class)

    def test_LocalType_interface(self):
        local_interface = jast.LocalType(
            decl=jast.Interface(
                id=jast.identifier("A"),
                body=[jast.EmptyDecl()],
            )
        )
        self.assertIsInstance(local_interface, jast.LocalType)
        self.assertIsInstance(local_interface, jast.JAST)
        self.assertIsInstance(local_interface.decl, jast.Interface)
        self._test_iteration(local_interface)

    def test_LocalType_record(self):
        local_record = jast.LocalType(
            decl=jast.Record(
                id=jast.identifier("A"),
                body=[jast.EmptyDecl()],
            )
        )
        self.assertIsInstance(local_record, jast.LocalType)
        self.assertIsInstance(local_record, jast.JAST)
        self.assertIsInstance(local_record.decl, jast.Record)
        self._test_iteration(local_record)

    def test_LocalType_error(self):
        self.assertRaises(JASTError, jast.LocalType)

    def test_LocalVariable(self):
        local_variable = jast.LocalVariable(
            modifiers=[jast.Final()],
            type=jast.Int(),
            declarators=[
                jast.declarator(
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                    value=jast.Constant(jast.IntLiteral(42)),
                ),
                jast.declarator(id=jast.variabledeclaratorid(jast.identifier("bar"))),
            ],
        )
        self.assertIsInstance(local_variable, jast.LocalVariable)
        self.assertIsInstance(local_variable, jast.JAST)
        self.assertEqual(1, len(local_variable.modifiers))
        self.assertIsInstance(local_variable.modifiers[0], jast.Final)
        self.assertIsInstance(local_variable.type, jast.Int)
        self.assertEqual(2, len(local_variable.declarators))
        self.assertIsInstance(local_variable.declarators[0], jast.declarator)
        self.assertIsInstance(local_variable.declarators[1], jast.declarator)
        self._test_iteration(local_variable)

    def test_LocalVariable_error(self):
        self.assertRaises(
            JASTError,
            jast.LocalVariable,
            declarators=[
                jast.declarator(
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                    value=jast.Constant(jast.IntLiteral(42)),
                )
            ],
        )
        self.assertRaises(JASTError, jast.LocalVariable, type=jast.Int())
        self.assertRaises(
            JASTError, jast.LocalVariable, type=jast.Int(), declarators=[]
        )

    def test_Labeled(self):
        labeled = jast.Labeled(
            label=jast.identifier("foo"),
            body=jast.Empty(),
        )
        self.assertIsInstance(labeled, jast.Labeled)
        self.assertIsInstance(labeled, jast.JAST)
        self._test_identifier(labeled.label, "foo")
        self.assertIsInstance(labeled.body, jast.Empty)
        self._test_iteration(labeled)

    def test_Labeled_error(self):
        self.assertRaises(JASTError, jast.Labeled, body=jast.Empty())
        self.assertRaises(JASTError, jast.Labeled, label=jast.identifier("foo"))

    def test_Expression(self):
        expression = jast.Expression(
            value=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(expression, jast.Expression)
        self.assertIsInstance(expression, jast.JAST)
        self._test_int_constant(expression.value, 42)
        self._test_iteration(expression)

    def test_Expression_error(self):
        self.assertRaises(JASTError, jast.Expression)

    def test_If(self):
        if_ = jast.If(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Empty(),
            orelse=jast.Empty(),
        )
        self.assertIsInstance(if_, jast.If)
        self.assertIsInstance(if_, jast.JAST)
        self.assertIsInstance(if_.test, jast.Constant)
        self.assertIsInstance(if_.test.value, jast.BoolLiteral)
        self.assertTrue(if_.test.value)
        self.assertIsInstance(if_.body, jast.Empty)
        self.assertIsInstance(if_.orelse, jast.Empty)
        self._test_iteration(if_)

    def test_If_error(self):
        self.assertRaises(
            JASTError,
            jast.If,
            body=jast.Empty(),
            orelse=jast.Empty(),
        )
        self.assertRaises(
            JASTError,
            jast.If,
            test=jast.Constant(jast.BoolLiteral(True)),
            orelse=jast.Empty(),
        )

    def test_Assert(self):
        assert_ = jast.Assert(
            test=jast.Constant(jast.BoolLiteral(True)),
            msg=jast.Constant(jast.StringLiteral("foo")),
        )
        self.assertIsInstance(assert_, jast.Assert)
        self.assertIsInstance(assert_, jast.JAST)
        self.assertIsInstance(assert_.test, jast.Constant)
        self.assertIsInstance(assert_.test.value, jast.BoolLiteral)
        self.assertTrue(assert_.test.value)
        self.assertIsInstance(assert_.msg, jast.Constant)
        self.assertIsInstance(assert_.msg.value, jast.StringLiteral)
        self.assertEqual("foo", assert_.msg.value.value)
        self._test_iteration(assert_)

    def test_Assert_error(self):
        self.assertRaises(
            JASTError,
            jast.Assert,
            msg=jast.Constant(jast.StringLiteral("foo")),
        )

    def test_Match(self):
        match = jast.Match(
            type=jast.Int(),
            id=jast.identifier("foo"),
        )
        self.assertIsInstance(match, jast.Match)
        self.assertIsInstance(match, jast.JAST)
        self.assertIsInstance(match.type, jast.Int)
        self._test_identifier(match.id, "foo")
        self._test_iteration(match)

    def test_Match_error(self):
        self.assertRaises(JASTError, jast.Match, id=jast.identifier("foo"))
        self.assertRaises(JASTError, jast.Match, type=jast.Int())

    def test_Case(self):
        case = jast.Case(
            guard=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(case, jast.Case)
        self.assertIsInstance(case, jast.JAST)
        self._test_int_constant(case.guard, 42)
        self._test_iteration(case)

    def test_Case_error(self):
        self.assertRaises(JASTError, jast.Case)

    def test_DefaultCase(self):
        default = jast.DefaultCase()
        self.assertIsInstance(default, jast.DefaultCase)
        self.assertIsInstance(default, jast.JAST)
        self._test_iteration(default)

    def test_Throw(self):
        throw = jast.Throw(
            exc=jast.Name(jast.identifier("foo")),
        )
        self.assertIsInstance(throw, jast.Throw)
        self.assertIsInstance(throw, jast.JAST)
        self._test_name(throw.exc, "foo")
        self._test_iteration(throw)

    def test_Throw_error(self):
        self.assertRaises(JASTError, jast.Throw)

    def test_switchgroup(self):
        switchgroup = jast.switchgroup(
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
        self.assertIsInstance(switchgroup, jast.switchgroup)
        self.assertIsInstance(switchgroup, jast.JAST)
        self.assertEqual(2, len(switchgroup.labels))
        self.assertIsInstance(switchgroup.labels[0], jast.Case)
        self.assertIsInstance(switchgroup.labels[1], jast.Case)
        self.assertEqual(1, len(switchgroup.body))
        self.assertIsInstance(switchgroup.body[0], jast.Empty)
        self._test_iteration(switchgroup)

    def test_switchgroup_error(self):
        self.assertRaises(JASTError, jast.switchgroup, body=[jast.Empty()])
        self.assertRaises(JASTError, jast.switchgroup, labels=[], body=[jast.Empty()])
        self.assertRaises(
            JASTError,
            jast.switchgroup,
            labels=[jast.Case(guard=jast.Constant(jast.IntLiteral(42)))],
        )
        self.assertRaises(
            JASTError,
            jast.switchgroup,
            labels=[jast.Case(guard=jast.Constant(jast.IntLiteral(42)))],
            body=[],
        )

    def test_switchblock(self):
        switchblock = jast.switchblock(
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
        self.assertIsInstance(switchblock, jast.switchblock)
        self.assertIsInstance(switchblock, jast.JAST)
        self.assertEqual(1, len(switchblock.groups))
        self.assertIsInstance(switchblock.groups[0], jast.switchgroup)
        self.assertEqual(1, len(switchblock.labels))
        self.assertIsInstance(switchblock.labels[0], jast.Case)
        self._test_iteration(switchblock)

    def test_Switch(self):
        switch = jast.Switch(
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
        self.assertIsInstance(switch, jast.Switch)
        self.assertIsInstance(switch, jast.JAST)
        self._test_name(switch.value, "foo")
        self.assertIsInstance(switch.body, jast.switchblock)
        self._test_iteration(switch)

    def test_Switch_error(self):
        self.assertRaises(
            JASTError,
            jast.Switch,
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
        self.assertRaises(
            JASTError, jast.Switch, value=jast.Name(jast.identifier("foo"))
        )

    def test_While(self):
        while_ = jast.While(
            test=jast.Constant(jast.BoolLiteral(True)),
            body=jast.Empty(),
        )
        self.assertIsInstance(while_, jast.While)
        self.assertIsInstance(while_, jast.JAST)
        self.assertIsInstance(while_.test, jast.Constant)
        self.assertIsInstance(while_.test.value, jast.BoolLiteral)
        self.assertTrue(while_.test.value)
        self.assertIsInstance(while_.body, jast.Empty)
        self._test_iteration(while_)

    def test_While_error(self):
        self.assertRaises(
            JASTError,
            jast.While,
            body=jast.Empty(),
        )
        self.assertRaises(
            JASTError,
            jast.While,
            test=jast.Constant(jast.BoolLiteral(True)),
        )

    def test_DoWhile(self):
        do_while = jast.DoWhile(
            body=jast.Empty(),
            test=jast.Constant(jast.BoolLiteral(True)),
        )
        self.assertIsInstance(do_while, jast.DoWhile)
        self.assertIsInstance(do_while, jast.JAST)
        self.assertIsInstance(do_while.body, jast.Empty)
        self.assertIsInstance(do_while.test, jast.Constant)
        self.assertIsInstance(do_while.test.value, jast.BoolLiteral)
        self.assertTrue(do_while.test.value)
        self._test_iteration(do_while)

    def test_DoWhile_error(self):
        self.assertRaises(
            JASTError,
            jast.DoWhile,
            body=jast.Empty(),
        )
        self.assertRaises(
            JASTError,
            jast.DoWhile,
            test=jast.Constant(jast.BoolLiteral(True)),
        )

    def test_For(self):
        for_ = jast.For(
            init=[
                jast.Assign(
                    target=jast.Name(jast.identifier("foo")),
                    value=jast.Constant(jast.IntLiteral(42)),
                )
            ],
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
        self.assertIsInstance(for_, jast.For)
        self.assertIsInstance(for_, jast.JAST)
        self.assertEqual(1, len(for_.init))
        self.assertIsInstance(for_.init[0], jast.Assign)
        self._test_name(for_.init[0].target, "foo")
        self._test_int_constant(for_.init[0].value, 42)
        self.assertIsInstance(for_.test, jast.BinOp)
        self._test_name(for_.test.left, "foo")
        self.assertIsInstance(for_.test.op, jast.Gt)
        self._test_int_constant(for_.test.right, 0)
        self.assertEqual(1, len(for_.update))
        self.assertIsInstance(for_.update[0], jast.PostOp)
        self._test_name(for_.update[0].operand, "foo")
        self.assertIsInstance(for_.update[0].op, jast.PostDec)
        self._test_iteration(for_)

    def test_For_error(self):
        self.assertRaises(
            JASTError,
            jast.For,
            init=[
                jast.Assign(
                    target=jast.Name(jast.identifier("foo")),
                    value=jast.Constant(jast.IntLiteral(42)),
                )
            ],
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
        )

    def test_ForEach(self):
        for_each = jast.ForEach(
            modifiers=[jast.Final()],
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            iter=jast.Name(jast.identifier("bar")),
            body=jast.Empty(),
        )
        self.assertIsInstance(for_each, jast.ForEach)
        self.assertIsInstance(for_each, jast.JAST)
        self.assertEqual(1, len(for_each.modifiers))
        self.assertIsInstance(for_each.modifiers[0], jast.Final)
        self.assertIsInstance(for_each.type, jast.Int)
        self.assertIsInstance(for_each.id, jast.variabledeclaratorid)
        self._test_identifier(for_each.id.id, "foo")
        self.assertEqual(0, len(for_each.id.dims))
        self._test_name(for_each.iter, "bar")
        self.assertIsInstance(for_each.body, jast.Empty)
        self._test_iteration(for_each)

    def test_ForEach_error(self):
        self.assertRaises(
            JASTError,
            jast.ForEach,
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            iter=jast.Name(jast.identifier("bar")),
            body=jast.Empty(),
        )
        self.assertRaises(
            JASTError,
            jast.ForEach,
            type=jast.Int(),
            iter=jast.Name(jast.identifier("bar")),
            body=jast.Empty(),
        )
        self.assertRaises(
            JASTError,
            jast.ForEach,
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            body=jast.Empty(),
        )
        self.assertRaises(
            JASTError,
            jast.ForEach,
            type=jast.Int(),
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            iter=jast.Name(jast.identifier("bar")),
        )

    def test_Break(self):
        break_ = jast.Break(label=jast.identifier("foo"))
        self.assertIsInstance(break_, jast.Break)
        self.assertIsInstance(break_, jast.JAST)
        self._test_identifier(break_.label, "foo")
        self._test_iteration(break_)

    def test_Continue(self):
        continue_ = jast.Continue(label=jast.identifier("foo"))
        self.assertIsInstance(continue_, jast.Continue)
        self.assertIsInstance(continue_, jast.JAST)
        self._test_identifier(continue_.label, "foo")
        self._test_iteration(continue_)

    def test_Return(self):
        return_ = jast.Return(value=jast.Constant(jast.IntLiteral(42)))
        self.assertIsInstance(return_, jast.Return)
        self.assertIsInstance(return_, jast.JAST)
        self._test_int_constant(return_.value, 42)
        self._test_iteration(return_)

    def test_Synch(self):
        synch = jast.Synch(lock=jast.Constant(jast.IntLiteral(42)), body=jast.Block())
        self.assertIsInstance(synch, jast.Synch)
        self.assertIsInstance(synch, jast.JAST)
        self._test_int_constant(synch.lock, 42)
        self.assertIsInstance(synch.body, jast.Block)
        self._test_iteration(synch)

    def test_Synch_error(self):
        self.assertRaises(JASTError, jast.Synch, body=jast.Block())
        self.assertRaises(
            JASTError, jast.Synch, lock=jast.Constant(jast.IntLiteral(42))
        )

    def test_catch(self):
        catch = jast.catch(
            modifiers=[jast.Final()],
            excs=[jast.qname([jast.identifier("foo")])],
            id=jast.identifier("bar"),
            body=jast.Block(),
        )
        self.assertIsInstance(catch, jast.catch)
        self.assertIsInstance(catch, jast.JAST)
        self.assertEqual(1, len(catch.modifiers))
        self.assertIsInstance(catch.modifiers[0], jast.Final)
        self.assertEqual(1, len(catch.excs))
        self.assertIsInstance(catch.excs[0], jast.qname)
        self._test_identifier(catch.id, "bar")
        self.assertIsInstance(catch.body, jast.Block)
        self._test_iteration(catch)

    def test_catch_error(self):
        self.assertRaises(
            JASTError,
            jast.catch,
            excs=[jast.qname([jast.identifier("foo")])],
            body=jast.Block(),
        )
        self.assertRaises(
            JASTError,
            jast.catch,
            excs=[jast.qname([jast.identifier("foo")])],
            id=jast.identifier("bar"),
        )
        self.assertRaises(
            JASTError,
            jast.catch,
            excs=[],
            id=jast.identifier("bar"),
            body=jast.Block(),
        )
        self.assertRaises(
            JASTError,
            jast.catch,
            id=jast.identifier("bar"),
            body=jast.Block(),
        )

    def test_Try(self):
        try_ = jast.Try(
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
        self.assertIsInstance(try_, jast.Try)
        self.assertIsInstance(try_, jast.JAST)
        self.assertIsInstance(try_.body, jast.Block)
        self.assertEqual(1, len(try_.catches))
        self.assertIsInstance(try_.catches[0], jast.catch)
        self.assertIsInstance(try_.final, jast.Block)
        self._test_iteration(try_)

    def test_Try_error(self):
        self.assertRaises(JASTError, jast.Try, body=jast.Block())
        self.assertRaises(JASTError, jast.Try, final=jast.Block())
        self.assertRaises(
            JASTError,
            jast.Try,
            catches=[
                jast.catch(
                    modifiers=[jast.Final()],
                    excs=[jast.qname([jast.identifier("foo")])],
                    id=jast.identifier("bar"),
                    body=jast.Block(),
                )
            ],
        )
        self.assertRaises(JASTError, jast.Try, body=jast.Block(), catches=[])

    def test_resource(self):
        resource = jast.resource(
            modifiers=[jast.Final()],
            type=jast.Int(),
            variable=jast.declarator(
                id=jast.variabledeclaratorid(jast.identifier("foo")),
                init=jast.Constant(jast.IntLiteral(42)),
            ),
        )
        self.assertIsInstance(resource, jast.resource)
        self.assertIsInstance(resource, jast.JAST)
        self.assertEqual(1, len(resource.modifiers))
        self.assertIsInstance(resource.modifiers[0], jast.Final)
        self.assertIsInstance(resource.type, jast.Int)
        self.assertIsInstance(resource.variable, jast.declarator)
        self.assertIsInstance(resource.variable.id, jast.variabledeclaratorid)
        self._test_identifier(resource.variable.id.id, "foo")
        self.assertEqual(0, len(resource.variable.id.dims))
        self._test_int_constant(resource.variable.init, 42)
        self._test_iteration(resource)

    def test_resource_error(self):
        self.assertRaises(JASTError, jast.resource, type=jast.Int())
        self.assertRaises(
            JASTError,
            jast.resource,
            variable=jast.declarator(
                id=jast.variabledeclaratorid(jast.identifier("foo")),
                init=jast.Constant(jast.IntLiteral(42)),
            ),
        )

    def test_TryWithResources(self):
        try_with_resources = jast.TryWithResources(
            resources=[
                jast.resource(
                    modifiers=[jast.Final()],
                    type=jast.Int(),
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
        self.assertIsInstance(try_with_resources, jast.TryWithResources)
        self.assertIsInstance(try_with_resources, jast.JAST)
        self.assertEqual(1, len(try_with_resources.resources))
        self.assertIsInstance(try_with_resources.resources[0], jast.resource)
        self.assertIsInstance(try_with_resources.body, jast.Block)
        self.assertEqual(1, len(try_with_resources.catches))
        self.assertIsInstance(try_with_resources.catches[0], jast.catch)
        self.assertIsInstance(try_with_resources.final, jast.Block)
        self._test_iteration(try_with_resources)

    def test_TryWithResources_error(self):
        self.assertRaises(JASTError, jast.TryWithResources, body=jast.Block())
        self.assertRaises(
            JASTError, jast.TryWithResources, resources=[], body=jast.Block()
        )
        self.assertRaises(
            JASTError,
            jast.TryWithResources,
            resources=[
                jast.resource(
                    modifiers=[jast.Final()],
                    type=jast.Int(),
                    variable=jast.declarator(
                        id=jast.variabledeclaratorid(jast.identifier("foo")),
                        init=jast.Constant(jast.IntLiteral(42)),
                    ),
                )
            ],
        )

    def test_Yield(self):
        yield_ = jast.Yield(value=jast.Constant(jast.IntLiteral(42)))
        self.assertIsInstance(yield_, jast.Yield)
        self.assertIsInstance(yield_, jast.JAST)
        self._test_int_constant(yield_.value, 42)
        self._test_iteration(yield_)

    def test_Yield_error(self):
        self.assertRaises(JASTError, jast.Yield)

    def test_EmptyDecl(self):
        empty_decl = jast.EmptyDecl()
        self.assertIsInstance(empty_decl, jast.EmptyDecl)
        self.assertIsInstance(empty_decl, jast.JAST)
        self._test_iteration(empty_decl)

    def test_Package(self):
        package = jast.Package(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            name=jast.qname([jast.identifier("bar"), jast.identifier("baz")]),
        )
        self.assertIsInstance(package, jast.Package)
        self.assertIsInstance(package, jast.JAST)
        self.assertEqual(1, len(package.annotations))
        self.assertIsInstance(package.annotations[0], jast.Annotation)
        self.assertIsInstance(package.name, jast.qname)
        self.assertEqual(2, len(package.name.identifiers))
        self._test_identifier(package.name.identifiers[0], "bar")
        self._test_identifier(package.name.identifiers[1], "baz")
        self._test_iteration(package)

    def test_Package_error(self):
        self.assertRaises(
            JASTError,
            jast.Package,
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
        )

    def test_Import(self):
        import_ = jast.Import(
            static=True,
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertIsInstance(import_, jast.Import)
        self.assertIsInstance(import_, jast.JAST)
        self.assertTrue(import_.static)
        self.assertIsInstance(import_.name, jast.qname)
        self.assertEqual(2, len(import_.name.identifiers))
        self._test_identifier(import_.name.identifiers[0], "foo")
        self._test_identifier(import_.name.identifiers[1], "bar")
        self._test_iteration(import_)

    def test_Import_on_demand(self):
        import_ = jast.Import(
            name=jast.qname([jast.identifier("foo")]),
            on_demand=True,
        )
        self.assertIsInstance(import_, jast.Import)
        self.assertIsInstance(import_, jast.JAST)
        self.assertFalse(import_.static)
        self.assertIsInstance(import_.name, jast.qname)
        self.assertEqual(1, len(import_.name.identifiers))
        self._test_identifier(import_.name.identifiers[0], "foo")
        self.assertTrue(import_.on_demand)
        self._test_iteration(import_)

    def test_Import_error(self):
        self.assertRaises(JASTError, jast.Import, static=True, on_demand=True)

    def test_Requires(self):
        requires = jast.Requires(
            modifiers=[jast.Static()],
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertIsInstance(requires, jast.Requires)
        self.assertIsInstance(requires, jast.JAST)
        self.assertEqual(1, len(requires.modifiers))
        self.assertIsInstance(requires.modifiers[0], jast.Static)
        self.assertIsInstance(requires.name, jast.qname)
        self.assertEqual(2, len(requires.name.identifiers))
        self._test_identifier(requires.name.identifiers[0], "foo")
        self._test_identifier(requires.name.identifiers[1], "bar")
        self._test_iteration(requires)

    def test_Requires_error(self):
        self.assertRaises(
            JASTError,
            jast.Requires,
            modifiers=[jast.Static()],
        )

    def test_Exports(self):
        exports = jast.Exports(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            to=jast.qname([jast.identifier("baz")]),
        )
        self.assertIsInstance(exports, jast.Exports)
        self.assertIsInstance(exports, jast.JAST)
        self.assertIsInstance(exports.name, jast.qname)
        self.assertEqual(2, len(exports.name.identifiers))
        self._test_identifier(exports.name.identifiers[0], "foo")
        self._test_identifier(exports.name.identifiers[1], "bar")
        self.assertIsInstance(exports.to, jast.qname)
        self.assertEqual(1, len(exports.to.identifiers))
        self._test_identifier(exports.to.identifiers[0], "baz")
        self._test_iteration(exports)

    def test_Exports_error(self):
        self.assertRaises(
            JASTError, jast.Exports, to=jast.qname([jast.identifier("baz")])
        )

    def test_Opens(self):
        opens = jast.Opens(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            to=jast.qname([jast.identifier("baz")]),
        )
        self.assertIsInstance(opens, jast.Opens)
        self.assertIsInstance(opens, jast.JAST)
        self.assertIsInstance(opens.name, jast.qname)
        self.assertEqual(2, len(opens.name.identifiers))
        self._test_identifier(opens.name.identifiers[0], "foo")
        self._test_identifier(opens.name.identifiers[1], "bar")
        self.assertIsInstance(opens.to, jast.qname)
        self.assertEqual(1, len(opens.to.identifiers))
        self._test_identifier(opens.to.identifiers[0], "baz")
        self._test_iteration(opens)

    def test_Opens_error(self):
        self.assertRaises(
            JASTError, jast.Opens, to=jast.qname([jast.identifier("baz")])
        )

    def test_Uses(self):
        uses = jast.Uses(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
        )
        self.assertIsInstance(uses, jast.Uses)
        self.assertIsInstance(uses, jast.JAST)
        self.assertIsInstance(uses.name, jast.qname)
        self.assertEqual(2, len(uses.name.identifiers))
        self._test_identifier(uses.name.identifiers[0], "foo")
        self._test_identifier(uses.name.identifiers[1], "bar")
        self._test_iteration(uses)

    def test_Uses_error(self):
        self.assertRaises(JASTError, jast.Uses)

    def test_Provides(self):
        provides = jast.Provides(
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            with_=jast.qname([jast.identifier("baz")]),
        )
        self.assertIsInstance(provides, jast.Provides)
        self.assertIsInstance(provides, jast.JAST)
        self.assertIsInstance(provides.name, jast.qname)
        self.assertEqual(2, len(provides.name.identifiers))
        self._test_identifier(provides.name.identifiers[0], "foo")
        self._test_identifier(provides.name.identifiers[1], "bar")
        self.assertIsInstance(provides.with_, jast.qname)
        self.assertEqual(1, len(provides.with_.identifiers))
        self._test_identifier(provides.with_.identifiers[0], "baz")
        self._test_iteration(provides)

    def test_Provides_error(self):
        self.assertRaises(
            JASTError, jast.Provides, with_=jast.qname([jast.identifier("baz")])
        )
        self.assertRaises(
            JASTError, jast.Provides, name=jast.qname([jast.identifier("foo")])
        )

    def test_Module(self):
        module = jast.Module(
            open=True,
            name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
            body=[jast.Uses(name=jast.qname([jast.identifier("baz")]))],
        )
        self.assertIsInstance(module, jast.Module)
        self.assertIsInstance(module, jast.JAST)
        self.assertTrue(module.open)
        self.assertIsInstance(module.name, jast.qname)
        self.assertEqual(2, len(module.name.identifiers))
        self._test_identifier(module.name.identifiers[0], "foo")
        self._test_identifier(module.name.identifiers[1], "bar")
        self.assertEqual(1, len(module.body))
        self.assertIsInstance(module.body[0], jast.Uses)
        self._test_iteration(module)

    def test_Module_error(self):
        self.assertRaises(
            JASTError,
            jast.Module,
            open=True,
            body=[jast.Uses(name=jast.qname([jast.identifier("baz")]))],
        )

    def test_declarator(self):
        declarator = jast.declarator(
            id=jast.variabledeclaratorid(jast.identifier("foo")),
            init=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(declarator, jast.declarator)
        self.assertIsInstance(declarator, jast.JAST)
        self.assertIsInstance(declarator.id, jast.variabledeclaratorid)
        self._test_identifier(declarator.id.id, "foo")
        self.assertEqual(0, len(declarator.id.dims))
        self.assertIsInstance(declarator.init, jast.Constant)
        self._test_int_constant(declarator.init, 42)
        self._test_iteration(declarator)

    def test_declarator_error(self):
        self.assertRaises(
            JASTError, jast.declarator, init=jast.Constant(jast.IntLiteral(42))
        )

    def test_Field(self):
        field = jast.Field(
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
        self.assertIsInstance(field, jast.Field)
        self.assertIsInstance(field, jast.JAST)
        self.assertEqual(1, len(field.modifiers))
        self.assertIsInstance(field.modifiers[0], jast.Final)
        self.assertIsInstance(field.type, jast.Int)
        self.assertEqual(2, len(field.declarators))
        self.assertIsInstance(field.declarators[0], jast.declarator)
        self.assertIsInstance(field.declarators[1], jast.declarator)
        self._test_iteration(field)

    def test_Field_error(self):
        self.assertRaises(
            JASTError,
            jast.Field,
            declarators=[
                jast.declarator(
                    id=jast.variabledeclaratorid(jast.identifier("foo")),
                    init=jast.Constant(jast.IntLiteral(42)),
                )
            ],
        )
        self.assertRaises(JASTError, jast.Field, type=jast.Int())
        self.assertRaises(JASTError, jast.Field, type=jast.Int(), declarators=[])

    def test_Method(self):
        method = jast.Method(
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            return_type=jast.Int(),
            id=jast.identifier("bar"),
            parameters=jast.params(
                parameters=[
                    jast.param(type=jast.Int(), id=jast.identifier("baz")),
                    jast.param(type=jast.Int(), id=jast.identifier("qux")),
                ],
            ),
            dims=[jast.dim()],
            throws=[jast.qname([jast.identifier("quux")])],
            body=jast.Block(),
        )
        self.assertIsInstance(method, jast.Method)
        self.assertIsInstance(method, jast.JAST)
        self.assertEqual(1, len(method.modifiers))
        self.assertIsInstance(method.modifiers[0], jast.Public)
        self.assertIsInstance(method.type_params, jast.typeparams)
        self.assertEqual(1, len(method.type_params.parameters))
        self.assertIsInstance(method.type_params.parameters[0], jast.typeparam)
        self._test_identifier(method.type_params.parameters[0].id, "T")
        self.assertEqual(1, len(method.annotations))
        self.assertIsInstance(method.annotations[0], jast.Annotation)
        self.assertIsInstance(method.return_type, jast.Int)
        self._test_identifier(method.id, "bar")
        self.assertIsInstance(method.parameters, jast.params)
        self.assertEqual(2, len(method.parameters.parameters))
        self.assertIsInstance(method.parameters.parameters[0], jast.param)
        self.assertIsInstance(method.parameters.parameters[1], jast.param)
        self.assertEqual(1, len(method.dims))
        self.assertIsInstance(method.dims[0], jast.dim)
        self.assertEqual(1, len(method.throws))
        self.assertIsInstance(method.throws[0], jast.qname)
        self._test_identifier(method.throws[0].identifiers[0], "quux")
        self.assertIsInstance(method.body, jast.Block)
        self._test_iteration(method)

    def test_Method_error(self):
        self.assertRaises(
            JASTError,
            jast.Method,
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            id=jast.identifier("bar"),
            parameters=jast.params(
                parameters=[
                    jast.param(type=jast.Int(), id=jast.identifier("baz")),
                    jast.param(type=jast.Int(), id=jast.identifier("qux")),
                ],
            ),
            dims=[jast.dim()],
            throws=[jast.qname([jast.identifier("quux")])],
        )
        self.assertRaises(
            JASTError,
            jast.Method,
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            return_type=jast.Int(),
            parameters=jast.params(
                parameters=[
                    jast.param(type=jast.Int(), id=jast.identifier("baz")),
                    jast.param(type=jast.Int(), id=jast.identifier("qux")),
                ],
            ),
            dims=[jast.dim()],
            throws=[jast.qname([jast.identifier("quux")])],
        )

    def test_Constructor(self):
        constructor = jast.Constructor(
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            id=jast.identifier("bar"),
            parameters=jast.params(
                parameters=[
                    jast.param(type=jast.Int(), id=jast.identifier("baz")),
                    jast.param(type=jast.Int(), id=jast.identifier("qux")),
                ],
            ),
            throws=[jast.qname([jast.identifier("quux")])],
            body=jast.Block(),
        )
        self.assertIsInstance(constructor, jast.Constructor)
        self.assertIsInstance(constructor, jast.JAST)
        self.assertEqual(1, len(constructor.modifiers))
        self.assertIsInstance(constructor.modifiers[0], jast.Public)
        self.assertIsInstance(constructor.type_params, jast.typeparams)
        self.assertEqual(1, len(constructor.type_params.parameters))
        self.assertIsInstance(constructor.type_params.parameters[0], jast.typeparam)
        self._test_identifier(constructor.type_params.parameters[0].id, "T")
        self._test_identifier(constructor.id, "bar")
        self.assertIsInstance(constructor.parameters, jast.params)
        self.assertEqual(2, len(constructor.parameters.parameters))
        self.assertIsInstance(constructor.parameters.parameters[0], jast.param)
        self.assertIsInstance(constructor.parameters.parameters[1], jast.param)
        self.assertEqual(1, len(constructor.throws))
        self.assertIsInstance(constructor.throws[0], jast.qname)
        self.assertEqual(1, len(constructor.throws[0].identifiers))
        self._test_identifier(constructor.throws[0].identifiers[0], "quux")
        self.assertIsInstance(constructor.body, jast.Block)
        self._test_iteration(constructor)

    def test_Constructor_error(self):
        self.assertRaises(
            JASTError,
            jast.Constructor,
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            parameters=jast.params(
                parameters=[
                    jast.param(type=jast.Int(), id=jast.identifier("baz")),
                    jast.param(type=jast.Int(), id=jast.identifier("qux")),
                ],
            ),
            body=jast.Block(),
        )

    def test_Initializer(self):
        initializer = jast.Initializer(
            static=True,
            body=jast.Block(),
        )
        self.assertIsInstance(initializer, jast.Initializer)
        self.assertIsInstance(initializer, jast.JAST)
        self.assertTrue(initializer.static)
        self.assertIsInstance(initializer.body, jast.Block)
        self._test_iteration(initializer)

    def test_Initializer_error(self):
        self.assertRaises(JASTError, jast.Initializer, static=True)

    def test_Interface(self):
        interface = jast.Interface(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            extends=[jast.Coit(id=jast.identifier("bar"))],
            implements=[jast.Coit(id=jast.identifier("baz"))],
            body=[jast.Method(return_type=jast.Int(), id=jast.identifier("qux"))],
        )
        self.assertIsInstance(interface, jast.Interface)
        self.assertIsInstance(interface, jast.JAST)
        self.assertEqual(1, len(interface.modifiers))
        self.assertIsInstance(interface.modifiers[0], jast.Public)
        self._test_identifier(interface.id, "foo")
        self.assertIsInstance(interface.type_params, jast.typeparams)
        self.assertEqual(1, len(interface.type_params.parameters))
        self.assertIsInstance(interface.type_params.parameters[0], jast.typeparam)
        self._test_identifier(interface.type_params.parameters[0].id, "T")
        self.assertEqual(1, len(interface.extends))
        self.assertIsInstance(interface.extends[0], jast.Coit)
        self._test_identifier(interface.extends[0].id, "bar")
        self.assertEqual(1, len(interface.implements))
        self.assertIsInstance(interface.implements[0], jast.Coit)
        self._test_identifier(interface.implements[0].id, "baz")
        self.assertEqual(1, len(interface.body))
        self.assertIsInstance(interface.body[0], jast.Method)
        self._test_iteration(interface)

    def test_Interface_error(self):
        self.assertRaises(
            JASTError,
            jast.Interface,
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            extends=[jast.Coit(id=jast.identifier("bar"))],
            permits=[jast.Coit(id=jast.identifier("baz"))],
            body=[jast.Method(return_type=jast.Int(), id=jast.identifier("qux"))],
        )

    def test_AnnotationMethod(self):
        annotation_method = jast.AnnotationMethod(
            modifiers=[jast.Public()],
            type=jast.Int(),
            id=jast.identifier("foo"),
            default=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertIsInstance(annotation_method, jast.AnnotationMethod)
        self.assertIsInstance(annotation_method, jast.JAST)
        self.assertEqual(1, len(annotation_method.modifiers))
        self.assertIsInstance(annotation_method.modifiers[0], jast.Public)
        self.assertIsInstance(annotation_method.type, jast.Int)
        self._test_identifier(annotation_method.id, "foo")
        self.assertIsInstance(annotation_method.default, jast.Constant)
        self._test_int_constant(annotation_method.default, 42)
        self._test_iteration(annotation_method)

    def test_AnnotationMethod_error(self):
        self.assertRaises(
            JASTError,
            jast.AnnotationMethod,
            modifiers=[jast.Public()],
            type=jast.Int(),
            default=jast.Constant(jast.IntLiteral(42)),
        )
        self.assertRaises(
            JASTError,
            jast.AnnotationMethod,
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
        )

    def test_AnnotationDecl(self):
        annotation_decl = jast.AnnotationDecl(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            extends=[jast.Coit(id=jast.identifier("bar"))],
            permits=[jast.Coit(id=jast.identifier("baz"))],
            body=[jast.AnnotationMethod(type=jast.Int(), id=jast.identifier("qux"))],
        )
        self.assertIsInstance(annotation_decl, jast.AnnotationDecl)
        self.assertIsInstance(annotation_decl, jast.JAST)
        self.assertEqual(1, len(annotation_decl.modifiers))
        self.assertIsInstance(annotation_decl.modifiers[0], jast.Public)
        self._test_identifier(annotation_decl.id, "foo")
        self.assertEqual(1, len(annotation_decl.extends))
        self.assertIsInstance(annotation_decl.extends[0], jast.Coit)
        self._test_identifier(annotation_decl.extends[0].id, "bar")
        self.assertEqual(1, len(annotation_decl.permits))
        self.assertIsInstance(annotation_decl.permits[0], jast.Coit)
        self._test_identifier(annotation_decl.permits[0].id, "baz")
        self.assertEqual(1, len(annotation_decl.body))
        self.assertIsInstance(annotation_decl.body[0], jast.AnnotationMethod)
        self._test_iteration(annotation_decl)

    def test_AnnotationDecl_error(self):
        self.assertRaises(
            JASTError,
            jast.AnnotationDecl,
            modifiers=[jast.Public()],
            extends=[jast.Coit(id=jast.identifier("bar"))],
            permits=[jast.Coit(id=jast.identifier("baz"))],
            body=[jast.AnnotationMethod(type=jast.Int(), id=jast.identifier("qux"))],
        )

    def test_Class(self):
        class_ = jast.Class(
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
        self.assertIsInstance(class_, jast.Class)
        self.assertIsInstance(class_, jast.JAST)
        self.assertEqual(1, len(class_.modifiers))
        self.assertIsInstance(class_.modifiers[0], jast.Public)
        self._test_identifier(class_.id, "foo")
        self.assertIsInstance(class_.type_params, jast.typeparams)
        self.assertEqual(1, len(class_.type_params.parameters))
        self.assertIsInstance(class_.type_params.parameters[0], jast.typeparam)
        self._test_identifier(class_.type_params.parameters[0].id, "T")
        self.assertIsInstance(class_.extends, jast.Coit)
        self._test_identifier(class_.extends.id, "bar")
        self.assertEqual(1, len(class_.implements))
        self.assertIsInstance(class_.implements[0], jast.Coit)
        self._test_identifier(class_.implements[0].id, "baz")
        self.assertEqual(1, len(class_.permits))
        self.assertIsInstance(class_.permits[0], jast.Coit)
        self._test_identifier(class_.permits[0].id, "qux")
        self.assertEqual(1, len(class_.body))
        self.assertIsInstance(class_.body[0], jast.Method)
        self._test_iteration(class_)

    def test_Class_error(self):
        self.assertRaises(
            JASTError,
            jast.Class,
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
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

    def test_enumconstant(self):
        enumconstant = jast.enumconstant(
            annotations=[jast.Annotation(jast.qname([jast.identifier("foo")]))],
            id=jast.identifier("bar"),
            args=[jast.Constant(jast.IntLiteral(42))],
            body=jast.Block(),
        )
        self.assertIsInstance(enumconstant, jast.enumconstant)
        self.assertIsInstance(enumconstant, jast.JAST)
        self.assertEqual(1, len(enumconstant.annotations))
        self.assertIsInstance(enumconstant.annotations[0], jast.Annotation)
        self._test_identifier(enumconstant.id, "bar")
        self.assertEqual(1, len(enumconstant.args))
        self._test_int_constant(enumconstant.args[0], 42)
        self.assertIsInstance(enumconstant.body, jast.Block)
        self._test_iteration(enumconstant)

    def test_enumconstant_error(self):
        self.assertRaises(
            JASTError,
            jast.enumconstant,
            args=[jast.Constant(jast.IntLiteral(42))],
            body=jast.Block(),
        )

    def test_Enum(self):
        enum = jast.Enum(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            implements=[jast.Coit(id=jast.identifier("bar"))],
            constants=[jast.enumconstant(id=jast.identifier("baz"))],
            body=[
                jast.Method(
                    return_type=jast.Int(), id=jast.identifier("qux"), body=jast.Block()
                )
            ],
        )
        self.assertIsInstance(enum, jast.Enum)
        self.assertIsInstance(enum, jast.JAST)
        self.assertEqual(1, len(enum.modifiers))
        self.assertIsInstance(enum.modifiers[0], jast.Public)
        self._test_identifier(enum.id, "foo")
        self.assertEqual(1, len(enum.implements))
        self.assertIsInstance(enum.implements[0], jast.Coit)
        self._test_identifier(enum.implements[0].id, "bar")
        self.assertEqual(1, len(enum.constants))
        self.assertIsInstance(enum.constants[0], jast.enumconstant)
        self.assertEqual(1, len(enum.body))
        self.assertIsInstance(enum.body[0], jast.Method)
        self._test_iteration(enum)

    def test_Enum_error(self):
        self.assertRaises(
            JASTError,
            jast.Enum,
            modifiers=[jast.Public()],
            implements=[jast.Coit(id=jast.identifier("bar"))],
            constants=[jast.enumconstant(id=jast.identifier("baz"))],
            body=[
                jast.Method(
                    return_type=jast.Int(), id=jast.identifier("qux"), body=jast.Block()
                )
            ],
        )

    def test_recordcomponent(self):
        recordcomponent = jast.recordcomponent(
            type=jast.Int(),
            id=jast.identifier("foo"),
        )
        self.assertIsInstance(recordcomponent, jast.recordcomponent)
        self.assertIsInstance(recordcomponent, jast.JAST)
        self.assertIsInstance(recordcomponent.type, jast.Int)
        self._test_identifier(recordcomponent.id, "foo")
        self._test_iteration(recordcomponent)

    def test_recordcomponent_error(self):
        self.assertRaises(
            JASTError,
            jast.recordcomponent,
            id=jast.identifier("foo"),
        )
        self.assertRaises(
            JASTError,
            jast.recordcomponent,
            type=jast.Int(),
        )

    def test_Record(self):
        record = jast.Record(
            modifiers=[jast.Public()],
            id=jast.identifier("foo"),
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            components=[
                jast.recordcomponent(type=jast.Int(), id=jast.identifier("bar"))
            ],
            implements=[jast.Coit(id=jast.identifier("baz"))],
            body=[
                jast.Method(
                    return_type=jast.Int(), id=jast.identifier("qux"), body=jast.Block()
                )
            ],
        )
        self.assertIsInstance(record, jast.Record)
        self.assertIsInstance(record, jast.JAST)
        self.assertEqual(1, len(record.modifiers))
        self.assertIsInstance(record.modifiers[0], jast.Public)
        self._test_identifier(record.id, "foo")
        self.assertIsInstance(record.type_params, jast.typeparams)
        self.assertEqual(1, len(record.type_params.parameters))
        self.assertIsInstance(record.type_params.parameters[0], jast.typeparam)
        self._test_identifier(record.type_params.parameters[0].id, "T")
        self.assertEqual(1, len(record.components))
        self.assertIsInstance(record.components[0], jast.recordcomponent)
        self.assertEqual(1, len(record.implements))
        self.assertIsInstance(record.implements[0], jast.Coit)
        self._test_identifier(record.implements[0].id, "baz")
        self.assertEqual(1, len(record.body))
        self.assertIsInstance(record.body[0], jast.Method)
        self._test_iteration(record)

    def test_Record_error(self):
        self.assertRaises(
            JASTError,
            jast.Record,
            modifiers=[jast.Public()],
            type_params=jast.typeparams(
                parameters=[jast.typeparam(id=jast.identifier("T"))],
            ),
            components=[
                jast.recordcomponent(type=jast.Int(), id=jast.identifier("bar"))
            ],
            implements=[jast.Coit(id=jast.identifier("baz"))],
            body=[
                jast.Method(
                    return_type=jast.Int(), id=jast.identifier("qux"), body=jast.Block()
                )
            ],
        )

    def test_CompilationUnit(self):
        compilation_unit = jast.CompilationUnit(
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
        self.assertIsInstance(compilation_unit, jast.CompilationUnit)
        self.assertIsInstance(compilation_unit, jast.JAST)
        self.assertIsInstance(compilation_unit.package, jast.Package)
        self.assertIsInstance(compilation_unit.imports[0], jast.Import)
        self.assertIsInstance(compilation_unit.body[0], jast.Class)
        self._test_iteration(compilation_unit)

    def test_ModularUnit(self):
        modular_unit = jast.ModularUnit(
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
        self.assertIsInstance(modular_unit, jast.ModularUnit)
        self.assertIsInstance(modular_unit, jast.JAST)
        self.assertIsInstance(modular_unit.imports[0], jast.Import)
        self.assertIsInstance(modular_unit.body, jast.Module)
        self._test_iteration(modular_unit)

    def test_ModularUnit_error(self):
        self.assertRaises(
            JASTError,
            jast.ModularUnit,
            imports=[
                jast.Import(
                    static=True,
                    name=jast.qname([jast.identifier("foo"), jast.identifier("bar")]),
                )
            ],
        )
