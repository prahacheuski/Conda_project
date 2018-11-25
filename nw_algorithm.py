from collections import namedtuple
import numpy as np

IdentificationResult = namedtuple('IdentificationResult', ['identity', 'score'])


class NWAlgorithm(object):
    __slots__ = '__mat', '__mis', '__gap', '__gap_symbol'

    def __init__(self, match_score: int, mismatch_score: int, gap_score: int, gap_symbol: str = '-') -> None:
        self.__mat: int = match_score
        self.__mis: int = mismatch_score
        self.__gap: int = gap_score
        self.__gap_symbol: str = gap_symbol

    def __match_values(self, first: str, second: str) -> int:
        if first == second:
            result = self.__mat

        elif first == self.__gap_symbol or second == self.__gap_symbol:
            result = self.__gap

        else:
            result = self.__mis

        return result

    def __init_score(self, m: int, n: int) -> np.ndarray:
        score: np.ndarray = np.zeros((m + 1, n + 1))

        for i in range(m + 1):
            score[i][0] = self.__gap * i

        for j in range(n + 1):
            score[0][j] = self.__gap * j

        return score

    def identify(self, sequence1: str, sequence2: str) -> IdentificationResult:
        m, n = len(sequence1), len(sequence2)
        score: np.ndarray = self.__init_score(m, n)

        # Filling 'score'
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                diag = score[i - 1][j - 1] + self.__match_values(sequence1[i - 1], sequence2[j - 1])
                delete = score[i - 1][j] + self.__gap
                insert = score[i][j - 1] + self.__gap
                score[i][j] = max(diag, delete, insert)

        align1, align2 = '', ''
        i, j = m, n

        while i > 0 and j > 0:
            score_current = score[i][j]
            score_diag = score[i - 1][j - 1]
            score_left = score[i][j - 1]
            score_up = score[i - 1][j]

            if score_current == score_diag + self.__match_values(sequence1[i - 1], sequence2[j - 1]):
                a1, a2 = sequence1[i - 1], sequence2[j - 1]
                i, j = i - 1, j - 1

            elif score_current == score_up + self.__gap:
                a1, a2 = sequence1[i - 1], self.__gap_symbol
                i -= 1

            elif score_current == score_left + self.__gap:
                a1, a2 = self.__gap_symbol, sequence2[j - 1]
                j -= 1

            else:
                raise ValueError('Unexpected case.')

            align1 += a1
            align2 += a2

        while i > 0:
            a1, a2 = sequence1[i - 1], self.__gap_symbol
            align1 += a1
            align2 += a2
            i -= 1

        while j > 0:
            a1, a2 = self.__gap_symbol, sequence2[j - 1]
            align1 += a1
            align2 += a2
            j -= 1

        align1 = align1[::-1]
        align2 = align2[::-1]
        len_align1 = len(align1)
        seq_score = 0
        ident = 0

        for i in range(len_align1):
            a1 = align1[i]
            a2 = align2[i]
            if a1 == a2:
                ident += 1
                seq_score += self.__match_values(a1, a2)

            else:
                seq_score += self.__match_values(a1, a2)

        ident = float(ident) / len_align1 * 100  # Percentage

        return IdentificationResult(ident, seq_score)


if __name__ == '__main__':
    nw = NWAlgorithm(1, -1, -1)
    res = nw.identify('aabbccdaa', 'a2bc9mdaa')
    print(res)
