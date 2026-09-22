import os
import re

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class CrosswordAgent:
    def __init__(self):
        api_key = os.getenv("NEBIUS_API_KEY")

        base_url = os.getenv(
            "NEBIUS_BASE_URL",
            "https://api.tokenfactory.nebius.com/v1",
        )

        self.model = os.getenv(
            "NEBIUS_MODEL",
            "zai-org/GLM-5.3-Flash",
        )

        if not api_key:
            raise RuntimeError(
                "NEBIUS_API_KEY is missing from .env"
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    @staticmethod
    def matches_pattern(
        candidate: str,
        pattern: str,
    ) -> bool:
        if len(candidate) != len(pattern):
            return False

        for candidate_letter, pattern_letter in zip(
            candidate,
            pattern,
        ):
            if (
                pattern_letter != "_"
                and candidate_letter != pattern_letter
            ):
                return False

        return True

    def propose_candidates(
        self,
        clue: str,
        length: int,
        pattern: str,
        excluded=None,
        limit: int = 5,
    ):
        excluded = excluded or set()

        excluded_text = (
            ", ".join(sorted(excluded))
            if excluded
            else "NONE"
        )

        prompt = (
            f"Crossword clue: {clue}\n"
            f"Answer length: {length}\n"
            f"Pattern: {pattern}\n"
            f"Rejected answers: {excluded_text}\n\n"
            f"Give up to {limit} possible crossword answers.\n"
            "Every answer MUST match the exact length and pattern.\n"
            "An underscore means an unknown letter.\n"
            "Return answers only, one per line.\n"
            "No explanation."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You solve crossword clues. "
                        "Return only candidate answers. "
                        "Never explain your reasoning."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=300,
        )

        raw_response = (
            response.choices[0].message.content
            or ""
        )

        print(
            f"Raw model response: {raw_response!r}"
        )

        words = re.findall(
            r"[A-Za-z]+",
            raw_response.upper(),
        )

        candidates = []

        for word in words:
            if word in excluded:
                continue

            if len(word) != length:
                continue

            if not self.matches_pattern(
                word,
                pattern,
            ):
                continue

            if word not in candidates:
                candidates.append(word)

            if len(candidates) >= limit:
                break

        return candidates

    def solve_clue(
        self,
        clue: str,
        length: int,
        pattern=None,
    ):
        if pattern is None:
            pattern = "_" * length

        candidates = self.propose_candidates(
            clue=clue,
            length=length,
            pattern=pattern,
        )

        if not candidates:
            raise ValueError(
                f"No valid candidates returned "
                f"for clue: {clue}"
            )

        return candidates[0]


if __name__ == "__main__":
    print("Starting Crossword Agent...")

    agent = CrosswordAgent()

    print("Calling Nebius Token Factory...")

    candidates = agent.propose_candidates(
        clue="Largest planet in our solar system",
        length=7,
        pattern="_______",
    )

    print("Candidates:", candidates)
