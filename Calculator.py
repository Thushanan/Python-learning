"""Simple safe calculator.

Usage: run and enter arithmetic expressions (e.g. 2+3*4, -5/2, (2+3)**2).
Type "quit" or "exit" to leave.
"""
import ast


class EvalSafe(ast.NodeVisitor):
    ALLOWED_BINOP = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a ** b,
        ast.FloorDiv: lambda a, b: a // b,
    }
    ALLOWED_UNARY = {
        ast.UAdd: lambda a: +a,
        ast.USub: lambda a: -a,
    }

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        return super().visit(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in self.ALLOWED_BINOP:
            return self.ALLOWED_BINOP[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in self.ALLOWED_UNARY:
            return self.ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    def visit_Num(self, node):
        return node.n

    def visit_Constant(self, node):  # for Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")

    def generic_visit(self, node):
        raise ValueError(f"Unsupported expression: {type(node).__name__}")


def evaluate(expr: str):
    tree = ast.parse(expr, mode="eval")
    return EvalSafe().visit(tree)


def main():
    print("Calculator — enter expression or 'quit' to exit")
    while True:
        try:
            s = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not s:
            continue
        if s.lower() in {"quit", "exit"}:
            break
        try:
            result = evaluate(s)
        except Exception as e:
            print("Error:", e)
        else:
            print(result)


if __name__ == "__main__":
    main()
