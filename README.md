# Crossword AI Agent

An AI agent that solves crossword puzzles using Nebius Token Factory and deterministic crossword constraints.

The agent uses an LLM to generate candidate answers, then validates those candidates against answer length, known letters, and Across/Down intersections before placing them in the grid.

## Architecture

The solving loop is:

1. Load the crossword puzzle.
2. Select an unsolved clue.
3. Build the current pattern from known crossing letters.
4. Ask the LLM for candidate answers.
5. Validate candidate length and crossing constraints.
6. Accept a valid candidate or retry.
7. Propagate newly discovered letters through the grid.
8. Continue until the puzzle is complete or no further progress is possible.
9. Evaluate the completed grid against a separate answer key.

```text
Crossword JSON
      |
      v
CrosswordPuzzle
      |
      v
CrosswordSolver
      |
      v
CrosswordAgent
      |
      v
Nebius Token Factory
      |
      v
Candidate Answers
      |
      v
Constraint Validation
      |
   +--+--+
   |     |
 Valid Invalid
   |     |
 Place  Retry
   |
   v
Updated Grid
Key Components
agent.py - communicates with Nebius Token Factory and generates candidate answers.
crossword.py - represents the crossword grid, clues, positions, patterns, and intersections.
solver.py - controls the iterative solving and retry loop.
evaluator.py - calculates solution-quality and efficiency metrics.
app.py - command-line entry point.
data/ - sample puzzles and separate answer keys.
tests/ - deterministic crossword constraint tests.
Requirements
Python 3.12+
Nebius Token Factory API key
Installation

Create and activate a virtual environment:

python3.12 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

NEBIUS_API_KEY=your_real_api_key
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1
NEBIUS_MODEL=zai-org/GLM-5.3-Flash

The .env file is excluded from Git.

Run

Run the default sample puzzle:

python app.py

Run another puzzle:

python app.py \
  --puzzle data/puzzle_2.json \
  --solution data/solution_2.json

Example:

1A Across: Round object used in many sports
Pattern: ____
Candidates: ['BALL']
Accepted: BALL

As crossing letters are discovered, later clues become more constrained:

Pattern: A___
Candidates: ['AREA']
Accepted: AREA
Tests

Run:

python -m pytest -v

Current deterministic tests verify:

Across/Down intersections
valid crossing answers
conflicting crossing rejection
incorrect answer-length rejection
Evaluation Methodology

The agent is evaluated using:

Clue accuracy - percentage of Across/Down clues solved correctly.
Letter accuracy - percentage of crossword cells containing the correct letter.
Grid fill rate - percentage of answer cells filled by the agent.
Exact puzzle match - whether the complete puzzle exactly matches the answer key.
API calls - number of LLM requests required to solve the puzzle.
Solve time - end-to-end solving latency.

The answer key is stored separately from the puzzle input so that the solver cannot use the correct answers during inference.

Initial Evaluation Results

Three controlled 4x4 puzzles were evaluated.

Puzzle	Clue Accuracy	Letter Accuracy	Exact Match	API Calls	Solve Time
Mini Crossword 1	100% (8/8)	100%	Yes	6	29.01 s
Mini Crossword 2	100% (8/8)	100%	Yes	5	12.31 s
Mini Crossword 3	100% (8/8)	100%	Yes	5	14.61 s

Across this controlled test set:

24/24 clue answers were correct.
3/3 puzzles achieved an exact match.
Average API usage was approximately 5.3 calls per puzzle.
Average solve time was approximately 18.6 seconds.

These are small synthetic evaluation puzzles and should not be interpreted as performance on arbitrary newspaper-scale crosswords.

Design Decisions
LLM reasoning + deterministic constraints

The LLM is responsible for semantic clue solving, while Python code enforces structural crossword constraints.

This prevents the system from blindly trusting model output.

Candidate generation

The model can return multiple possible answers. Candidates are filtered by:

required answer length
known crossing letters
previously rejected answers
Iterative solving

The solver performs multiple passes so that information discovered from one clue can constrain other clues.

Separate evaluation data

Correct solutions are stored separately from puzzle inputs. This avoids leaking answers into the solving process.

Current Limitations
The current implementation does not perform full search-tree backtracking when an early valid-looking answer later causes conflicts.
The initial evaluation set contains small synthetic 4x4 puzzles.
LLM responses are nondeterministic, so API-call count and latency may vary between runs.
More complex crossword conventions, rebus cells, themes, and multi-word normalization are not yet handled.
Possible Improvements
Add backtracking and candidate scoring.
Evaluate against larger real-world crossword datasets.
Add confidence scores for candidate answers.
Compare multiple Token Factory models.
Add token and monetary cost tracking.
Support blocked grids and larger puzzle formats.
