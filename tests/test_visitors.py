import unittest

import jast

from copy import copy


class TestVisitor(unittest.TestCase):
    def setUp(self):
        self.source = (
            "public class Example {\n"
            "    public int add(int a, int b) {\n"
            "        return a + b;\n"
            "    }\n"
            "    \n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "}"
        )
        self.example = jast.parse(self.source)

    def test_IdentifierVisitor(self):
        class IdentifierVisitor(jast.JNodeVisitor):
            def default_result(self):
                return []

            def aggregate_result(self, aggregate, result):
                return aggregate + result

            def visit_identifier(self, node):
                return [node.value]

        visitor = IdentifierVisitor()
        identifiers = visitor.visit(self.example)
        self.assertEqual(
            [
                "Example",
                "add",
                "a",
                "b",
                "a",
                "b",
                "main",
                "String",
                "args",
                "System",
                "out",
                "println",
                "add",
            ],
            identifiers,
        )

    def test_ChangeAdd(self):
        class ChangeAdd(jast.JNodeTransformer):
            def visit_Method(self, node):
                if node.id == "add":
                    node.body = self.visit(node.body)
                    return node
                return node

            def visit_BinOp(self, node):
                if isinstance(node.op, jast.Add):
                    node.op = jast.Sub()
                    return node
                return node

        change_add = ChangeAdd()
        new_tree = change_add.visit(self.example)
        code = jast.unparse(new_tree)
        self.assertEqual(
            "public class Example {\n"
            "    public int add(int a, int b) {\n"
            "        return a - b;\n"
            "    }\n"
            "    \n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "}",
            code,
        )
        self.assertIs(self.example, new_tree)

    def test_ChangeAdd_keep(self):
        class ChangeAdd(jast.JNodeKeepTransformer):
            def visit_Method(self, node):
                if node.id == "add":
                    node.body = self.visit(node.body)
                return node

            def visit_BinOp(self, node):
                if isinstance(node.op, jast.Add):
                    node.op = jast.Sub()
                return node

        change_add = ChangeAdd()
        new_tree = change_add.visit(self.example)
        code = jast.unparse(new_tree)
        self.assertEqual(
            "public class Example {\n"
            "    public int add(int a, int b) {\n"
            "        return a - b;\n"
            "    }\n"
            "    \n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "}",
            code,
        )
        self.assertIsNot(self.example, new_tree)
        self.assertEqual(
            self.source,
            jast.unparse(self.example),
        )

    def test_copy_identifier(self):
        identifier = jast.identifier("a")
        new_identifier = copy(identifier)
        self.assertIsNot(identifier, new_identifier)
        self.assertEqual(identifier, new_identifier)
        self.assertEqual(identifier.value, new_identifier.value)

    def test_copy_IntLiteral(self):
        int_literal = jast.IntLiteral(42)
        new_int_literal = copy(int_literal)
        self.assertIsNot(int_literal, new_int_literal)
        self.assertEqual(int_literal, new_int_literal)
        self.assertEqual(int_literal.value, new_int_literal.value)

    def test_copy_FloatLiteral(self):
        float_literal = jast.FloatLiteral(3.14)
        new_float_literal = copy(float_literal)
        self.assertIsNot(float_literal, new_float_literal)
        self.assertEqual(float_literal, new_float_literal)
        self.assertEqual(float_literal.value, new_float_literal.value)

    def test_copy_BoolLiteral(self):
        bool_literal = jast.BoolLiteral(True)
        new_bool_literal = copy(bool_literal)
        self.assertIsNot(bool_literal, new_bool_literal)
        self.assertEqual(bool_literal, new_bool_literal)
        self.assertEqual(bool_literal.value, new_bool_literal.value)

    def test_copy_CharLiteral(self):
        char_literal = jast.CharLiteral("a")
        new_char_literal = copy(char_literal)
        self.assertIsNot(char_literal, new_char_literal)
        self.assertEqual(char_literal, new_char_literal)
        self.assertEqual(char_literal.value, new_char_literal.value)

    def test_copy_StringLiteral(self):
        string_literal = jast.StringLiteral("Hello, World!")
        new_string_literal = copy(string_literal)
        self.assertIsNot(string_literal, new_string_literal)
        self.assertEqual(string_literal, new_string_literal)
        self.assertEqual(string_literal.value, new_string_literal.value)

    def test_copy_TextBlock(self):
        text_block = jast.TextBlock(["Hello,", "World!"])
        new_text_block = copy(text_block)
        self.assertIsNot(text_block, new_text_block)
        self.assertEqual(text_block.value, new_text_block.value)

    def test_DeleteReturn(self):
        class DeleteReturn(jast.JNodeTransformer):
            def visit_Return(self, node):
                return None

        delete_return = DeleteReturn()
        new_tree = delete_return.visit(self.example)
        code = jast.unparse(new_tree)
        self.assertEqual(
            "public class Example {\n"
            "    public int add(int a, int b) {}\n"
            "    \n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "}",
            code,
        )

    def test_DeleteReturn_keep(self):
        class DeleteReturn(jast.JNodeKeepTransformer):
            def visit_Return(self, node):
                return None

        delete_return = DeleteReturn()
        new_tree = delete_return.visit(self.example)
        code = jast.unparse(new_tree)
        self.assertEqual(
            "public class Example {\n"
            "    public int add(int a, int b) {}\n"
            "    \n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "}",
            code,
        )
        self.assertIsNot(self.example, new_tree)
        self.assertEqual(
            self.source,
            jast.unparse(self.example),
        )

    def test_DeleteAndAdd(self):
        class DeleteAndAdd(jast.JNodeTransformer):
            def __init__(self):
                self.to_add = None

            def visit_Method(self, node):
                if node.id == "add":
                    self.to_add = node
                    return None
                elif node.id == "main":
                    return [node, self.to_add]
                return node

        delete_and_add = DeleteAndAdd()
        new_tree = delete_and_add.visit(self.example)
        code = jast.unparse(new_tree)
        self.assertEqual(
            "public class Example {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "    \n"
            "    public int add(int a, int b) {\n"
            "        return a + b;\n"
            "    }\n"
            "}",
            code,
        )

    def test_DeleteAndAdd_keep(self):
        class DeleteAndAdd(jast.JNodeKeepTransformer):
            def __init__(self):
                self.to_add = None

            def visit_Method(self, node):
                if node.id == "add":
                    self.to_add = node
                    return None
                elif node.id == "main":
                    return [node, self.to_add]
                return node

        delete_and_add = DeleteAndAdd()
        new_tree = delete_and_add.visit(self.example)
        code = jast.unparse(new_tree)
        self.assertEqual(
            "public class Example {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(add(27, 55));\n"
            "    }\n"
            "    \n"
            "    public int add(int a, int b) {\n"
            "        return a + b;\n"
            "    }\n"
            "}",
            code,
        )
        self.assertIsNot(self.example, new_tree)
        self.assertEqual(
            self.source,
            jast.unparse(self.example),
        )
