import numpy as np

def diagonal(matrix, i, j, seq1, seq2):
    if seq1[i-1] == seq2[j-1]:
        return matrix[i-1][j-1] + 1
    else:
        return matrix[i-1][j-1] - 1


def up(matrix, i, j):
    return matrix[i-1][j] - 2


def left(matrix, i, j):
    return matrix[i][j-1] - 2


def fill_matrix(score, trace, i, j, seq1, seq2):
    d = diagonal(score, i, j, seq1, seq2)
    u = up(score, i, j)
    l = left(score, i, j)

    directions = ''

    max_score = max(d, u, l)

    if d == max_score:
        directions += 'D'
    if u == max_score:
        directions += 'U'
    if l == max_score:
        directions += 'L'

    trace[i][j] = directions
    score[i][j] = max_score


def main():
    seq2 = "AGT"
    seq1 = "AAGC"

    # columns = j, rows = i
    score_matrix = np.empty((len(seq1)+1, len(seq2)+1), dtype=int)
    traceback_matrix = np.empty((len(seq1)+1, len(seq2)+1), dtype=list)

    score_matrix[0, :] = np.arange(0, (len(seq2)+1)*-2, -2)
    score_matrix[:, 0] = np.arange(0, (len(seq1)+1)*-2, -2)

    traceback_matrix[0, :] = "L"
    traceback_matrix[:, 0] = "U"
    traceback_matrix[0, 0] = "X"

    for i in range(1, len(score_matrix[:, 0])):
        for j in range(1, len(score_matrix[0, :])):
            fill_matrix(score_matrix, traceback_matrix, i, j, seq1, seq2)

    print(f'\n{score_matrix}\n')
    print(f'{traceback_matrix}\n')


if __name__ == "__main__":
    main()
