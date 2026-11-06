# Emanuel Messiha
# 7WCM2026-0911-2026 - Data Structure and Algorithms 2
# Question 1 - Maze

import random
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Below I saved the exact 21 by 21 maze provided in the question as a list of strings.
# A # represents a wall and a . represents a square that we can walk through.
# This also means that we do not need to download another file to run the code.
MAZE = [
    "#########.###########",
    "#.....#.......#...#.#",
    "#.#####.#.###.#.#.#.#",
    "#.#.....#.#.....#...#",
    "#.#.#####.###########",
    "#.#.#...#...........#",
    "#.#.###.#########.#.#",
    "#.#...#.....#...#.#.#",
    "#.###.#.#####.#.#.#.#",
    "#.#...#.#...#.#.#.#.#",
    "#.#.###.#.#.#.#.###.#",
    "#.#.#...#.#.#.#.....#",
    "#.#.###.#.#.#.#####.#",
    "#.#.#...#.#...#.....#",
    "#.#.#.#.#.###.#######",
    "#.#.#.#.#...#.#.....#",
    "#.#.#.#.###.#######.#",
    "#.#...#.#...#.....#.#",
    "#.#####.#.###.#.###.#",
    "#.......#.....#.....#",
    "###########.#########",
]

# The entrance is in the top row, and the exit is in the bottom row.
START = (0, 9)
EXIT = (20, 11)

# We only use four directions, so the program never moves diagonally.
# For Backtracking, I chose to check down, right, left and up in this order.
DIRECTIONS = [(1, 0), (0, 1), (0, -1), (-1, 0)]
MAX_STEPS = 200
TOTAL_RUNS = 10000


def check_maze(maze):
    # This checks that we have exactly 21 rows and 21 columns.
    if len(maze) != 21 or any(len(row) != 21 for row in maze):
        raise ValueError("The maze must contain exactly 21 rows and 21 columns.")
    if any(square not in ".#" for row in maze for square in row):
        raise ValueError("The maze must only contain walls (#) and paths (.).")
    if maze[START[0]][START[1]] != ".":
        raise ValueError("The entrance must be an open square.")
    if maze[EXIT[0]][EXIT[1]] != ".":
        raise ValueError("The exit must be an open square.")


def available_moves(maze, position):
    # The function below finds all legal squares next to our current position.
    # We check the maze boundaries and walls before allowing a movement.
    row, col = position
    moves = []
    for change_row, change_col in DIRECTIONS:
        next_row = row + change_row
        next_col = col + change_col
        if (0 <= next_row < len(maze) and
                0 <= next_col < len(maze[0]) and
                maze[next_row][next_col] == "."):
            moves.append((next_row, next_col))
    return moves


def solve_backtracking(maze):
    # Backtracking uses a visited set and a path list to explore possible routes.
    # If we reach a dead end, we remove the last position from our current path
    # and return to the previous position to try another direction.
    visited = set()
    history = []
    path = []

    def search(position):
        # This records each square as we enter it for the first time.
        visited.add(position)
        history.append(position)
        path.append(position)

        # If we reach the exit, the recursion can stop successfully.
        if position == EXIT:
            return True

        # We try each legal direction in our chosen fixed order.
        for next_position in available_moves(maze, position):
            if next_position not in visited:
                if search(next_position):
                    return True

                # This records the movement back to our previous square.
                history.append(position)

        # If no direction leads to the exit, we backtrack by removing this square.
        path.pop()
        return False

    success = search(START)
    return success, history, path


def solve_las_vegas(maze, generator):
    # The Las Vegas approach chooses the next legal move randomly.
    # We prefer squares not yet visited, but if all neighbors were visited,
    # we randomly choose from the available legal moves to keep exploring.
    position = START
    history = [position]
    visited = {position}
    steps = 0

    # The search stops as soon as we find the exit or complete 200 moves.
    while position != EXIT and steps < MAX_STEPS:
        possible_moves = available_moves(maze, position)
        if not possible_moves:
            # The supplied maze has no isolated open squares, but this check protects the code.
            raise ValueError("No legal orthogonal movements from the current square.")

        new_moves = [square for square in possible_moves if square not in visited]
        choices = new_moves if new_moves else possible_moves
        position = generator.choice(choices)
        history.append(position)
        visited.add(position)
        steps += 1

    success = position == EXIT
    return success, history, history if success else []


def print_maze(maze, visited_history=None, solution_path=None):
    # This displays the complete maze directly in the terminal.
    # S is the entrance, E is the exit, v means visited, and o is the solution path.
    visited = set(visited_history or [])
    solution = set(solution_path or [])
    print("Legend: # = wall, . = corridor, v = visited, o = solution, S = start, E = exit")
    for row in range(len(maze)):
        line = ""
        for col in range(len(maze[row])):
            position = (row, col)
            if position == START:
                line += "S"
            elif position == EXIT:
                line += "E"
            elif position in solution:
                line += "o"
            elif position in visited:
                line += "v"
            else:
                line += maze[row][col]
        print(line)
    print()


def draw_visited(maze, visited_history, solution_path, title, file_name):
    # Matplotlib displays every square visited, including any wrong turns.
    # The correct Backtracking route is shown separately from explored squares.
    image = [[0 if square == "#" else 1 for square in row] for row in maze]
    for row, col in set(visited_history):
        image[row][col] = 2
    for row, col in solution_path:
        image[row][col] = 3
    image[START[0]][START[1]] = 4
    image[EXIT[0]][EXIT[1]] = 5

    colours = ["#212121", "#FFFFFF", "#F9C74F", "#43AA8B", "#277DA1", "#F94144"]
    figure, ax = plt.subplots(figsize=(9, 9))
    ax.imshow(image, cmap=ListedColormap(colours), vmin=0, vmax=5,
              interpolation="nearest")
    ax.set_title(title)
    ax.set_xticks(range(0, 21, 2))
    ax.set_yticks(range(0, 21, 2))
    ax.set_xticks([number - 0.5 for number in range(22)], minor=True)
    ax.set_yticks([number - 0.5 for number in range(22)], minor=True)
    ax.grid(which="minor", color="#CCCCCC", linewidth=0.35)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.legend(handles=[Patch(facecolor=colour, edgecolor="grey", label=label)
                       for colour, label in zip(colours, [
                           "Wall", "Open", "Visited", "Solution path", "Entrance", "Exit"
                       ])], loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)
    figure.tight_layout()
    figure.savefig(file_name, dpi=200, bbox_inches="tight")
    print(f"Visited-squares image saved as: {file_name}")
    plt.show()


def compare_success_rates(maze):
    # We run BOTH algorithms 10,000 times as required by the question.
    # The fixed seed makes the random experiment reproducible.
    generator = random.Random(2026)
    backtracking_successes = 0
    las_vegas_successes = 0

    for _ in range(TOTAL_RUNS):
        if solve_backtracking(maze)[0]:
            backtracking_successes += 1
        if solve_las_vegas(maze, generator)[0]:
            las_vegas_successes += 1

    print(f"Backtracking: {backtracking_successes}/{TOTAL_RUNS} successful runs "
          f"= {100 * backtracking_successes / TOTAL_RUNS:.2f}%")
    print(f"Las Vegas: {las_vegas_successes}/{TOTAL_RUNS} successful runs "
          f"= {100 * las_vegas_successes / TOTAL_RUNS:.2f}%")


if __name__ == "__main__":
    check_maze(MAZE)

    print("QUESTION 1 - MAZE SOLVER")
    print("Original 21 x 21 maze from the assignment:")
    print_maze(MAZE)

    # Below we ask the user which of the two algorithms they want to use.
    while True:
        choice = input("Choose 1 for Backtracking or 2 for Las Vegas: ").strip()
        if choice in ("1", "2"):
            break
        print("Invalid choice. Please enter 1 or 2.")

    if choice == "1":
        approach = "Backtracking"
        successful, history, final_path = solve_backtracking(MAZE)
    else:
        approach = "Las Vegas"
        # A seed of 42 can be entered to repeat the same successful test.
        # Pressing Enter instead gives a new random result on each run.
        while True:
            seed_input = input("Optional random seed (press Enter for random): ").strip()
            try:
                generator = random.Random(int(seed_input)) if seed_input else random.Random()
                break
            except ValueError:
                print("Please enter an integer seed or press Enter.")
        successful, history, final_path = solve_las_vegas(MAZE, generator)

    print(f"\n{approach} result: {'SUCCESS - exit found' if successful else 'UNSUCCESSFUL - exit not found'}")
    print(f"Number of movements: {len(history) - 1}")
    print(f"Unique squares visited: {len(set(history))}")
    print("Visited positions in order:")
    print(history)
    print("\nMaze with the visited squares:")
    print_maze(MAZE, history, final_path if choice == "1" else [])

    print("SUCCESS RATES AFTER 10,000 RUNS")
    compare_success_rates(MAZE)

    # The visited-squares diagram is shown when the program finishes.
    output = Path("question1_visited_backtracking.png" if choice == "1"
                  else "question1_visited_las_vegas.png")
    draw_visited(MAZE, history, final_path if choice == "1" else [],
                 f"{approach} - visited squares ({'success' if successful else 'unsuccessful'})",
                 output)
