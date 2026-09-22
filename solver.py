from agent import CrosswordAgent
from crossword import CrosswordPuzzle


class CrosswordSolver:
    def __init__(
        self,
        puzzle: CrosswordPuzzle,
        agent: CrosswordAgent,
        max_passes: int = 5,
        max_attempts_per_entry: int = 2,
    ):
        self.puzzle = puzzle
        self.agent = agent

        self.max_passes = max_passes
        self.max_attempts_per_entry = max_attempts_per_entry

        self.failed_candidates = {
            entry.entry_id: set()
            for entry in puzzle.entries
        }

        self.accepted_answers = {}
        self.api_calls = 0

    def known_letter_count(self, entry):
        pattern = self.puzzle.get_pattern(entry)

        return sum(
            1
            for character in pattern
            if character != "_"
        )

    def is_entry_complete(self, entry):
        pattern = self.puzzle.get_pattern(entry)

        return "_" not in pattern

    def is_complete(self):
        return all(
            self.is_entry_complete(entry)
            for entry in self.puzzle.entries
        )

    def solve_entry(self, entry):
        pattern = self.puzzle.get_pattern(entry)

        print(
            f"\n{entry.entry_id} "
            f"{entry.direction.title()}: "
            f"{entry.clue}"
        )

        print(f"Pattern: {pattern}")

        rejected = self.failed_candidates[
            entry.entry_id
        ]

        for attempt in range(
            1,
            self.max_attempts_per_entry + 1,
        ):
            print(f"Attempt {attempt}")

            candidates = self.agent.propose_candidates(
                clue=entry.clue,
                length=entry.length,
                pattern=pattern,
                excluded=rejected,
            )

            self.api_calls += 1

            print("Candidates:", candidates)

            if not candidates:
                print("No candidates returned.")
                continue

            for candidate in candidates:
                if self.puzzle.can_place(
                    entry,
                    candidate,
                ):
                    self.puzzle.place_answer(
                        entry,
                        candidate,
                    )

                    self.accepted_answers[
                        entry.entry_id
                    ] = candidate

                    print(f"Accepted: {candidate}")

                    return True

                print(f"Rejected: {candidate}")
                rejected.add(candidate)

        print(
            f"Could not solve {entry.entry_id}."
        )

        return False

    def solve(self):
        print(
            f"\nSolving: {self.puzzle.title}"
        )

        self.puzzle.display()

        for pass_number in range(
            1,
            self.max_passes + 1,
        ):
            print(
                f"===== PASS {pass_number} ====="
            )

            if self.is_complete():
                break

            unsolved_entries = [
                entry
                for entry in self.puzzle.entries
                if not self.is_entry_complete(entry)
            ]

            unsolved_entries.sort(
                key=lambda entry: (
                    -self.known_letter_count(entry),
                    entry.length,
                    entry.number,
                )
            )

            progress = False

            for entry in unsolved_entries:
                if self.is_entry_complete(entry):
                    continue

                solved = self.solve_entry(entry)

                if solved:
                    progress = True
                    self.puzzle.display()

            if self.is_complete():
                break

            if not progress:
                print(
                    "No progress during this pass."
                )
                break

        print("\n===== RESULT =====")

        self.puzzle.display()

        print(
            f"API calls: {self.api_calls}"
        )

        print(
            f"Complete: {self.is_complete()}"
        )

        return self.puzzle
