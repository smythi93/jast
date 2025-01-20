import unittest

import jast


class TestConstructors(unittest.TestCase):
    def test_identifier(self):
        identifier = jast.identifier("foo")
        self.assertIsInstance(identifier, str)
        self.assertEqual(identifier, "foo")
        self.assertIsInstance(identifier, jast.JAST)
