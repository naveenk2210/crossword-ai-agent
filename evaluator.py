import json
from pathlib import Path


class CrosswordEvaluator:
    def __init__(
        self,
        puzzle,
        solution_path,
    ):
        self.puzzle = puzzle

        path = Path(solution_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            self.solution = json.load(file)

    def get_actual_answer(self, entry):
        return self.puzzle.get_pattern(entry)

    def evaluate(
        self,
        api_calls=0,
        elapsed_seconds=0.0,
    ):
        total_clues = len(self.solution)
        correct_clues = 0

        expected_cells = {}

        for entry in self.puzzle.entries:
            expected_answer = self.solution.get(
                entry.entry_id
            )

            if expected_answer is None:
                continue

            actual_answer = self.get_actual_answer(
                entry
            )

            if actual_answer == expected_answer:
                correct_clues += 1

            for position, letter in zip(
                entry.positions(),
                expected_answer,
            ):
                if (
                    position in expected_cells
                    and expected_cells[position] != letter
                ):
                    raise ValueError(
                        f"Conflicting solution at {position}"
                    )

                expected_cells[position] = letter

        correct_cells = 0
        filled_cells = 0

        for (row, col), expected_letter in (
            expected_cells.items()
        ):
            actual_letter = self.puzzle.grid[row][col]

            if actual_letter not in ("", "#"):
                filled_cells += 1

            if actual_letter == expected_letter:
                correct_cells += 1

        total_cells = len(expected_cells)

        clue_accuracy = (
            correct_clues / total_clues
            if total_clues
            else 0.0
        )

        letter_accuracy = (
            correct_cells / total_cells
            if total_cells
            else 0.0
        )

        fill_rate = (
            filled_cells / total_cells
            if total_cells
            else 0.0
        )

        exact_puzzle_match = (
            correct_clues == total_clues
            and total_clues > 0
        )

        return {
            "total_clues": total_clues,
            "correct_clues": correct_clues,
            "clue_accuracy": clue_accuracy,
            "letter_accuracy": letter_accuracy,
            "fill_rate": fill_rate,
            "exact_puzzle_match": exact_puzzle_match,
            "api_calls": api_calls,
            "elapsed_seconds": elapsed_seconds,
        }

    @staticmethod
    def print_report(metrics):
        print("\n===== EVALUATION =====")

        print(
            "Clue accuracy: "
            f"{metrics['clue_accuracy']:.1%} "
            f"({metrics['correct_clues']}/"
            f"{metrics['total_clues']})"
        )

        print(
            "Letter accuracy: "
            f"{metrics['letter_accuracy']:.1%}"
        )

        print(
            "Grid fill rate: "
            f"{metrics['fill_rate']:.1%}"
        )

        print(
            "Exact puzzle match: "
            f"{metrics['exact_puzzle_match']}"
        )

        print(
            f"API calls: {metrics['api_calls']}"
        )

        print(
            "Solve time: "
            f"{metrics['elapsed_seconds']:.2f} seconds"
        )
