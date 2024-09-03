import heapq

class PuzzleState:
    def __init__(self, board, goal, moves=0, previous=None):
        self.board, self.goal, self.moves, self.previous = board, goal, moves, previous

    def __lt__(self, other):
        return self.moves + self.manhattan_distance() < other.moves + other.manhattan_distance()

    def manhattan_distance(self):
        distance, flat_goal = 0, sum(self.goal, [])
        for i in range(3):
            for j in range(3):
                if self.board[i][j]:
                    x, y = divmod(flat_goal.index(self.board[i][j]), 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def is_goal(self):
        return self.board == self.goal

    def get_neighbours(self):
        x, y = next((i, j) for i, row in enumerate(self.board) for j, val in enumerate(row) if not val)
        neighbours, directions = [], [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            if 0 <= x + dx < 3 and 0 <= y + dy < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[x + dx][y + dy] = new_board[x + dx][y + dy], new_board[x][y]
                neighbours.append(PuzzleState(new_board, self.goal, self.moves + 1, self))
        return neighbours

    def path(self):
        path, state = [], self
        while state:
            path.append(state.board)
            state = state.previous
        return path[::-1]

def a_star(start, goal):
    open_set, closed_set = [], set()
    heapq.heappush(open_set, PuzzleState(start, goal))

    while open_set:
        current = heapq.heappop(open_set)
        if current.is_goal(): return current.path()
        closed_set.add(tuple(map(tuple, current.board)))
        for neighbour in current.get_neighbours():
            if tuple(map(tuple, neighbour.board)) not in closed_set:
                heapq.heappush(open_set, neighbour)
    return None

# Example usage:
start = [
    [1, 2, 3],
    [0, 4, 5],
    [7, 8, 6]
]

goal = [
    [1, 2, 3],
    [4, 8, 0],
    [7, 6, 5]
]

solution = a_star(start, goal)

if solution:
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("No solution found.")
