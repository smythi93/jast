import unittest

import jast

OPERATORS_ASSIGN = [
    ("Add", "+", jast.Add),
    ("Sub", "-", jast.Sub),
    ("Mult", "*", jast.Mult),
    ("Div", "/", jast.Div),
    ("Mod", "%", jast.Mod),
    ("BitAnd", "&", jast.BitAnd),
    ("BitOr", "|", jast.BitOr),
    ("BitXor", "^", jast.BitXor),
    ("LShift", "<<", jast.LShift),
    ("RShift", ">>", jast.RShift),
    ("URShift", ">>>", jast.URShift),
]

OPERATORS = [
    ("Add", "+", jast.Add),
    ("Sub", "-", jast.Sub),
    ("Mult", "*", jast.Mult),
    ("Div", "/", jast.Div),
    ("Mod", "%", jast.Mod),
    ("And", "&&", jast.And),
    ("Or", "||", jast.Or),
    ("BitAnd", "&", jast.BitAnd),
    ("BitOr", "|", jast.BitOr),
    ("BitXor", "^", jast.BitXor),
    ("LShift", "<<", jast.LShift),
    ("RShift", ">>", jast.RShift),
    ("URShift", ">>>", jast.URShift),
    ("Eq", "==", jast.Eq),
    ("NotEq", "!=", jast.NotEq),
    ("Lt", "<", jast.Lt),
    ("LtE", "<=", jast.LtE),
    ("Gt", ">", jast.Gt),
    ("GtE", ">=", jast.GtE),
]

LEFT_PRECEDENCE_FOR_RIGHT = [
    ("Or_Or", "||", "||", jast.Or, jast.Or),
    ("And_And", "&&", "&&", jast.And, jast.And),
    ("And_Or", "&&", "||", jast.And, jast.Or),
    ("BitOr_BitOr", "|", "|", jast.BitOr, jast.BitOr),
    ("BitOr_And", "|", "&&", jast.BitOr, jast.And),
    ("BitXor_BitXor", "^", "^", jast.BitXor, jast.BitXor),
    ("BitXor_BitOr", "^", "|", jast.BitXor, jast.BitOr),
    ("BitAnd_BitAnd", "&", "&", jast.BitAnd, jast.BitAnd),
    ("BitAnd_BitXor", "&", "^", jast.BitAnd, jast.BitXor),
    ("Eq_Eq", "==", "==", jast.Eq, jast.Eq),
    ("Eq_NotEq", "==", "!=", jast.Eq, jast.NotEq),
    ("NotEq_NotEq", "!=", "!=", jast.NotEq, jast.NotEq),
    ("NotEq_Eq", "!=", "==", jast.NotEq, jast.Eq),
    ("Eq_BitAnd", "==", "&", jast.Eq, jast.BitAnd),
    ("NotEq_BitAnd", "!=", "&", jast.NotEq, jast.BitAnd),
    ("Lt_Lt", "<", "<", jast.Lt, jast.Lt),
    ("Lt_LtE", "<", "<=", jast.Lt, jast.LtE),
    ("LtE_Lt", "<=", "<", jast.LtE, jast.Lt),
    ("LtE_LtE", "<=", "<=", jast.LtE, jast.LtE),
    ("Lt_Gt", "<", ">", jast.Lt, jast.Gt),
    ("Lt_GtE", "<", ">=", jast.Lt, jast.GtE),
    ("LtE_Gt", "<=", ">", jast.LtE, jast.Gt),
    ("LtE_GtE", "<=", ">=", jast.LtE, jast.GtE),
    ("Gt_Lt", ">", "<", jast.Gt, jast.Lt),
    ("Gt_LtE", ">", "<=", jast.Gt, jast.LtE),
    ("Gt_Lt", ">", "<", jast.Gt, jast.Lt),
    ("Gt_LtE", ">", "<=", jast.Gt, jast.LtE),
    ("Gt_Gt", ">", ">", jast.Gt, jast.Gt),
    ("Gt_GtE", ">", ">=", jast.Gt, jast.GtE),
    ("GtE_Gt", ">=", ">", jast.GtE, jast.Gt),
    ("GtE_GtE", ">=", ">=", jast.GtE, jast.GtE),
    ("Lt_Eq", "<", "==", jast.Lt, jast.Eq),
    ("Lt_NotEq", "<", "!=", jast.Lt, jast.NotEq),
    ("LtE_Eq", "<=", "==", jast.LtE, jast.Eq),
    ("LtE_NotEq", "<=", "!=", jast.LtE, jast.NotEq),
    ("Gt_Eq", ">", "==", jast.Gt, jast.Eq),
    ("Gt_NotEq", ">", "!=", jast.Gt, jast.NotEq),
    ("GtE_Eq", ">=", "==", jast.GtE, jast.Eq),
    ("GtE_NotEq", ">=", "!=", jast.GtE, jast.NotEq),
    ("LShift_LShift", "<<", "<<", jast.LShift, jast.LShift),
    ("LShift_RShift", "<<", ">>", jast.LShift, jast.RShift),
    ("LShift_URShift", "<<", ">>>", jast.LShift, jast.URShift),
    ("RShift_LShift", ">>", "<<", jast.RShift, jast.LShift),
    ("RShift_RShift", ">>", ">>", jast.RShift, jast.RShift),
    ("RShift_URShift", ">>", ">>>", jast.RShift, jast.URShift),
    ("URShift_LShift", ">>>", "<<", jast.URShift, jast.LShift),
    ("URShift_RShift", ">>>", ">>", jast.URShift, jast.RShift),
    ("URShift_URShift", ">>>", ">>>", jast.URShift, jast.URShift),
    ("LShift_Lt", "<<", "<", jast.LShift, jast.Lt),
    ("LShift_LtE", "<<", "<=", jast.LShift, jast.LtE),
    ("LShift_Gt", "<<", ">", jast.LShift, jast.Gt),
    ("LShift_GtE", "<<", ">=", jast.LShift, jast.GtE),
    ("RShift_Lt", ">>", "<", jast.RShift, jast.Lt),
    ("RShift_LtE", ">>", "<=", jast.RShift, jast.LtE),
    ("RShift_Gt", ">>", ">", jast.RShift, jast.Gt),
    ("RShift_GtE", ">>", ">=", jast.RShift, jast.GtE),
    ("URShift_Lt", ">>>", "<", jast.URShift, jast.Lt),
    ("URShift_LtE", ">>>", "<=", jast.URShift, jast.LtE),
    ("URShift_Gt", ">>>", ">", jast.URShift, jast.Gt),
    ("URShift_GtE", ">>>", ">=", jast.URShift, jast.GtE),
    ("Add_Add", "+", "+", jast.Add, jast.Add),
    ("Add_Sub", "+", "-", jast.Add, jast.Sub),
    ("Sub_Add", "-", "+", jast.Sub, jast.Add),
    ("Sub_Sub", "-", "-", jast.Sub, jast.Sub),
    ("Add_LShift", "+", "<<", jast.Add, jast.LShift),
    ("Add_RShift", "+", ">>", jast.Add, jast.RShift),
    ("Add_URShift", "+", ">>>", jast.Add, jast.URShift),
    ("Sub_LShift", "-", "<<", jast.Sub, jast.LShift),
    ("Sub_RShift", "-", ">>", jast.Sub, jast.RShift),
    ("Sub_URShift", "-", ">>>", jast.Sub, jast.URShift),
    ("Mult_Mult", "*", "*", jast.Mult, jast.Mult),
    ("Mult_Div", "*", "/", jast.Mult, jast.Div),
    ("Mult_Mod", "*", "%", jast.Mult, jast.Mod),
    ("Div_Mult", "/", "*", jast.Div, jast.Mult),
    ("Div_Div", "/", "/", jast.Div, jast.Div),
    ("Div_Mod", "/", "%", jast.Div, jast.Mod),
    ("Mod_Mult", "%", "*", jast.Mod, jast.Mult),
    ("Mod_Div", "%", "/", jast.Mod, jast.Div),
    ("Mod_Mod", "%", "%", jast.Mod, jast.Mod),
    ("Mult_Add", "*", "+", jast.Mult, jast.Add),
    ("Mult_Sub", "*", "-", jast.Mult, jast.Sub),
    ("Div_Add", "/", "+", jast.Div, jast.Add),
    ("Div_Sub", "/", "-", jast.Div, jast.Sub),
    ("Mod_Add", "%", "+", jast.Mod, jast.Add),
    ("Mod_Sub", "%", "-", jast.Mod, jast.Sub),
]

RIGHT_PRECEDENCE_FOR_LEFT = [
    ("Add_Mult", "+", "*", jast.Add, jast.Mult),
    ("Add_Div", "+", "/", jast.Add, jast.Div),
    ("Add_Mod", "+", "%", jast.Add, jast.Mod),
    ("Sub_Mult", "-", "*", jast.Sub, jast.Mult),
    ("Sub_Div", "-", "/", jast.Sub, jast.Div),
    ("Sub_Mod", "-", "%", jast.Sub, jast.Mod),
    ("LShift_Add", "<<", "+", jast.LShift, jast.Add),
    ("LShift_Sub", "<<", "-", jast.LShift, jast.Sub),
    ("RShift_Add", ">>", "+", jast.RShift, jast.Add),
    ("RShift_Sub", ">>", "-", jast.RShift, jast.Sub),
    ("URShift_Add", ">>>", "+", jast.URShift, jast.Add),
    ("URShift_Sub", ">>>", "-", jast.URShift, jast.Sub),
    ("Lt_LShift", "<", "<<", jast.Lt, jast.LShift),
    ("Lt_RShift", "<", ">>", jast.Lt, jast.RShift),
    ("Lt_URShift", "<", ">>>", jast.Lt, jast.URShift),
    ("LtE_LShift", "<=", "<<", jast.LtE, jast.LShift),
    ("LtE_RShift", "<=", ">>", jast.LtE, jast.RShift),
    ("LtE_URShift", "<=", ">>>", jast.LtE, jast.URShift),
    ("Gt_LShift", ">", "<<", jast.Gt, jast.LShift),
    ("Gt_RShift", ">", ">>", jast.Gt, jast.RShift),
    ("Gt_URShift", ">", ">>>", jast.Gt, jast.URShift),
    ("GtE_LShift", ">=", "<<", jast.GtE, jast.LShift),
    ("GtE_RShift", ">=", ">>", jast.GtE, jast.RShift),
    ("GtE_URShift", ">=", ">>>", jast.GtE, jast.URShift),
    ("Eq_Lt", "==", "<", jast.Eq, jast.Lt),
    ("Eq_LtE", "==", "<=", jast.Eq, jast.LtE),
    ("Eq_Gt", "==", ">", jast.Eq, jast.Gt),
    ("Eq_GtE", "==", ">=", jast.Eq, jast.GtE),
    ("NotEq_Lt", "!=", "<", jast.NotEq, jast.Lt),
    ("NotEq_LtE", "!=", "<=", jast.NotEq, jast.LtE),
    ("NotEq_Gt", "!=", ">", jast.NotEq, jast.Gt),
    ("NotEq_GtE", "!=", ">=", jast.NotEq, jast.GtE),
    ("BitAnd_Eq", "&", "==", jast.BitAnd, jast.Eq),
    ("BitAnd_NotEq", "&", "!=", jast.BitAnd, jast.NotEq),
    ("BitXor_BitAnd", "^", "&", jast.BitXor, jast.BitAnd),
    ("BitOr_BitXor", "|", "^", jast.BitOr, jast.BitXor),
    ("And_BitOr", "&&", "|", jast.And, jast.BitOr),
    ("Or_And", "||", "&&", jast.Or, jast.And),
]

INSTANCEOF_LOWER_PRECEDENCE = [
    ("Eq", "==", jast.Eq),
    ("NotEq", "!=", jast.NotEq),
    ("BitAnd", "&", jast.BitAnd),
    ("BitXor", "^", jast.BitXor),
    ("BitOr", "|", jast.BitOr),
    ("And", "&&", jast.And),
    ("Or", "||", jast.Or),
]

INSTANCEOF_SAME_PRECEDENCE = [
    ("Lt", "<", jast.Lt),
    ("LtE", "<=", jast.LtE),
    ("Gt", ">", jast.Gt),
    ("GtE", ">=", jast.GtE),
]

INSTANCEOF_HIGHER_PRECEDENCE = [
    ("LShift", "<<", jast.LShift),
    ("RShift", ">>", jast.RShift),
    ("URShift", ">>>", jast.URShift),
    ("Add", "+", jast.Add),
    ("Sub", "-", jast.Sub),
    ("Mult", "*", jast.Mult),
    ("Div", "/", jast.Div),
    ("Mod", "%", jast.Mod),
]

INSTANCEOF_HIGHER_SAME_PRECEDENCE = (
    INSTANCEOF_SAME_PRECEDENCE + INSTANCEOF_HIGHER_PRECEDENCE
)

INSTANCEOF_LOWER_SAME_PRECEDENCE = (
    INSTANCEOF_SAME_PRECEDENCE + INSTANCEOF_LOWER_PRECEDENCE
)

UNARY_OPERATORS = [
    ("UAdd", "+", jast.UAdd),
    ("USub", "-", jast.USub),
    ("Invert", "~", jast.Invert),
    ("Not", "!", jast.Not),
    ("PreInc", "++", jast.PreInc),
    ("PreDec", "--", jast.PreDec),
]

POST_OPERATORS = [
    ("PostInc", "++", jast.PostInc),
    ("PostDec", "--", jast.PostDec),
]


class BaseTest(unittest.TestCase):
    def _test_int_literal(self, literal, expected: int = 42):
        self.assertIsInstance(literal, jast.IntLiteral)
        self.assertEqual(literal.value, expected)

    def _test_int_constant(self, constant, expected: int = 42):
        self.assertIsInstance(constant, jast.Constant)
        self._test_int_literal(constant.value, expected)

    def _test_bool_constant(self, constant, expected: bool = True):
        self.assertIsInstance(constant, jast.Constant)
        self.assertIsInstance(constant.value, jast.BoolLiteral)
        if expected:
            self.assertTrue(constant.value.value)
        else:
            self.assertFalse(constant.value.value)

    def _test_identifier(self, identifier, expected: str):
        self.assertIsInstance(identifier, jast.identifier)
        self.assertEqual(expected, identifier)

    def _test_variabledeclaratorid(self, vdi, expected: str, dims: int = 0):
        self.assertIsInstance(vdi, jast.variabledeclaratorid)
        self._test_identifier(vdi.id, expected)
        self.assertEqual(dims, len(vdi.dims))
        for dim in vdi.dims:
            self.assertIsInstance(dim, jast.dim)

    def _test_name(self, name, expected: str):
        self.assertIsInstance(name, jast.Name)
        self._test_identifier(name.id, expected)
