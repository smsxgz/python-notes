def naive_pattern_search(pattern, txt):
    M = len(pattern)
    N = len(txt)

    for i in range(N - M + 1):
        for j in range(M):
            if txt[i + j] != pattern[j]:
                break
        else:
            print('Pattern found as index {}'.format(i))


# KMP
def computeLPSArray(pat, M):
    lps = [0] * M

    i = 0
    j = 1

    while j < M:
        if pat[i] == pat[j]:
            i += 1
            lps[j] = i
            j += 1
        else:
            if i != 0:
                i = lps[i - 1]

            else:
                lps[j] = 0
                j += 1

    return lps


def KMP(pat, txt):
    M = len(pat)
    N = len(txt)

    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    lps = computeLPSArray(pat, M)

    i = 0  # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            print("pattern found at index " + str(i - j))
            j = lps[j - 1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1


# Rabin Karp
def Rabin_Karp(pattern, txt, q):
    d = 256
    M = len(pattern)
    N = len(txt)
    i = 0
    j = 0
    p = 0
    t = 0
    h = 1

    for i in range(M - 1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(txt[i])) % q

    for i in range(N - M + 1):
        if p == t:
            for j in range(M):
                if txt[i + j] != pattern[j]:
                    break
            else:
                print('Pattern found as index {}'.format(i))
        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
            if t < 0:
                t = t + q


# Finite Automata
def computeTransFun(pat):
    M = len(pat)
    character_dict = dict((ch, i) for i, ch in enumerate(set(pat)))
    NO_OF_CHARS = len(character_dict)

    lps = 0
    TF = [[0 for _1 in range(NO_OF_CHARS)] for _2 in range(M + 1)]

    TF[0][character_dict[pat[0]]] = 1

    for i in range(1, M + 1):
        for x in range(NO_OF_CHARS):
            TF[i][x] = TF[lps][x]

        if i < M:
            TF[i][character_dict[pat[i]]] = i + 1
            lps = TF[lps][character_dict[pat[i]]]
        else:
            TF[i][character_dict[pat[0]]] = 1

    def trans_func(j, ch):
        if ch not in character_dict:
            return 0
        else:
            return TF[j][character_dict[ch]]

    return trans_func


def Finite_Automata(pat, txt):
    N = len(txt)
    M = len(pat)

    trans_func = computeTransFun(pat)

    j = 0
    for i in range(N):
        j = trans_func(j, txt[i])
        if j == M:
            print("pattern found at index " + str(i - M + 1))


if __name__ == '__main__':
    txt = "GEEKS FOR GEEKS"
    pattern = "GEEKS"
    naive_pattern_search(pattern, txt)
    KMP(pattern, txt)
    q = 101
    Rabin_Karp(pattern, txt, q)
    Finite_Automata(pattern, txt)
