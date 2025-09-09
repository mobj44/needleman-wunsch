'''
Needleman-Wunsch Algorith 
Morgan Johnston
'''

import copy
import numpy as np


class Cell:
    '''
    This Class defines a cell of the matrix. it includes the score and direction to traverse. 
    '''

    def __init__(self, score: int, direction: str):
        self.score = score
        self.direction = direction

    def __str__(self):
        return f'({self.score}:{self.direction})'


class Path:
    '''
    The path object contains a path as well as the current postion 
    in row and column that are used for getting the path.
    '''

    def __init__(self, position: tuple[int, int], path: list[str] = []):
        self.path = path
        self.position = position

    def __str__(self):
        return ''.join(self.path)


class Alignment:
    '''Stores an alignment and the path used to get it'''

    def __init__(self, path: list[str], alignment: list[str] = []):
        self.path = path
        self.alignment = alignment


def diagonal(matrix: np.ndarray, position: tuple[int, int], left_seq: str, top_seq: str) -> int:
    '''
    Calculates the diagonal rule

    Inputs: 
        matrix
        postition: current cell in matrix
        left_seq: DNA seq from left side of matrix
        top_seq: DNA seq from top of matrix

    Output: score 
    '''
    i, j = position

    if left_seq[i-1] == top_seq[j-1]:
        return matrix[i-1][j-1].score + 1
    return matrix[i-1][j-1].score - 1


def up(matrix: np.ndarray, position: tuple[int, int]) -> int:
    '''
    Calculates the up rule

    Inputs: 
        matrix
        postition: current cell in matrix
        left_seq: DNA seq from left side of matrix
        top_seq: DNA seq from top of matrix

    Output: score 
    '''
    i, j = position
    return matrix[i-1][j].score - 2


def left(matrix: np.ndarray, position: tuple[int, int]) -> int:
    '''
    Calculates the left rule

    Inputs: 
        matrix
        postition: current cell in matrix
        left_seq: DNA seq from left side of matrix
        top_seq: DNA seq from top of matrix

    Output: score 
    '''

    i, j = position
    return matrix[i][j-1].score - 2


def get_new_position(direction: str, position: tuple[int, int]) -> tuple[int, int]:
    '''
    Gets the new coordinates for the next direction in the path
    Inputs: 
        direction: current direction as a string (D,U,L)
        position: tuple of current coordinates (row, col)

    Outputs: row, col (tuple) new coordinates in the path
    '''
    row, col = position
    match direction:
        case "D":
            row -= 1
            col -= 1
        case "U":
            row -= 1
        case "L":
            col -= 1
        case _: pass
    return row, col


def get_paths(matrix: np.ndarray) -> list[Path]:
    '''
    Gets all possible paths

    Inputs: matrix
    Outputs: paths: list of paths 
    '''
    paths: list[Path] = []

    position = (matrix.shape[0] - 1, matrix.shape[1] - 1)
    base_path = Path(position)

    paths.append(base_path)

    for path in paths:
        row, col = path.position
        cur_dir = matrix[row, col].direction
        while cur_dir != "X":
            if len(cur_dir) > 1:
                for i in range(1, len(cur_dir)):
                    new_path = copy.deepcopy(path)
                    new_path.path.append(cur_dir[i])
                    new_path.position = get_new_position(
                        cur_dir[i], new_path.position)
                    paths.append(new_path)

            path.path.append(cur_dir[0])
            path.position = get_new_position(cur_dir[0], path.position)
            row, col = path.position
            cur_dir = matrix[row, col].direction

    return paths


def build_alignment(left_seq: str, top_seq: str, path: Path):
    '''
    Builds and prints an alignment based on the traceback path

    Inputs:
        left_seq: DNA seq from left side of matrix
        top_seq: DNA seq from top of matrix
        path: a path object that stores the traceback

    Outputs: 
        prints alignment
    '''
    pointer1 = 0
    pointer2 = 0

    path.path.reverse()

    new_seq_1: str = ''
    new_seq_2: str = ''
    connector = ''

    for i in path.path:
        match i:
            case "D":
                new_seq_1 += left_seq[pointer1]
                new_seq_2 += top_seq[pointer2]
                pointer1 += 1
                pointer2 += 1
            case "U":
                new_seq_1 += "-"
                new_seq_2 += top_seq[pointer2]
                pointer2 += 1
            case "L":
                new_seq_2 += "-"
                new_seq_1 += left_seq[pointer1]
                pointer1 += 1
            case _:
                pass

    for i in range(len(new_seq_1)):
        if new_seq_1[i] == new_seq_2[i]:
            connector += "|"
        else:
            connector += " "

    print(f'\n{new_seq_1}')
    print(connector)
    print(f'{new_seq_2}\n')


def fill_matrix(matrix: np.ndarray, position: tuple[int, int], left_seq: str, top_seq: str):
    '''
    Fills matrix with score and direction

    Inputs: 
        matrix: score and traceback
        position: cell position in the matrix
        left_seq: DNA seq from left side of matrix
        top_seq: DNA seq from top of matrix
    '''

    d = diagonal(matrix, position, left_seq, top_seq)
    u = up(matrix, position)
    l = left(matrix, position)

    directions = ''

    max_score = max(d, u, l)

    if d == max_score:
        directions += 'D'
    if u == max_score:
        directions += 'U'
    if l == max_score:
        directions += 'L'

    i, j = position
    matrix[i][j] = Cell(max_score, directions)


def print_matrix(matrix: np.ndarray):
    '''
    Prints the matrix nice!

    Input: matrix 
    Output: prints matrix
    '''
    rows: list[str] = []
    for i in range(matrix.shape[0]):
        row: list[str] = []
        for j in range(matrix.shape[1]):
            row.append(str(matrix[i][j]))
        rows.append(" ".join(row))
    print("\n".join(rows))


def main():
    '''This is the main function'''
    top_seq = "ATG"
    left_seq = "GGAATGG"

    # columns = j, rows = i
    matrix = np.empty((len(left_seq)+1, len(top_seq)+1), dtype=Cell)

    matrix[:, 0] = [Cell(i * -2, "U") for i in range(matrix.shape[0])]
    matrix[0, :] = [Cell(j * -2, "L") for j in range(matrix.shape[1])]
    matrix[0, 0] = Cell(0, "X")

    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1]):
            position = (i, j)
            fill_matrix(matrix, position, left_seq, top_seq)

    print_matrix(matrix)

    paths = get_paths(matrix)
    for path in paths:
        build_alignment(top_seq, left_seq, path)


if __name__ == "__main__":
    main()
