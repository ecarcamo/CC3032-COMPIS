from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text

    if op == '%':
        if isinstance(left_type, IntType) and isinstance(right_type, IntType):
            return IntType()
        else:
            raise TypeError("Unsupported operand types for %: {} and {} (modulo requires int operands)".format(left_type, right_type))

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for * or /: {} and {}".format(left_type, right_type))

  def visitComparison(self, ctx: SimpleLangParser.ComparisonContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text
    is_numeric = lambda t: isinstance(t, (IntType, FloatType))

    if op in ('==', '!='):
        if (is_numeric(left_type) and is_numeric(right_type)) or type(left_type) == type(right_type):
            return BoolType()
        else:
            raise TypeError("Unsupported operand types for {}: {} and {}".format(op, left_type, right_type))
    else:
        if is_numeric(left_type) and is_numeric(right_type):
            return BoolType()
        else:
            raise TypeError("Unsupported operand types for {}: {} and {} (comparison requires numeric operands)".format(op, left_type, right_type))

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for + or -: {} and {}".format(left_type, right_type))
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())
