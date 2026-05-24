from abc import ABC, abstractmethod

# INTERPRETER PATTERN: Expression Classes
class MathExpression(ABC):
    """Interface: semua elemen grammar harus bisa di-calculate()."""

    @abstractmethod
    def calculate(self) -> float:
        pass


class Num(MathExpression):
    """Terminal Expression: leaf node, langsung return nilainya."""

    def __init__(self, value: float):
        self.value = value

    def calculate(self) -> float:
        print(f"  Num({self.value}).calculate() return {self.value}")
        return self.value


class PlusExpression(MathExpression):
    """Compound Expression: delegasi ke left dan right, lalu jumlahkan."""

    def __init__(self, left: MathExpression, right: MathExpression):
        self.left = left
        self.right = right

    def calculate(self) -> float:
        print("  PlusExpression.calculate()")
        l = self.left.calculate()
        r = self.right.calculate()
        result = l + r
        print(f"   {l} + {r} = {result}")
        return result


class MinusExpression(MathExpression):
    """Compound Expression: delegasi ke left dan right, lalu kurangkan."""

    def __init__(self, left: MathExpression, right: MathExpression):
        self.left = left
        self.right = right

    def calculate(self) -> float:
        print("  MinusExpression.calculate()")
        l = self.left.calculate()
        r = self.right.calculate()
        result = l - r
        print(f"   {l} - {r} = {result}")
        return result


class BracketsExpression(MathExpression):
    """Compound Expression: wrapper untuk grouping, forward ke child."""

    def __init__(self, expr: MathExpression):
        self.expr = expr

    def calculate(self) -> float:
        print("  BracketsExpression.calculate()")
        result = self.expr.calculate()
        print(f"   return {result}")
        return result

if __name__ == "__main__":

    # (3 + 5) - 2 = 6
    tree = MinusExpression(
        BracketsExpression(
            PlusExpression(Num(3), Num(5))
        ),
        Num(2)
    )

    print("Trace:")
    result = tree.calculate()
    print(f"\nHasil: {int(result)}")