"""Solver for type equations."""

import logging

from pytype.pytd import booleq
from pytype.pytd import optimize
from pytype.pytd import pytd
from pytype.pytd import type_match
from pytype.pytd import utils as pytd_utils
from pytype.pytd.parse import visitors

log = logging.getLogger(__name__)

# How deep to nest type parameters
# TODO(kramm): Currently, the solver only generates variables for depth 1.
MAX_DEPTH = 1

is_unknown = type_match.is_unknown
is_partial = type_match.is_partial
is_complete = type_match.is_complete


class FlawedQuery(Exception):
  """Thrown if there is a fundamental flaw in the query."""
  pass


class TypeSolver(object):
  """Class for solving ~unknowns in type inference results."""

  def __init__(self, ast, builtins):
    self.ast = ast
    self.builtins = builtins

  def match_unknown_against_complete(self, matcher,
                                     solver, unknown, complete):
    """Given an ~unknown, match it against a class.

    Args:
      matcher: An instance of pytd.type_match.TypeMatch.
      solver: An instance of pytd.booleq.Solver.
      unknown: The unknown class to match
      complete: A complete class to match against. (E.g. a built-in or a user
        defined class)
    Returns:
      An instance of pytd.booleq.BooleanTerm.
    """

    assert is_unknown(unknown)
    assert is_complete(complete)
    type_params = {p.type_param: matcher.type_parameter(unknown, complete, p)
                   for p in complete.template}
    subst = type_params.copy()
    implication = matcher.match_Class_against_Class(unknown, complete, subst)
    if implication is not booleq.FALSE and type_params:
      # If we're matching against a templated class (E.g. list[T]), record the
      # fact that we'll also have to solve the type parameters.
      for param in type_params.values():
        solver.register_variable(param.name)
    solver.implies(booleq.Eq(unknown.name, complete.name), implication)

  def match_partial_against_complete(self, matcher, solver, partial, complete):
    """Match a partial class (call record) against a complete class.

    Args:
      matcher: An instance of pytd.type_match.TypeMatch.
      solver: An instance of pytd.booleq.Solver.
      partial: The partial class to match. The class name needs to be prefixed
        with "~" - the rest of the name is typically the same as complete.name.
      complete: A complete class to match against. (E.g. a built-in or a user
        defined class)
    Returns:
      An instance of pytd.booleq.BooleanTerm.
    Raises:
      FlawedQuery: If this call record is incompatible with the builtin.
    """
    assert is_partial(partial)
    assert is_complete(complete)
    # Types recorded for type parameters in the partial builtin are meaningless,
    # since we don't know which instance of the builtin used them when.
    subst = {p.type_param: pytd.AnythingType() for p in complete.template}
    formula = matcher.match_Class_against_Class(partial, complete, subst)
    if formula is booleq.FALSE:
      raise FlawedQuery("%s can never be %s" % (partial.name, complete.name))
    solver.always_true(formula)

  def match_call_record(self, matcher, solver, call_record, complete):
    """Match the record of a method call against the formal signature."""
    assert is_partial(call_record)
    assert is_complete(complete)
    formula = (
        matcher.match_Function_against_Function(call_record, complete, {}))
    if formula is booleq.FALSE:
      cartesian = call_record.Visit(optimize.ExpandSignatures())
      for signature in cartesian.signatures:
        formula = matcher.match_Signature_against_Function(
            signature, complete, {})
        if formula is booleq.FALSE:
          faulty_signature = pytd.Print(signature)
          break
      else:
        faulty_signature = ""
      raise FlawedQuery("Bad call %s%s" % (call_record.name, faulty_signature))
    solver.always_true(formula)

  def solve(self):
    """Solve the equations generated from the pytd.

    Returns:
      A dictionary (str->str), mapping unknown class names to known class names.
    Raises:
      AssertionError: If we detect an internal error.
    """
    hierarchy = type_match.get_all_subclasses([self.ast, self.builtins])
    factory = type_match.TypeMatch(hierarchy)
    solver = factory.solver

    unknown_classes = set()
    partial_classes = set()
    complete_classes = set()
    for cls in self.ast.classes:
      if is_unknown(cls):
        solver.register_variable(cls.name)
        unknown_classes.add(cls)
      elif is_partial(cls):
        partial_classes.add(cls)
      else:
        complete_classes.add(cls)

    for complete in complete_classes.union(self.builtins.classes):
      for unknown in unknown_classes:
        self.match_unknown_against_complete(factory, solver, unknown, complete)
      for partial in partial_classes:
        if type_match.unpack_name_of_partial(partial.name) == complete.name:
          self.match_partial_against_complete(
              factory, solver, partial, complete)

    partial_functions = set()
    complete_functions = set()
    for f in self.ast.functions:
      if is_partial(f):
        partial_functions.add(f)
      else:
        complete_functions.add(f)
    for partial in partial_functions:
      for complete in complete_functions.union(self.builtins.functions):
        if type_match.unpack_name_of_partial(partial.name) == complete.name:
          self.match_call_record(factory, solver, partial, complete)

    log.info("=========== Equations to solve =============\n%s", solver)
    log.info("=========== Equations to solve (end) =======")
    return solver.solve()


def solve(ast, builtins_pytd):
  """Solve the unknowns in a pytd AST using the standard Python builtins.

  Args:
    ast: A pytd.TypeDeclUnit, containing classes named ~unknownXX.
    builtins_pytd: A pytd for builtins.

  Returns:
    A tuple of (1) a dictionary (str->str) mapping unknown class names to known
    class names and (2) a pytd.TypeDeclUnit of the complete classes in ast.
  """
  builtins_pytd = pytd_utils.RemoveMutableParameters(builtins_pytd)
  builtins_pytd = visitors.LookupClasses(builtins_pytd, overwrite=True)
  ast = visitors.LookupClasses(ast, builtins_pytd, overwrite=True)
  ast.Visit(visitors.InPlaceFillInExternalTypes(builtins_pytd))
  return TypeSolver(ast, builtins_pytd).solve(), extract_local(ast)


def extract_local(ast):
  """Extract all classes that are not unknowns of call records of builtins."""
  return pytd.TypeDeclUnit(
      name=ast.name,
      classes=tuple(cls for cls in ast.classes if is_complete(cls)),
      functions=tuple(f for f in ast.functions if is_complete(f)),
      constants=tuple(c for c in ast.constants if is_complete(c)))


def convert_string_type(string_type, unknown, mapping, global_lookup, depth=0):
  """Convert a string representing a type back to a pytd type."""
  try:
    # Check whether this is a type declared in a pytd.
    cls = global_lookup.Lookup(string_type)
    base_type = pytd_utils.ExternalOrNamedOrClassType(cls.name, cls)
  except KeyError:
    # If we don't have a pytd for this type, it can't be a template.
    cls = None
    base_type = pytd_utils.ExternalOrNamedOrClassType(string_type, cls)

  if cls and cls.template:
    parameters = []
    for t in cls.template:
      type_param_name = unknown + "." + string_type + "." + t.name
      if type_param_name in mapping and depth < MAX_DEPTH:
        string_type_params = mapping[type_param_name]
        parameters.append(convert_string_type_list(
            string_type_params, unknown, mapping, global_lookup, depth + 1))
      else:
        parameters.append(pytd.AnythingType())
    if len(parameters) == 1:
      return pytd.HomogeneousContainerType(base_type, tuple(parameters))
    else:
      return pytd.GenericType(base_type, tuple(parameters))
  else:
    return base_type


def convert_string_type_list(types_as_string, unknown, mapping,
                             global_lookup, depth=0):
  """Like convert_string_type, but operate on a list."""
  if not types_as_string or booleq.Solver.ANY_VALUE in types_as_string:
    # If we didn't find a solution for a type (the list of matches is empty)
    # then report it as "?", not as "nothing", because the latter is confusing.
    return pytd.AnythingType()
  return pytd_utils.JoinTypes(convert_string_type(type_as_string, unknown,
                                                  mapping, global_lookup, depth)
                              for type_as_string in types_as_string)


def insert_solution(result, mapping, global_lookup):
  """Replace ~unknown types in a pytd with the actual (solved) types."""
  subst = {
      unknown: convert_string_type_list(types_as_strings, unknown,
                                        mapping, global_lookup)
      for unknown, types_as_strings in mapping.items()}
  result = result.Visit(optimize.RenameUnknowns(subst))
  # We remove duplicates here (even though Optimize does so again) because
  # it's much faster before the string types are replaced.
  result = result.Visit(optimize.RemoveDuplicates())
  return result.Visit(visitors.ReplaceTypes(subst))


def convert_pytd(ast, builtins_pytd):
  """Convert pytd with unknowns (structural types) to one with nominal types."""
  builtins_pytd = builtins_pytd.Visit(visitors.ClassTypeToNamedType())
  mapping, result = solve(ast, builtins_pytd)
  log_info_mapping(mapping)
  lookup = pytd_utils.Concat(builtins_pytd, result)
  result = insert_solution(result, mapping, lookup)
  if log.isEnabledFor(logging.INFO):
    log.info("=========== solve result =============\n%s", pytd.Print(result))
    log.info("=========== solve result (end) =============")
  return result


def log_info_mapping(mapping):
  """Print a raw type mapping. For debugging."""
  if log.isEnabledFor(logging.DEBUG):
    cutoff = 12
    log.debug("=========== (possible types) ===========")
    for unknown, possible_types in sorted(mapping.items()):
      assert isinstance(possible_types, (set, frozenset))
      if len(possible_types) > cutoff:
        log.debug("%s can be   %s, ... (total: %d)", unknown,
                  ", ".join(sorted(possible_types)[0:cutoff]),
                  len(possible_types))
      else:
        log.debug("%s can be %s", unknown,
                  ", ".join(sorted(possible_types)))
    log.debug("=========== (end of possible types) ===========")
