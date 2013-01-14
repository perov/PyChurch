import utils.rrandom as rrandom 
import utils.rhash as rhash
from utils.rexceptions import RException
import math

# transition // for inference on theta, the internal randomness generated during init
# marg (scoring total probability of all applications);
# propose (re-propose a particular application)


# class XRP:
#   def __init__(self, initargs):
#     #self.deterministic = False
#     #self.initargs = initargs
#     #self.state = None
#     raise RException("Not implemented")
#   def transition(self, args, vals, theta, initargs):
#     raise RException("Not implemented")
#   def joint(args, vals, state, initargs, theta):
#     raise RException("Not implemented")
#   def mhprop(args, oldval, state, initargs, theta)
#     # returns newval, q->, q-<
#     raise RException("Not implemented")
#   def __str__(self):
#     return 'XRP'

class XRP:
  def __init__(self):
    self.deterministic = False
    return
  def apply(self, args = None):
    raise RException("Not implemented")
  def incorporate(self, val, args = None):
    pass
  def remove(self, val, args = None):
    pass
  ## SHOULD RETURN THE LOG PROBABILITY
  def prob(self, val, args = None):
    return 0
  def __str__(self):
    return 'XRP'
  def mhprop(args, oldval, state, initargs, theta):
    # TODO
    pass
    # returns newval, q->, q-<
  def load_from_unweighted_XRP(self):
    # TODO
    pass
  def is_mem_proc(self):
    return False
  def is_mem(self):
    return False

class unweighted_XRP:
  def __init__(self):
    self.deterministic = False
    return
  def apply(self, args = None):
    raise RException("Not implemented")
  def incorporate(self, val, args = None):
    pass
  def remove(self, val, args = None):
    pass
  ## SHOULD RETURN THE LOG PROBABILITY
  def prob(self, val, args = None):
    return 0
  def is_mem_proc(self):
    return False
  def is_mem(self):
    return False
  def __str__(self):
    return 'XRP'
  def mhprop(args, oldval, state, initargs, theta):
    # TODO
    pass
    # returns newval, q->, q-<

class Value:
  def initialize(self):
    # dummy values to prevent RPython typer from complaining
    self.bool = False
    self.num = 0.0 
    self.int = 0 
    self.nat = 0 
    self.xrp = XRP()
    self.vars = ['']
    self.body = None
    self.env = None
  def __hash__(self):
    raise RException("Invalid operation")
  def __repr__(self):
    return self.__str__()
  def __eq__(self, other):
    return BoolValue(self is other)
  def __gt__(self, other):
    raise RException("Invalid operation")
  def __lt__(self, other):
    raise RException("Invalid operation")
  def __ge__(self, other):
    raise RException("Invalid operation")
  def __le__(self, other):
    raise RException("Invalid operation")
  def __add__(self, other):
    raise RException("Invalid operation")
  def __sub__(self, other):
    raise RException("Invalid operation")
  def __mul__(self, other):
    raise RException("Invalid operation")
  def __div__(self, other):
    raise RException("Invalid operation")
  def __pow__(self, other):
    raise RException("Invalid operation")
  def __mod__(self, other):
    raise RException("Invalid operation")
  def __and__(self, other):
    raise RException("Invalid operation")
  def __or__(self, other):
    raise RException("Invalid operation")
  def __xor__(self, other):
    raise RException("Invalid operation")
  def __inv__(self):
    raise RException("Invalid operation")
  def __abs__(self):
    raise RException("Invalid operation")
  def __int__(self):
    raise RException("Invalid operation")
  def __round__(self):
    raise RException("Invalid operation")
  def __floor__(self):
    raise RException("Invalid operation")
  def __ceil__(self):
    raise RException("Invalid operation")
  def __nonzero__(self):
    return BoolValue((self.num > 0))
  pass 

class Procedure(Value):
  def __init__(self, vars, body, env):
    self.initialize()
    self.type = 'procedure'
    self.vars = vars
    self.body = body
    self.env = env 
    self.hash = rrandom.random.randbelow()
    self.str_hash = str(self.hash)
  def __str__(self):
    return '(lambda %s : %s)' % (str(self.vars), str(self.body))
  def __hash__(self):
    return self.hash
  def __eq__(self, other):
    return BoolValue((self.type == other.type) and (self.hash == other.hash))

class XRPValue(Value):
  def __init__(self, xrp):
    self.initialize()
    self.type = 'xrp'
    self.xrp = xrp 
    self.hash = rrandom.random.randbelow()
    self.str_hash = str(self.hash)
  def __str__(self):
    return 'xrp %s' % (str(self.xrp)) 
  def __hash__(self):
    return self.hash
  def __eq__(self, other):
    return BoolValue((self.type == other.type) and (self.hash == other.hash))

class BoolValue(Value):
  def __init__(self, bool):
    self.initialize()
    self.type = 'bool'
    self.bool = bool 
    self.str_hash = ("true" if self.bool else "false")
  def __str__(self):
    return str(self.bool)
  def __hash__(self):
    return (1 if self.bool else 0)
  def __eq__(self, other):
    return BoolValue((self.type == other.type) and (self.bool == other.bool))
  def __and__(self, other):
    return BoolValue(self.bool and other.bool)
  def __or__(self, other):
    return BoolValue(self.bool or other.bool)
  def __xor__(self, other):
    return BoolValue(self.bool ^ other.bool)
  def __inv__(self):
    return BoolValue(not self.bool)
  def __nonzero__(self):
    return self.bool

# TODO: use this?
def MakeNumValue(val):
  if int(val) == val:
    if val >= 0:
      return NatValue(val)
    else:
      return IntValue(val)
  else:
    return NumValue(val)

class NumValue(Value):
  def __init__(self, num):
    self.initialize()
    self.type = 'num'
    self.num = num
    self.str_hash = str(self.num)
  def __str__(self):
    return str(self.num)
  def __hash__(self):
    return rhash.hash_float(self.num)
  def __eq__(self, other):
    return BoolValue((self.type == other.type) and (self.num == other.num))
  def __gt__(self, other):
    if other.type not in ['num', 'int', 'nat']:
      raise RException("Invalid comparison")
    return BoolValue((self.num > other.num))
  def __ge__(self, other):
    if other.type not in ['num', 'int', 'nat']:
      raise RException("Invalid comparison")
    return BoolValue((self.num >= other.num))
  def __lt__(self, other):
    if other.type not in ['num', 'int', 'nat']:
      raise RException("Invalid comparison")
    return BoolValue((self.num < other.num))
  def __le__(self, other):
    if other.type not in ['num', 'int', 'nat']:
      raise RException("Invalid comparison")
    return BoolValue((self.num <= other.num))
  def __add__(self, other):
    return NumValue(self.num + other.num)
  def __sub__(self, other):
    return NumValue(self.num - other.num)
  def __mul__(self, other):
    return NumValue(self.num * other.num)
  def __div__(self, other):
    return NumValue(self.num / (other.num + 0.0))
  def __pow__(self, other):
    return NumValue(math.pow(self.num, other.num))
  def __inv__(self):
    return NumValue(- self.num)
  def __abs__(self):
    return NumValue(abs(self.num))
  #def __mod__(self, other):
  #  return NumValue(self.num % other.nat)
  def __int__(self): # round towards zero
    val = int(self.num)
    if val < 0:
      return IntValue(val)
    else:
      return NatValue(val)
  def __round__(self): # round to nearest
    if self.num <= -0.5:
      return IntValue(int(self.num - 0.5))
    elif self.num >= 0:
      return NatValue(int(self.num + 0.5))
    else:
      return NatValue(0)
  def __floor__(self):
    val = int(math.floor(self.num))
    if val < 0:
      return IntValue(val)
    else:
      return NatValue(val)
  def __ceil__(self):
    val = int(math.ceil(self.num))
    if val < 0:
      return IntValue(val)
    else:
      return NatValue(val)

  def __nonzero__(self):
    return BoolValue((self.num > 0))

class IntValue(NumValue):
  def __init__(self, num):
    self.initialize()
    self.type = 'int'
    self.int = num
    self.num = num
    self.str_hash = str(self.int)
  def __hash__(self):
    return self.int
  def __add__(self, other):
    if other.type == 'int' or other.type == 'nat':
      intval = self.int + other.int
      if intval < 0:
        return IntValue(intval)
      else:
        return NatValue(intval)
    else:
      return NumValue(self.num + other.num)
  def __sub__(self, other):
    if other.type == 'int' or other.type == 'nat':
      intval = self.int - other.int
      if intval < 0:
        return IntValue(intval)
      else:
        return NatValue(intval)
    else:
      return NumValue(self.num - other.num)
  def __mul__(self, other):
    if other.type == 'int' or other.type == 'nat':
      intval = self.int * other.int
      if intval < 0:
        return IntValue(intval)
      else:
        return NatValue(intval)
    else:
      return NumValue(self.num * other.num)
  def __pow__(self, other):
    if other.type == 'nat':
      intval = 1
      for i in range(other.int):
        intval = intval * self.int
      if intval < 0:
        return IntValue(intval)
      else:
        return NatValue(intval)
    else:
      return NumValue(math.pow(self.num, other.num))
  def __mod__(self, other):
    return NatValue(self.int % other.nat)
  def __abs__(self):
    return NatValue(abs(self.int))
  def __inv__(self):
    return IntValue(- self.int)

  
class NatValue(IntValue):
  def __init__(self, num):
    self.initialize()
    self.type = 'nat'
    self.nat = num
    self.int = num
    self.num = num
    self.str_hash = str(self.int)

