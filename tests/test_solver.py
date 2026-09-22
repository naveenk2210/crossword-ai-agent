import pytest

from crossword import CrosswordPuzzle


def test_crossword_intersection():
    puzzle = CrosswordPuzzle.from_json(
        "data/sample_puzzle.json"
    )

    across = puzzle.get_entry("1A")
    down = puzzle.get_entry("1D")

    puzzle.place_answer(
        across,
        "BALL",
    )

    assert puzzle.get_pattern(down) == "B___"


def test_valid_crossing_answer():
    puzzle = CrosswordPuzzle.from_json(
        "data/sample_puzzle.json"
    )

    across = puzzle.get_entry("1A")
    down = puzzle.get_entry("1D")

    puzzle.place_answer(
        across,
        "BALL",
    )

    assert puzzle.can_place(
        down,
        "BALL",
    )


def test_conflicting_crossing_answer():
    puzzle = CrosswordPuzzle.from_json(
        "data/sample_puzzle.json"
    )

    across = puzzle.get_entry("1A")
    down = puzzle.get_entry("1D")

    puzzle.place_answer(
        across,
        "BALL",
    )

    assert not puzzle.can_place(
        down,
        "TALL",
    )


def test_wrong_length_answer():
    puzzle = CrosswordPuzzle.from_json(
        "data/sample_puzzle.json"
    )

    entry = puzzle.get_entry("1A")

    assert not puzzle.can_place(
        entry,
        "BASEBALL",
    )
