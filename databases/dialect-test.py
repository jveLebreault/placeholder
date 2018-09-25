from dialects import SqliteDialect
import unittest

class SqliteDialectTest(unittest.TestCase):

    def test_DialectInstance(self):
        SqliteDialect()


if __name__ == '__main__':
    unittest.main()