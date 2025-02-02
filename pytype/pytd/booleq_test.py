# -*- coding:utf-8; python-indent:2; indent-tabs-mode:nil -*-
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for booleq.py."""

import unittest

from pytype.pytd import booleq

# pylint: disable=invalid-name
And = booleq.And
Or = booleq.Or
Eq = booleq.Eq
TRUE = booleq.TRUE
FALSE = booleq.FALSE


# TODO(kramm): pludemann@ wants me to remind him to create more tests for
#              booleq.py.


class TestBoolEq(unittest.TestCase):
  """Test algorithms and datastructures of booleq.py."""

  def testTrueAndFalse(self):
    self.assertNotEqual(TRUE, FALSE)
    self.assertNotEqual(FALSE, TRUE)
    self.assertEqual(TRUE, TRUE)
    self.assertEqual(FALSE, FALSE)

  def testEquality(self):
    self.assertEqual(Eq("a", "b"), Eq("b", "a"))
    self.assertEqual(Eq("a", "b"), Eq("a", "b"))
    self.assertNotEqual(Eq("a", "a"), Eq("a", "b"))
    self.assertNotEqual(Eq("b", "a"), Eq("b", "b"))

  def testAnd(self):
    self.assertEqual(TRUE, And([]))
    self.assertEqual(TRUE, And([TRUE]))
    self.assertEqual(TRUE, And([TRUE, TRUE]))
    self.assertEqual(FALSE, And([TRUE, FALSE]))
    self.assertEqual(Eq("a", "b"), And([Eq("a", "b"), TRUE]))
    self.assertEqual(FALSE, And([Eq("a", "b"), FALSE]))

  def testOr(self):
    self.assertEqual(FALSE, Or([]))
    self.assertEqual(TRUE, Or([TRUE]))
    self.assertEqual(TRUE, Or([TRUE, TRUE]))
    self.assertEqual(TRUE, Or([TRUE, FALSE]))
    self.assertEqual(Eq("a", "b"), Or([Eq("a", "b"), FALSE]))
    self.assertEqual(TRUE, Or([Eq("a", "b"), TRUE]))

  def testNestedEquals(self):
    eq1 = Eq("a", "u")
    eq2 = Eq("b", "v")
    eq3 = Eq("c", "w")
    eq4 = Eq("d", "x")
    nested = Or([And([eq1, eq2]), And([eq3, eq4])])
    self.assertEqual(nested, nested)

  def testOrder(self):
    eq1 = Eq("a", "b")
    eq2 = Eq("b", "c")
    self.assertEqual(Or([eq1, eq2]), Or([eq2, eq1]))
    self.assertEqual(And([eq1, eq2]), And([eq2, eq1]))

  def testHash(self):
    eq1 = Eq("a", "b")
    eq2 = Eq("b", "c")
    eq3 = Eq("c", "d")
    self.assertEqual(hash(Eq("x", "y")), hash(Eq("y", "x")))
    self.assertEqual(hash(Or([eq1, eq2, eq3])), hash(Or([eq2, eq3, eq1])))
    self.assertEqual(hash(And([eq1, eq2, eq3])), hash(And([eq2, eq3, eq1])))

  def testPivots(self):
    # x == 0 || x == 1
    equation = Or([Eq("x", "0"), Eq("x", "1")])
    self.assertItemsEqual(["0", "1"], equation.extract_pivots()["x"])

    # x == 0 && x == 0
    equation = And([Eq("x", "0"), Eq("x", "0")])
    self.assertItemsEqual(["0"], equation.extract_pivots()["x"])

    # x == 0 && (x == 0 || x == 1)
    equation = And([Eq("x", "0"), Or([Eq("x", "0"), Eq("x", "1")])])
    self.assertItemsEqual(["0"], equation.extract_pivots()["x"])

    # x == 0 || x == 0
    equation = And([Eq("x", "0"), Eq("x", "0")])
    self.assertItemsEqual(["0"], equation.extract_pivots()["x"])

  def testSimplify(self):
    # x == 0 || x == 1  with x in {0}
    equation = Or([Eq("x", "0"), Eq("x", "1")])
    values = {"x": {"0"}}
    self.assertEquals(Eq("x", "0"), equation.simplify(values))

    # x == 0 || x == 1  with x in {0}
    equation = Or([Eq("x", "0"), Eq("x", "1")])
    values = {"x": {"0", "1"}}
    self.assertEquals(equation, equation.simplify(values))

    # x == 0 with x in {1}
    equation = Eq("x", "0")
    values = {"x": {"1"}}
    self.assertEquals(FALSE, equation.simplify(values))

    # x == 0 with x in {0}
    equation = Eq("x", "0")
    values = {"x": {"0"}}
    self.assertEquals(equation, equation.simplify(values))

    # x == 0 && y == 0 with x in {1}, y in {1}
    equation = Or([Eq("x", "0"), Eq("y", "1")])
    values = {"x": {"1"}, "y": {"1"}}
    self.assertEquals(Eq("y", "1"), equation.simplify(values))

    # x == 0 && y == 0 with x in {0}, y in {1}
    equation = Or([Eq("x", "0"), Eq("y", "1")])
    values = {"x": {"0"}, "y": {"1"}}
    self.assertEquals(equation, equation.simplify(values))

    # x == 0 && x == 0 with x in {0}
    equation = And([Eq("x", "0"), Eq("x", "0")])
    values = {"x": {"0"}}
    self.assertEquals(Eq("x", "0"), equation.simplify(values))

    # x == y with x in {0, 1} and y in {1, 2}
    equation = Eq("x", "y")
    values = {"x": {"0", "1"}, "y": {"1", "2"}}
    self.assertEquals(And([Eq("x", "1"), Eq("y", "1")]),
                      equation.simplify(values))

  def _MakeSolver(self, variables=("x", "y")):
    solver = booleq.Solver()
    for variable in variables:
      solver.register_variable(variable)
    return solver

  def testGetFalseFirstApproximation(self):
    solver = self._MakeSolver(["x"])
    solver.implies(Eq("x", "1"), FALSE)
    self.assertDictEqual(solver._get_first_approximation(), {"x": set()})

  def testGetUnrelatedFirstApproximation(self):
    solver = self._MakeSolver()
    solver.implies(Eq("x", "1"), TRUE)
    solver.implies(Eq("y", "2"), TRUE)
    self.assertDictEqual(solver._get_first_approximation(),
                         {"x": {"1"}, "y": {"2"}})

  def testGetEqualFirstApproximation(self):
    solver = self._MakeSolver()
    solver.implies(Eq("x", "1"), Eq("x", "y"))
    assignments = solver._get_first_approximation()
    self.assertDictEqual(assignments,
                         {"x": {"1"}, "y": {"1"}})
    self.assertTrue(assignments["x"] is assignments["y"])

  def testGetMultipleEqualFirstApproximation(self):
    solver = self._MakeSolver(["x", "y", "z"])
    solver.implies(Eq("y", "1"), Eq("x", "y"))
    solver.implies(Eq("z", "2"), Eq("y", "z"))
    assignments = solver._get_first_approximation()
    self.assertDictEqual(assignments,
                         {"x": {"1", "2"},
                          "y": {"1", "2"},
                          "z": {"1", "2"}})
    self.assertTrue(assignments["x"] is assignments["y"])
    self.assertTrue(assignments["y"] is assignments["z"])

  def testImplication(self):
    solver = self._MakeSolver()
    solver.implies(Eq("x", "1"), Eq("y", "1"))
    solver.implies(Eq("x", "2"), FALSE)  # not Eq("x", "2")
    self.assertDictEqual(solver.solve(),
                         {"x": {"1"},
                          "y": {"1"}})

  def testGroundTruth(self):
    solver = self._MakeSolver()
    solver.implies(Eq("x", "1"), Eq("y", "1"))
    solver.always_true(Eq("x", "1"))
    self.assertDictEqual(solver.solve(),
                         {"x": {"1"},
                          "y": {"1"}})

  def testFilter(self):
    solver = self._MakeSolver(["x", "y"])
    solver.implies(Eq("x", "1"), TRUE)
    solver.implies(Eq("x", "2"), FALSE)
    solver.implies(Eq("x", "3"), FALSE)
    solver.implies(Eq("y", "1"), Or([Eq("x", "1"), Eq("x", "2"), Eq("x", "3")]))
    solver.implies(Eq("y", "2"), Or([Eq("x", "2"), Eq("x", "3")]))
    solver.implies(Eq("y", "3"), Or([Eq("x", "2")]))
    self.assertDictEqual(solver.solve(),
                         {"x": {"1"},
                          "y": {"1"}})

  def testSolveAnd(self):
    solver = self._MakeSolver(["x", "y", "z"])
    solver.always_true(Eq("x", "1"))
    solver.implies(Eq("y", "1"), And([Eq("x", "1"), Eq("z", "1")]))
    solver.implies(Eq("x", "1"), And([Eq("y", "1"), Eq("z", "1")]))
    solver.implies(Eq("z", "1"), And([Eq("x", "1"), Eq("y", "1")]))
    self.assertDictEqual(solver.solve(),
                         {"x": {"1"},
                          "y": {"1"},
                          "z": {"1"}})

  def testSolveTwice(self):
    solver = self._MakeSolver()
    solver.implies(Eq("x", "1"), Or([Eq("y", "1"), Eq("y", "2")]))
    solver.implies(Eq("y", "1"), FALSE)
    self.assertDictEqual(solver.solve(), solver.solve())

  def testChangeAfterSolve(self):
    solver = self._MakeSolver()
    solver.solve()
    self.assertRaises(AssertionError, solver.register_variable, "z")
    self.assertRaises(AssertionError, solver.implies, Eq("x", "1"), TRUE)

if __name__ == "__main__":
  unittest.main()
