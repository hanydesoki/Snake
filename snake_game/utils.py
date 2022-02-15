
def check_similar_element(squares):
        head = squares[0]
        return squares.count(head) > 1

def check_boundaries(squares, boundaries):
    max_i = max(max(squares, key=lambda s: s[0]))
    min_i = min(min(squares, key=lambda s: s[0]))
    max_j = max(max(squares, key=lambda s: s[1]))
    min_j = min(min(squares, key=lambda s: s[1]))
    cond1 = max_i > boundaries - 1 or max_j > boundaries - 1
    cond2 = min_i < 0 or min_j < 0

    return cond1 or cond2

def get_empty_space(grid):
    empty_squares = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == ' ':
                empty_squares.append([i, j])

    return empty_squares

def check_apple_in_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 'A':
                return True
    return False


