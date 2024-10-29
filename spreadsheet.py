
class SpreadSheet:

    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        value = self.get(cell)
        if value.isdigit():
            return int(value)
        try:
            float(value)
            return "#Error"
        except ValueError:
            if value.startswith("'") and value.endswith("'"):
                return value[1:-1]
            if value.startswith("="):
                if value[1:].isdigit():
                    return str(value[1:])
                elif value[1:].startswith("'") and value[-1] == "'":
                    return value[2:-1]
                elif value[1:] in self._cells:
                    referenced_value = self.evaluate(value[1:])
                    if isinstance(referenced_value, int):
                        return referenced_value
                    else:
                        return "#Error"
                try:
                    # Evaluate arithmetic expressions
                    return eval(value[1:])
                except:
                    return "#Error"
            return "#Error"

