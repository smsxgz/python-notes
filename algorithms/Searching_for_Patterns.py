def naive_pattern_search(pattern, txt):
    M = len(pattern)
    N = len(txt)

    for i in range(N - M + 1):
        for j in range(M):
            if txt[i + j] != pattern[j]:
                break
        else:
            print('Pattern found as index {}'.format(i))


def computeLPSArray(pat, M, lps):
    l = 0
    i = 1

    while i < M:
        if pat[i] == pat[l]:
            l += 1
            lps[i] = l
            i += 1
        else:
            if l != 0:
                l = lps[l - 1]

            else:
                lps[i] = 0
                i += 1


def KMP():
    pass


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


if __name__ == '__main__':
    txt = "this is his pen."
    pattern = 'his'
    q = 101
    naive_pattern_search(pattern, txt)
    Rabin_Karp(pattern, txt, q)
