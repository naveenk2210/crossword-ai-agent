import argparse
import time

from agent import CrosswordAgent
from crossword import CrosswordPuzzle
from evaluator import CrosswordEvaluator
from solver import CrosswordSolver


def main():
    parser = argparse.ArgumentParser(
        description="Solve and evaluate a crossword puzzle."
    )

    parser.add_argument(
        "--puzzle",
        default="data/sample_puzzle.json",
        help="Path to the crossword puzzle JSON file.",
    )

    parser.add_argument(
        "--solution",
        default="data/sample_solution.json",
        help="Path to the answer-key JSON file.",
    )

    args = parser.parse_args()

    puzzle = CrosswordPuzzle.from_json(
        args.puzzle
    )

    agent = CrosswordAgent()

    solver = CrosswordSolver(
        puzzle=puzzle,
        agent=agent,
    )

    start_time = time.perf_counter()

    solver.solve()

    elapsed_seconds = (
        time.perf_counter() - start_time
    )

    evaluator = CrosswordEvaluator(
        puzzle=puzzle,
        solution_path=args.solution,
    )

    metrics = evaluator.evaluate(
        api_calls=solver.api_calls,
        elapsed_seconds=elapsed_seconds,
    )

    evaluator.print_report(metrics)


if __name__ == "__main__":
    main()
