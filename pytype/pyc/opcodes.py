"""Opcode definitions for both Python 2 and Python 3."""

# We define all-uppercase classes, to match their opcode names:
# pylint: disable=invalid-name

HAS_CONST = 1  # references the constant table
HAS_NAME = 2  # references the name table
HAS_JREL = 4  # relative jump
HAS_JABS = 8  # absolute jump
HAS_JUNKNOWN = 16  # jumps to unknown location
HAS_LOCAL = 32  # references the varnames table
HAS_FREE = 64  # references "free variable" cells
HAS_NARGS = 128  # stores number of args + kwargs
HAS_ARGUMENT = 256  # all opcodes >= 90
NO_NEXT = 512  # doesn't execute the following opcode
STORE_JUMP = 1024  # only stores a jump, doesn't actually execute it
PUSHES_BLOCK = 2048  # starts a block (while, try, finally, with, etc.)
POPS_BLOCK = 4096  # ends a block


class Opcode(object):
  """An opcode without arguments."""

  __slots__ = ("line", "index", "prev", "next",
               "target", "block_target", "code")
  FLAGS = 0

  def __init__(self, index, line):
    self.index = index
    self.line = line
    self.target = None
    self.code = None  # If we have a CodeType or OrderedCode parent

  def __str__(self):
    return "%4d: %s" % (self.index, self.__class__.__name__)

  def __repr__(self):
    return self.__class__.__name__

  @property
  def name(self):
    return self.__class__.__name__

  @classmethod
  def has_const(cls):
    return bool(cls.FLAGS & HAS_CONST)

  @classmethod
  def has_name(cls):
    return bool(cls.FLAGS & HAS_NAME)

  @classmethod
  def has_jrel(cls):
    return bool(cls.FLAGS & HAS_JREL)

  @classmethod
  def has_jabs(cls):
    return bool(cls.FLAGS & HAS_JABS)

  @classmethod
  def has_junknown(cls):
    return bool(cls.FLAGS & HAS_JUNKNOWN)

  @classmethod
  def has_jump(cls):
    return bool(cls.FLAGS & (HAS_JREL | HAS_JABS | HAS_JUNKNOWN))

  @classmethod
  def has_local(cls):
    return bool(cls.FLAGS & HAS_LOCAL)

  @classmethod
  def has_free(cls):
    return bool(cls.FLAGS & HAS_FREE)

  @classmethod
  def has_nargs(cls):
    return bool(cls.FLAGS & HAS_NARGS)

  @classmethod
  def has_argument(cls):
    return bool(cls.FLAGS & HAS_ARGUMENT)

  @classmethod
  def no_next(cls):
    return bool(cls.FLAGS & NO_NEXT)

  @classmethod
  def carry_on_to_next(cls):
    return not cls.FLAGS & NO_NEXT

  @classmethod
  def store_jump(cls):
    return bool(cls.FLAGS & STORE_JUMP)

  @classmethod
  def does_jump(cls):
    return cls.has_jump() and not cls.store_jump()

  @classmethod
  def pushes_block(cls):
    return bool(cls.FLAGS & PUSHES_BLOCK)

  @classmethod
  def pops_block(cls):
    return bool(cls.FLAGS & POPS_BLOCK)

  @classmethod
  def has_arg(cls):
    return False


class OpcodeWithArg(Opcode):
  """An opcode with one argument."""

  __slots__ = ("arg", "pretty_arg")

  def __init__(self, index, line, arg, pretty_arg=None):
    super(OpcodeWithArg, self).__init__(index, line)
    self.arg = arg
    self.pretty_arg = pretty_arg

  def __str__(self):
    return "%4d: %s %s" % (self.index, self.__class__.__name__, self.arg)

  @classmethod
  def has_arg(cls):
    return True


class STOP_CODE(Opcode):
  __slots__ = ()
  FLAGS = NO_NEXT


class POP_TOP(Opcode):
  __slots__ = ()


class ROT_TWO(Opcode):
  __slots__ = ()


class ROT_THREE(Opcode):
  __slots__ = ()


class DUP_TOP(Opcode):
  __slots__ = ()


class ROT_FOUR(Opcode):
  __slots__ = ()


class DUP_TOP_TWO(Opcode):
  __slots__ = ()


class NOP(Opcode):
  __slots__ = ()


class UNARY_POSITIVE(Opcode):
  __slots__ = ()


class UNARY_NEGATIVE(Opcode):
  __slots__ = ()


class UNARY_NOT(Opcode):
  __slots__ = ()


class UNARY_CONVERT(Opcode):
  __slots__ = ()


class UNARY_INVERT(Opcode):
  __slots__ = ()


class BINARY_POWER(Opcode):
  __slots__ = ()


class BINARY_MULTIPLY(Opcode):
  __slots__ = ()


class BINARY_DIVIDE(Opcode):
  __slots__ = ()


class BINARY_MODULO(Opcode):
  __slots__ = ()


class BINARY_ADD(Opcode):
  __slots__ = ()


class BINARY_SUBTRACT(Opcode):
  __slots__ = ()


class BINARY_SUBSCR(Opcode):
  __slots__ = ()


class BINARY_FLOOR_DIVIDE(Opcode):
  __slots__ = ()


class BINARY_TRUE_DIVIDE(Opcode):
  __slots__ = ()


class INPLACE_FLOOR_DIVIDE(Opcode):
  __slots__ = ()


class INPLACE_TRUE_DIVIDE(Opcode):
  __slots__ = ()


class SLICE_0(Opcode):
  __slots__ = ()


class SLICE_1(Opcode):
  __slots__ = ()


class SLICE_2(Opcode):
  __slots__ = ()


class SLICE_3(Opcode):
  __slots__ = ()


class STORE_SLICE_0(Opcode):
  __slots__ = ()


class STORE_SLICE_1(Opcode):
  __slots__ = ()


class STORE_SLICE_2(Opcode):
  __slots__ = ()


class STORE_SLICE_3(Opcode):
  __slots__ = ()


class DELETE_SLICE_0(Opcode):
  __slots__ = ()


class DELETE_SLICE_1(Opcode):
  __slots__ = ()


class DELETE_SLICE_2(Opcode):
  __slots__ = ()


class DELETE_SLICE_3(Opcode):
  __slots__ = ()


class STORE_MAP(Opcode):
  __slots__ = ()


class INPLACE_ADD(Opcode):
  __slots__ = ()


class INPLACE_SUBTRACT(Opcode):
  __slots__ = ()


class INPLACE_MULTIPLY(Opcode):
  __slots__ = ()


class INPLACE_DIVIDE(Opcode):
  __slots__ = ()


class INPLACE_MODULO(Opcode):
  __slots__ = ()


class STORE_SUBSCR(Opcode):
  __slots__ = ()


class DELETE_SUBSCR(Opcode):
  __slots__ = ()


class BINARY_LSHIFT(Opcode):
  __slots__ = ()


class BINARY_RSHIFT(Opcode):
  __slots__ = ()


class BINARY_AND(Opcode):
  __slots__ = ()


class BINARY_XOR(Opcode):
  __slots__ = ()


class BINARY_OR(Opcode):
  __slots__ = ()


class INPLACE_POWER(Opcode):
  __slots__ = ()


class GET_ITER(Opcode):
  __slots__ = ()


class STORE_LOCALS(Opcode):
  __slots__ = ()


class PRINT_EXPR(Opcode):
  __slots__ = ()


class PRINT_ITEM(Opcode):
  __slots__ = ()


class PRINT_NEWLINE(Opcode):
  __slots__ = ()


class PRINT_ITEM_TO(Opcode):
  __slots__ = ()


class PRINT_NEWLINE_TO(Opcode):
  __slots__ = ()


class LOAD_BUILD_CLASS(Opcode):
  __slots__ = ()


class YIELD_FROM(Opcode):
  FLAGS = HAS_JUNKNOWN
  __slots__ = ()


class INPLACE_LSHIFT(Opcode):
  __slots__ = ()


class INPLACE_RSHIFT(Opcode):
  __slots__ = ()


class INPLACE_AND(Opcode):
  __slots__ = ()


class INPLACE_XOR(Opcode):
  __slots__ = ()


class INPLACE_OR(Opcode):
  __slots__ = ()


class BREAK_LOOP(Opcode):
  FLAGS = HAS_JUNKNOWN | NO_NEXT
  __slots__ = ()


class WITH_CLEANUP(Opcode):
  # This opcode changes the block stack, but it should never change its depth.
  FLAGS = HAS_JUNKNOWN  # might call __exit__
  __slots__ = ()


class LOAD_LOCALS(Opcode):
  __slots__ = ()


class RETURN_VALUE(Opcode):
  FLAGS = HAS_JUNKNOWN | NO_NEXT
  __slots__ = ()


class IMPORT_STAR(Opcode):
  __slots__ = ()


class EXEC_STMT(Opcode):
  FLAGS = HAS_JUNKNOWN
  __slots__ = ()


class YIELD_VALUE(Opcode):
  FLAGS = HAS_JUNKNOWN
  __slots__ = ()


class POP_BLOCK(Opcode):
  FLAGS = POPS_BLOCK
  __slots__ = ()


class END_FINALLY(Opcode):
  FLAGS = HAS_JUNKNOWN  # might re-raise an exception
  __slots__ = ()


class BUILD_CLASS(Opcode):
  __slots__ = ()


class POP_EXCEPT(Opcode):
  __slots__ = ()


class STORE_NAME(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class DELETE_NAME(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class UNPACK_SEQUENCE(OpcodeWithArg):  # Arg: Number of tuple items
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class FOR_ITER(OpcodeWithArg):
  FLAGS = HAS_JREL|HAS_ARGUMENT
  __slots__ = ()


class LIST_APPEND(OpcodeWithArg):
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class UNPACK_EX(OpcodeWithArg):
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class STORE_ATTR(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class DELETE_ATTR(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class STORE_GLOBAL(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class DELETE_GLOBAL(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class DUP_TOPX(OpcodeWithArg):  # Arg: Number of items to duplicate
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class LOAD_CONST(OpcodeWithArg):  # Arg: Index in const list
  FLAGS = HAS_ARGUMENT|HAS_CONST
  __slots__ = ()


class LOAD_NAME(OpcodeWithArg):  # Arg: Index in name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class BUILD_TUPLE(OpcodeWithArg):  # Arg: Number of tuple items
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class BUILD_LIST(OpcodeWithArg):  # Arg: Number of list items
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class BUILD_SET(OpcodeWithArg):  # Arg: Number of set items
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class BUILD_MAP(OpcodeWithArg):  # Arg: Number of dict entries (up to 255)
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class LOAD_ATTR(OpcodeWithArg):  # Arg: Index in name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class COMPARE_OP(OpcodeWithArg):  # Arg: Comparison operator
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class IMPORT_NAME(OpcodeWithArg):  # Arg: Index in name list
  FLAGS = HAS_NAME|HAS_ARGUMENT|HAS_JUNKNOWN
  __slots__ = ()


class IMPORT_FROM(OpcodeWithArg):  # Arg: Index in name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class JUMP_FORWARD(OpcodeWithArg):
  FLAGS = HAS_JREL|HAS_ARGUMENT|NO_NEXT
  __slots__ = ()


class JUMP_IF_FALSE_OR_POP(OpcodeWithArg):
  FLAGS = HAS_JABS|HAS_ARGUMENT
  __slots__ = ()


class JUMP_IF_TRUE_OR_POP(OpcodeWithArg):
  FLAGS = HAS_JABS|HAS_ARGUMENT
  __slots__ = ()


class JUMP_ABSOLUTE(OpcodeWithArg):
  FLAGS = HAS_JABS|HAS_ARGUMENT|NO_NEXT
  __slots__ = ()


class POP_JUMP_IF_FALSE(OpcodeWithArg):
  FLAGS = HAS_JABS|HAS_ARGUMENT
  __slots__ = ()


class POP_JUMP_IF_TRUE(OpcodeWithArg):
  FLAGS = HAS_JABS|HAS_ARGUMENT
  __slots__ = ()


class LOAD_GLOBAL(OpcodeWithArg):  # Indexes into name list
  FLAGS = HAS_NAME|HAS_ARGUMENT
  __slots__ = ()


class CONTINUE_LOOP(OpcodeWithArg):  # Acts as jump
  FLAGS = HAS_JABS|HAS_ARGUMENT|NO_NEXT
  __slots__ = ()


class SETUP_LOOP(OpcodeWithArg):
  FLAGS = HAS_JREL|HAS_ARGUMENT|STORE_JUMP|PUSHES_BLOCK
  __slots__ = ()


class SETUP_EXCEPT(OpcodeWithArg):
  FLAGS = HAS_JREL|HAS_ARGUMENT|STORE_JUMP|PUSHES_BLOCK
  __slots__ = ()


class SETUP_FINALLY(OpcodeWithArg):
  FLAGS = HAS_JREL|HAS_ARGUMENT|STORE_JUMP|PUSHES_BLOCK
  __slots__ = ()


class LOAD_FAST(OpcodeWithArg):  # Loads local variable number
  FLAGS = HAS_LOCAL|HAS_ARGUMENT
  __slots__ = ()


class STORE_FAST(OpcodeWithArg):  # Stores local variable number
  FLAGS = HAS_LOCAL|HAS_ARGUMENT
  __slots__ = ()


class DELETE_FAST(OpcodeWithArg):  # Deletes local variable number
  FLAGS = HAS_LOCAL|HAS_ARGUMENT
  __slots__ = ()


class RAISE_VARARGS(OpcodeWithArg):  # Arg: Number of raise args (1, 2, or 3)
  FLAGS = HAS_ARGUMENT|HAS_JUNKNOWN|NO_NEXT
  __slots__ = ()


class CALL_FUNCTION(OpcodeWithArg):  # Arg: #args + (#kwargs << 8)
  FLAGS = HAS_NARGS|HAS_ARGUMENT|HAS_JUNKNOWN
  __slots__ = ()


class MAKE_FUNCTION(OpcodeWithArg):  # Arg: Number of args with default values
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class BUILD_SLICE(OpcodeWithArg):  # Arg: Number of items
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class MAKE_CLOSURE(OpcodeWithArg):
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class LOAD_CLOSURE(OpcodeWithArg):
  FLAGS = HAS_FREE|HAS_ARGUMENT
  __slots__ = ()


class LOAD_DEREF(OpcodeWithArg):
  FLAGS = HAS_FREE|HAS_ARGUMENT
  __slots__ = ()


class STORE_DEREF(OpcodeWithArg):
  FLAGS = HAS_FREE|HAS_ARGUMENT
  __slots__ = ()


class DELETE_DEREF(OpcodeWithArg):
  FLAGS = HAS_FREE|HAS_ARGUMENT
  __slots__ = ()


class CALL_FUNCTION_VAR(OpcodeWithArg):  # Arg: #args + (#kwargs << 8)
  FLAGS = HAS_NARGS|HAS_ARGUMENT|HAS_JUNKNOWN
  __slots__ = ()


class CALL_FUNCTION_KW(OpcodeWithArg):  # Arg: #args + (#kwargs << 8)
  FLAGS = HAS_NARGS|HAS_ARGUMENT|HAS_JUNKNOWN
  __slots__ = ()


class CALL_FUNCTION_VAR_KW(OpcodeWithArg):  # Arg: #args + (#kwargs << 8)
  FLAGS = HAS_NARGS|HAS_ARGUMENT|HAS_JUNKNOWN
  __slots__ = ()


class SETUP_WITH(OpcodeWithArg):
  FLAGS = HAS_JREL|HAS_ARGUMENT|STORE_JUMP|PUSHES_BLOCK
  __slots__ = ()


class EXTENDED_ARG(OpcodeWithArg):
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class SET_ADD(OpcodeWithArg):
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class MAP_ADD(OpcodeWithArg):
  FLAGS = HAS_ARGUMENT
  __slots__ = ()


class LOAD_CLASSDEREF(OpcodeWithArg):
  FLAGS = HAS_FREE|HAS_ARGUMENT
  __slots__ = ()


python2_mapping = {
    0: STOP_CODE,  # removed in Python 3
    1: POP_TOP,
    2: ROT_TWO,
    3: ROT_THREE,
    4: DUP_TOP,
    5: ROT_FOUR,  # becomes DUP_TOP_TWO in Python 3
    9: NOP,
    10: UNARY_POSITIVE,
    11: UNARY_NEGATIVE,
    12: UNARY_NOT,
    13: UNARY_CONVERT,  # removed in Python 3
    15: UNARY_INVERT,
    19: BINARY_POWER,
    20: BINARY_MULTIPLY,
    21: BINARY_DIVIDE,  # removed in Python 3
    22: BINARY_MODULO,
    23: BINARY_ADD,
    24: BINARY_SUBTRACT,
    25: BINARY_SUBSCR,
    26: BINARY_FLOOR_DIVIDE,
    27: BINARY_TRUE_DIVIDE,
    28: INPLACE_FLOOR_DIVIDE,
    29: INPLACE_TRUE_DIVIDE,
    30: SLICE_0,  # removed in Python 3
    31: SLICE_1,  # removed in Python 3
    32: SLICE_2,  # removed in Python 3
    33: SLICE_3,  # removed in Python 3
    40: STORE_SLICE_0,  # removed in Python 3
    41: STORE_SLICE_1,  # removed in Python 3
    42: STORE_SLICE_2,  # removed in Python 3
    43: STORE_SLICE_3,  # removed in Python 3
    50: DELETE_SLICE_0,  # removed in Python 3
    51: DELETE_SLICE_1,  # removed in Python 3
    52: DELETE_SLICE_2,  # removed in Python 3
    53: DELETE_SLICE_3,  # removed in Python 3
    54: STORE_MAP,
    55: INPLACE_ADD,
    56: INPLACE_SUBTRACT,
    57: INPLACE_MULTIPLY,
    58: INPLACE_DIVIDE,  # removed in Python 3
    59: INPLACE_MODULO,
    60: STORE_SUBSCR,
    61: DELETE_SUBSCR,
    62: BINARY_LSHIFT,
    63: BINARY_RSHIFT,
    64: BINARY_AND,
    65: BINARY_XOR,
    66: BINARY_OR,
    67: INPLACE_POWER,
    68: GET_ITER,
    70: PRINT_EXPR,
    71: PRINT_ITEM,  # becomes LOAD_BUILD_CLASS in Python 3
    72: PRINT_NEWLINE,  # becomes YIELD_FROM in Python 3
    73: PRINT_ITEM_TO,
    74: PRINT_NEWLINE_TO,
    75: INPLACE_LSHIFT,
    76: INPLACE_RSHIFT,
    77: INPLACE_AND,
    78: INPLACE_XOR,
    79: INPLACE_OR,
    80: BREAK_LOOP,
    81: WITH_CLEANUP,
    82: LOAD_LOCALS,  # removed in Python 3
    83: RETURN_VALUE,
    84: IMPORT_STAR,
    85: EXEC_STMT,  # removed in Python 3
    86: YIELD_VALUE,
    87: POP_BLOCK,
    88: END_FINALLY,
    89: BUILD_CLASS,  # becomes POP_EXCEPT in Python 3
    90: STORE_NAME,
    91: DELETE_NAME,
    92: UNPACK_SEQUENCE,
    93: FOR_ITER,
    94: LIST_APPEND,  # becomes UNPACK_EX in Python 3
    95: STORE_ATTR,
    96: DELETE_ATTR,
    97: STORE_GLOBAL,
    98: DELETE_GLOBAL,
    99: DUP_TOPX,  # removed in Python 3
    100: LOAD_CONST,
    101: LOAD_NAME,
    102: BUILD_TUPLE,
    103: BUILD_LIST,
    104: BUILD_SET,
    105: BUILD_MAP,
    106: LOAD_ATTR,
    107: COMPARE_OP,
    108: IMPORT_NAME,
    109: IMPORT_FROM,
    110: JUMP_FORWARD,
    111: JUMP_IF_FALSE_OR_POP,
    112: JUMP_IF_TRUE_OR_POP,
    113: JUMP_ABSOLUTE,
    114: POP_JUMP_IF_FALSE,
    115: POP_JUMP_IF_TRUE,
    116: LOAD_GLOBAL,
    119: CONTINUE_LOOP,
    120: SETUP_LOOP,
    121: SETUP_EXCEPT,
    122: SETUP_FINALLY,
    124: LOAD_FAST,
    125: STORE_FAST,
    126: DELETE_FAST,
    130: RAISE_VARARGS,
    131: CALL_FUNCTION,
    132: MAKE_FUNCTION,
    133: BUILD_SLICE,
    134: MAKE_CLOSURE,
    135: LOAD_CLOSURE,
    136: LOAD_DEREF,
    137: STORE_DEREF,
    140: CALL_FUNCTION_VAR,
    141: CALL_FUNCTION_KW,
    142: CALL_FUNCTION_VAR_KW,
    143: SETUP_WITH,
    145: EXTENDED_ARG,  # moved to 144 in Python 3, 145 becomes LIST_APPEND
    146: SET_ADD,
    147: MAP_ADD,
}

python3_mapping = {
    1: POP_TOP,
    2: ROT_TWO,
    3: ROT_THREE,
    4: DUP_TOP,
    5: DUP_TOP_TWO,
    9: NOP,
    10: UNARY_POSITIVE,
    11: UNARY_NEGATIVE,
    12: UNARY_NOT,
    15: UNARY_INVERT,
    19: BINARY_POWER,
    20: BINARY_MULTIPLY,
    22: BINARY_MODULO,
    23: BINARY_ADD,
    24: BINARY_SUBTRACT,
    25: BINARY_SUBSCR,
    26: BINARY_FLOOR_DIVIDE,
    27: BINARY_TRUE_DIVIDE,
    28: INPLACE_FLOOR_DIVIDE,
    29: INPLACE_TRUE_DIVIDE,
    54: STORE_MAP,
    55: INPLACE_ADD,
    56: INPLACE_SUBTRACT,
    57: INPLACE_MULTIPLY,
    59: INPLACE_MODULO,
    60: STORE_SUBSCR,
    61: DELETE_SUBSCR,
    62: BINARY_LSHIFT,
    63: BINARY_RSHIFT,
    64: BINARY_AND,
    65: BINARY_XOR,
    66: BINARY_OR,
    67: INPLACE_POWER,
    68: GET_ITER,
    69: STORE_LOCALS,  # removed again in Python 3.4
    70: PRINT_EXPR,
    71: LOAD_BUILD_CLASS,  # PRINT_ITEM in Python 2
    72: YIELD_FROM,  # PRINT_NEWLINE in Python 2
    75: INPLACE_LSHIFT,
    76: INPLACE_RSHIFT,
    77: INPLACE_AND,
    78: INPLACE_XOR,
    79: INPLACE_OR,
    80: BREAK_LOOP,
    81: WITH_CLEANUP,
    83: RETURN_VALUE,
    84: IMPORT_STAR,
    86: YIELD_VALUE,
    87: POP_BLOCK,
    88: END_FINALLY,
    89: POP_EXCEPT,  # BUILD_CLASS in Python 2
    90: STORE_NAME,
    91: DELETE_NAME,
    92: UNPACK_SEQUENCE,
    93: FOR_ITER,
    94: UNPACK_EX,  # LIST_APPEND in Python 2
    95: STORE_ATTR,
    96: DELETE_ATTR,
    97: STORE_GLOBAL,
    98: DELETE_GLOBAL,
    100: LOAD_CONST,
    101: LOAD_NAME,
    102: BUILD_TUPLE,
    103: BUILD_LIST,
    104: BUILD_SET,
    105: BUILD_MAP,
    106: LOAD_ATTR,
    107: COMPARE_OP,
    108: IMPORT_NAME,
    109: IMPORT_FROM,
    110: JUMP_FORWARD,
    111: JUMP_IF_FALSE_OR_POP,
    112: JUMP_IF_TRUE_OR_POP,
    113: JUMP_ABSOLUTE,
    114: POP_JUMP_IF_FALSE,
    115: POP_JUMP_IF_TRUE,
    116: LOAD_GLOBAL,
    119: CONTINUE_LOOP,
    120: SETUP_LOOP,
    121: SETUP_EXCEPT,
    122: SETUP_FINALLY,
    124: LOAD_FAST,
    125: STORE_FAST,
    126: DELETE_FAST,
    130: RAISE_VARARGS,
    131: CALL_FUNCTION,
    132: MAKE_FUNCTION,
    133: BUILD_SLICE,
    134: MAKE_CLOSURE,
    135: LOAD_CLOSURE,
    136: LOAD_DEREF,
    137: STORE_DEREF,
    138: DELETE_DEREF,
    140: CALL_FUNCTION_VAR,
    141: CALL_FUNCTION_KW,
    142: CALL_FUNCTION_VAR_KW,
    143: SETUP_WITH,
    144: EXTENDED_ARG,  # 145 in Python 2
    145: LIST_APPEND,  # 94 in Python 2
    146: SET_ADD,
    147: MAP_ADD,
    148: LOAD_CLASSDEREF,  # not in Python 2
}


class _LineNumberTableParser(object):
  """State machine for decoding a Python line number array."""

  def __init__(self, lnotab, firstlineno):
    assert not len(lnotab) & 1  # lnotab always has an even number of elements
    self.lnotab = lnotab
    self.lineno = firstlineno
    self.next_addr = ord(self.lnotab[0]) if self.lnotab else 0
    self.pos = 0

  def get(self, i):
    """Get the line number for the instruction at the given position.

    This does NOT allow random access. Call with incremental numbers.

    Args:
      i: The byte position in the bytecode. i needs to stay constant or increase
        between calls.

    Returns:
      The line number corresponding to the position at i.
    """
    while i >= self.next_addr and self.pos < len(self.lnotab):
      self.lineno += ord(self.lnotab[self.pos + 1])
      self.pos += 2
      if self.pos < len(self.lnotab):
        self.next_addr += ord(self.lnotab[self.pos])
    return self.lineno


def _prettyprint_arg(cls, oparg, co_consts, co_names,
                     co_varnames, cellvars_freevars):
  if cls.has_jrel():
    return oparg
  elif co_consts and cls.has_const():
    return repr(co_consts[oparg])
  elif co_names and cls.has_name():
    return co_names[oparg]
  elif co_varnames and cls.has_local():
    return co_varnames[oparg]
  elif cellvars_freevars and cls.has_free():
    return cellvars_freevars[oparg]
  else:
    return oparg


def _dis(data, mapping,
         co_varnames=None, co_names=None, co_consts=None, co_cellvars=None,
         co_freevars=None, co_lnotab=None, co_firstlineno=None):
  """Disassemble a string into a list of Opcode instances."""
  code = []
  size = len(data)
  pos = 0
  lp = _LineNumberTableParser(co_lnotab, co_firstlineno) if co_lnotab else None
  offset_to_index = {}
  extended_arg = 0
  if co_cellvars is not None and co_freevars is not None:
    cellvars_freevars = co_cellvars + co_freevars
  else:
    cellvars_freevars = None
  while pos < size:
    opcode = ord(data[pos])
    index = len(code)
    offset_to_index[pos] = index
    if lp:
      line = lp.get(pos)
    else:
      # single line programs don't have co_lnotab
      line = co_firstlineno
    pos += 1
    cls = mapping[opcode]
    if cls is EXTENDED_ARG:
      # EXTENDED_ARG modifies the opcode after it, setting bits 16..31 of
      # its argument.
      assert not extended_arg, "two EXTENDED_ARGs in a row"
      extended_arg = ord(data[pos]) << 16 | ord(data[pos+1]) << 24
    elif cls.FLAGS & HAS_ARGUMENT:
      oparg = ord(data[pos]) | ord(data[pos+1]) << 8 | extended_arg
      extended_arg = 0
      pos += 2
      if cls.has_jrel():
        oparg += pos
      pretty = _prettyprint_arg(cls, oparg, co_consts, co_names, co_varnames,
                                cellvars_freevars)
      code.append(cls(index, line, oparg, pretty))
    else:
      assert not extended_arg, "EXTENDED_ARG in front of opcode without arg"
      code.append(cls(index, line))

  # Map the target of jump instructions to the opcode they jump to, and fill
  # in "next" and "prev" pointers
  for i, op in enumerate(code):
    if op.FLAGS & (HAS_JREL | HAS_JABS):
      op.arg = op.pretty_arg = offset_to_index[op.arg]
      op.target = code[op.arg]
    op.prev = code[i - 1] if i > 0 else None
    op.next = code[i + 1] if i < len(code) - 1 else None
  return code


def dis(data, python_version, *args, **kwargs):
  assert python_version[0] in (2, 3)
  mapping = python2_mapping if python_version[0] == 2 else python3_mapping
  return _dis(data, mapping, *args, **kwargs)


def dis_code(code):
  return dis(data=code.co_code,
             python_version=code.python_version,
             co_varnames=code.co_varnames,
             co_names=code.co_names,
             co_consts=code.co_consts,
             co_cellvars=code.co_cellvars,
             co_freevars=code.co_freevars,
             co_lnotab=code.co_lnotab,
             co_firstlineno=code.co_firstlineno)

