import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CrosswordEntry:
    number: int
    direction: str
    row: int
    col: int
    length: int
    clue: str

    @property
    def entry_id(self) -> str:
        direction_letter = "A" if self.direction.lower() == "across" else "D"
        return f"{self.number}{direction_letter}"

    def positions(self):
        positions = []

        for offset in range(self.length):
            if self.direction.lower() == "across":
                positions.append(
                    (self.row, self.col + offset)
                )
            else:
                positions.append(
                    (self.row + offset, self.col)
                )

        return positions


class CrosswordPuzzle:
    def __init__(
        self,
        title: str,
        rows: int,
        cols: int,
        entries: list[CrosswordEntry],
        blocks=None,
    ):
        self.title = title
        self.rows = rows
        self.cols = cols
        self.entries = entries

        self.blocks = {
            tuple(block)
            for block in (blocks or [])
        }

        self.grid = [
            ["" for _ in range(cols)]
            for _ in range(rows)
        ]

        for row, col in self.blocks:
            self.grid[row][col] = "#"

    @classmethod
    def from_json(cls, file_path):
        path = Path(file_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        entries = [
            CrosswordEntry(
                number=item["number"],
                direction=item["direction"],
                row=item["row"],
                col=item["col"],
                length=item["length"],
                clue=item["clue"],
            )
            for item in data["entries"]
        ]

        return cls(
            title=data["title"],
            rows=data["rows"],
            cols=data["cols"],
            entries=entries,
            blocks=data.get("blocks", []),
        )

    def get_entry(self, entry_id: str):
        entry_id = entry_id.upper()

        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry

        raise KeyError(
            f"Crossword entry {entry_id} was not found."
        )

    def get_pattern(self, entry: CrosswordEntry) -> str:
        pattern = []

        for row, col in entry.positions():
            value = self.grid[row][col]

            if value == "":
                pattern.append("_")
            else:
                pattern.append(value)

        return "".join(pattern)

    @staticmethod
    def normalize_answer(answer: str) -> str:
        return re.sub(
            r"[^A-Za-z]",
            "",
            answer,
        ).upper()

    def can_place(
        self,
        entry: CrosswordEntry,
        answer: str,
    ) -> bool:
        answer = self.normalize_answer(answer)

        if len(answer) != entry.length:
            return False

        if not answer.isalpha():
            return False

        for (row, col), letter in zip(
            entry.positions(),
            answer,
        ):
            current = self.grid[row][col]

            if current == "#":
                return False

            if current not in ("", letter):
                return False

        return True

    def place_answer(
        self,
        entry: CrosswordEntry,
        answer: str,
    ):
        answer = self.normalize_answer(answer)

        if not self.can_place(
            entry,
            answer,
        ):
            pattern = self.get_pattern(entry)

            raise ValueError(
                f"{answer!r} cannot be placed in "
                f"{entry.entry_id}. "
                f"Current pattern: {pattern}"
            )

        for (row, col), letter in zip(
            entry.positions(),
            answer,
        ):
            self.grid[row][col] = letter

    def display(self):
        print(f"\n{self.title}\n")

        for row in self.grid:
            display_row = []

            for cell in row:
                if cell == "":
                    display_row.append(".")
                else:
                    display_row.append(cell)

            print(" ".join(display_row))

        print()


if __name__ == "__main__":
    puzzle = CrosswordPuzzle.from_json(
        "data/sample_puzzle.json"
    )

    puzzle.display()

    entry_1a = puzzle.get_entry("1A")

    print(
        "1A pattern before:",
        puzzle.get_pattern(entry_1a),
    )

    puzzle.place_answer(
        entry_1a,
        "BALL",
    )

    puzzle.display()

    entry_1d = puzzle.get_entry("1D")

    print(
        "1D pattern after placing 1A:",
        puzzle.get_pattern(entry_1d),
    )
