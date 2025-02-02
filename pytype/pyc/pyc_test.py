"""Tests for pyc.py."""


from pytype.pyc import opcodes
from pytype.pyc import pyc
import unittest


class TestPyc(unittest.TestCase):
  """Tests for pyc.py."""

  python_version = (2, 7)

  def _compile(self, src):
    pyc_data = pyc.compile_src_string_to_pyc_string(
        src, python_version=self.python_version)
    return pyc.parse_pyc_string(pyc_data)

  def test_compile(self):
    code = self._compile("foobar = 3")
    self.assertIn("foobar", code.co_names)
    self.assertEquals(self.python_version, code.python_version)

  def test_lineno(self):
    code = self._compile("a = 1\n"      # line 1
                         "\n"           # line 2
                         "a = a + 1\n"  # line 3
                        )
    self.assertIn("a", code.co_names)
    op_and_line = [(op.name, op.line) for op in opcodes.dis_code(code)]
    self.assertEquals([("LOAD_CONST", 1),
                       ("STORE_NAME", 1),
                       ("LOAD_NAME", 3),
                       ("LOAD_CONST", 3),
                       ("BINARY_ADD", 3),
                       ("STORE_NAME", 3),
                       ("LOAD_CONST", 3),
                       ("RETURN_VALUE", 3)], op_and_line)

  def test_singlelineno(self):
    code = self._compile("a = 1\n"      # line 1
                        )
    self.assertIn("a", code.co_names)
    op_and_line = [(op.name, op.line) for op in opcodes.dis_code(code)]
    self.assertEquals([("LOAD_CONST", 1),
                       ("STORE_NAME", 1),
                       ("LOAD_CONST", 1),
                       ("RETURN_VALUE", 1)], op_and_line)

  def test_singlelinenowithspace(self):
    code = self._compile("\n"
                         "\n"
                         "a = 1\n"      # line 3
                        )
    self.assertIn("a", code.co_names)
    op_and_line = [(op.name, op.line) for op in opcodes.dis_code(code)]
    self.assertEquals([("LOAD_CONST", 3),
                       ("STORE_NAME", 3),
                       ("LOAD_CONST", 3),
                       ("RETURN_VALUE", 3)], op_and_line)


if __name__ == "__main__":
  unittest.main()
