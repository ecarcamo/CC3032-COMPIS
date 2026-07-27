from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text

    if op == '%':
      if not self.is_valid_modulo_operation(left_type, right_type):
        self.errors.append(f"Unsupported operand types for %: {left_type} and {right_type} (modulo requires int operands)")
      self.types[ctx] = IntType()
      return

    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterComparison(self, ctx: SimpleLangParser.ComparisonContext):
    pass

  def exitComparison(self, ctx: SimpleLangParser.ComparisonContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text
    if not self.is_valid_comparison_operation(left_type, right_type, op):
      reason = "" if op in ('==', '!=') else " (comparison requires numeric operands)"
      self.errors.append(f"Unsupported operand types for {op}: {left_type} and {right_type}{reason}")
    self.types[ctx] = BoolType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False

  def is_valid_modulo_operation(self, left_type, right_type):
    return isinstance(left_type, IntType) and isinstance(right_type, IntType)

  def is_valid_comparison_operation(self, left_type, right_type, op):
    is_numeric = lambda t: isinstance(t, (IntType, FloatType))
    if op in ('==', '!='):
      if is_numeric(left_type) and is_numeric(right_type):
        return True
      return type(left_type) == type(right_type)
    return is_numeric(left_type) and is_numeric(right_type)
