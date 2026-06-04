marks = 40
if marks >= 90:
    print("Grade: A")   
elif marks >= 80:
    print("Grade: B")
elif marks >= 70:
    print("Grade: C")
elif marks >= 60:
    print("Grade: D")
else:
    print("Grade: F")

    print("End of program")

import ast
import operator

class EvalSafe(ast.NodeVisitor):
    ALLOWED_BINOP = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.FloorDiv: operator.floordiv,
    }
    ALLOWED_UNARY = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
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
            user_input = input("> ")
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
            result = evaluate(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":    main()



