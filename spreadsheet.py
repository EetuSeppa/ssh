
class SpreadSheet:
    def __init__(self):
        self._cells = {}
        self._evaluating = set()

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        if cell in self._evaluating:
            return "#Circular"
        self._evaluating.add(cell)
        value = self.get(cell)
        if value.startswith("="):
            if value[1:].startswith("'") and value[-1] == "'":
                result = value[2:-1]
            else:
                ref = value[1:]
                if ref.isnumeric():
                    result = int(ref)
                elif ref in self._cells:
                    result = self.evaluate(ref)
                    if isinstance(result, str) and result.startswith("#"):
                        return result
                else:
                    result = "#Error"
        elif value.startswith("'") and value.endswith("'"):
            result = value[1:-1]
        else:
            try:
                result = int(value)
            except ValueError:
                result = "#Error"
        self._evaluating.remove(cell)
        return result


if __name__ == "__main__":
    spreadsheet = SpreadSheet()
    spreadsheet.set("A1", "=B1")
    spreadsheet.set("B1", "=A1")
    value = spreadsheet.evaluate("A1")

    print(value)

