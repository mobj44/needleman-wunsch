import numpy as np
import copy


class Cell:
    def __init__(self, score, direction):
        self.score = score
        self.direction = direction

    def __str__(self):
        return f'({self.score}:{self.direction})'


class Path:
    def __init__(self, row, col, path=[]):
        self.path = path
        self.row = row
        self.col = col

    def __str__(self):
        return ''.join(self.path)


class Alignment:
    def __init__(self, path, alignment=[]):
        self.path = path
        self.alignment = alignment


def diagonal(matrix, i, j, seq1, seq2):
    if seq1[i-1] == seq2[j-1]:
        return matrix[i-1][j-1].score + 1
    else:
        return matrix[i-1][j-1].score - 1


def up(matrix, i, j):
    return matrix[i-1][j].score - 2


def left(matrix, i, j):
    return matrix[i][j-1].score - 2


def get_new_position(direction, row, col):
    match direction:
        case "D":
            row -= 1
            col -= 1
        case "U":
            row -= 1
        case "L":
            col -= 1
    return row, col


def get_paths(matrix):
    paths = []

    row, col = matrix.shape[0] - 1, matrix.shape[1] - 1
    base_path = Path(row, col)

    paths.append(base_path)

    for path in paths:
        cur_dir = matrix[path.row, path.col].direction
        while cur_dir != "X":
            if len(cur_dir) != 1:
                for i in range(1, len(cur_dir)):
                    new_path = copy.deepcopy(path)
                    new_path.path.append(cur_dir[i])
                    new_path.row, new_path.col = get_new_position(
                        cur_dir[i], new_path.row, new_path.col)
                    paths.append(new_path)
            path.path.append(cur_dir[0])
            path.row, path.col = get_new_position(
                cur_dir[0], path.row, path.col)
            cur_dir = matrix[path.row, path.col].direction

    return paths


def traverse_matrix(seq1, seq2, path):
    pointer1 = 0
    pointer2 = 0

    path.path.reverse()

    new_seq_1 = ''
    new_seq_2 = ''
    connector = ''

    for i in path.path:
        match i:
            case "D":
                new_seq_1 += seq1[pointer1]
                new_seq_2 += seq2[pointer2]
                pointer1 += 1
                pointer2 += 1
            case "U":
                new_seq_1 += "-"
                new_seq_2 += seq2[pointer2]
                pointer2 += 1
            case "L":
                new_seq_2 += "-"
                new_seq_1 += seq1[pointer1]
                pointer1 += 1

    for i in range(len(new_seq_1)):
        if new_seq_1[i] == new_seq_2[i]:
            connector += "|"
        else:
            connector += " "

    print(new_seq_1)
    print(connector)
    print(new_seq_2)


def fill_matrix(matrix, i, j, seq1, seq2):
    d = diagonal(matrix, i, j, seq1, seq2)
    u = up(matrix, i, j)
    l = left(matrix, i, j)

    directions = ''

    max_score = max(d, u, l)

    if d == max_score:
        directions += 'D'
    if u == max_score:
        directions += 'U'
    if l == max_score:
        directions += 'L'

    matrix[i][j] = Cell(max_score, directions)


def print_matrix(matrix):
    rows = []
    for i in range(matrix.shape[0]):
        row = []
        for j in range(matrix.shape[1]):
            row.append(str(matrix[i][j]))
        rows.append(" ".join(row))
    print("\n".join(rows))


def main():
    seq2 = "AGT"
    seq1 = "AAGC"

    # columns = j, rows = i
    matrix = np.empty((len(seq1)+1, len(seq2)+1), dtype=Cell)

    matrix[:, 0] = [Cell(i * -2, "U") for i in range(matrix.shape[0])]
    matrix[0, :] = [Cell(j * -2, "L") for j in range(matrix.shape[1])]
    matrix[0, 0] = Cell(0, "X")

    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1]):
            fill_matrix(matrix, i, j, seq1, seq2)

    print_matrix(matrix)

    paths = get_paths(matrix)
    for path in paths:
        traverse_matrix(seq2, seq1, path)


if __name__ == "__main__":
    main()
