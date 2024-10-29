
class SpreadSheet:

    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        value = self.get(cell)

        # Check if value is an integer
        if value.isdigit():
            return int(value)

        try:
            # Attempt to check if the value can be converted to a float
            float_value = float(value)
            return "#Error"  # Return error for floats
        except ValueError:
            pass  # Not a number, proceed to next checks

        # Handle string values
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]  # Strip the quotes

        # Handle formulas
        if value.startswith("="):
            # Strip the '=' character
            expression = value[1:]

            # Check for direct references to other cells
            if expression in self._cells:
                referenced_value = self.evaluate(expression)
                return referenced_value if isinstance(referenced_value, int) else "#Error"

            # Check if the expression is a valid integer or a quoted string
            if expression.isdigit():
                return str(expression)  # Return as string if it's a direct integer
            elif expression.startswith("'") and expression.endswith("'"):
                return expression[1:-1]  # Return unquoted string

            # Evaluate arithmetic expressions
            try:
                # Safely evaluate the expression, ensuring it doesn't yield floats
                # Replace cell references in the expression with their evaluated results
                for cell_ref in self._cells:
                    if cell_ref in expression:
                        evaluated_ref = self.evaluate(cell_ref)
                        if isinstance(evaluated_ref, int):
                            expression = expression.replace(cell_ref, str(evaluated_ref))
                        else:
                            return "#Error"
                result = eval(expression)
                if isinstance(result, int):
                    return result
                else:
                    return "#Error"
            except (SyntaxError, ZeroDivisionError, TypeError):
                return "#Error"  # Return error for any issues during evaluation

        return "#Error"  # Fallback for any unrecognized formats

