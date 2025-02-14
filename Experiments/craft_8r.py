import copy
import time
import random

S = [12, 10, 13, 3, 14, 11, 15, 7, 8, 9, 1, 5, 0, 2, 4, 6]

K = [
    [6, 3, 4, 8, 15, 13, 14, 5, 10, 1, 11, 12, 9, 2, 0, 7],
    [11, 15, 7, 2, 0, 13, 5, 14, 6, 8, 10, 4, 1, 9, 12, 3],
    [15, 10, 1, 0, 13, 3, 7, 11, 12, 14, 4, 8, 9, 5, 6, 2],
    [11, 8, 1, 3, 13, 14, 2, 0, 15, 4, 9, 5, 10, 6, 12, 7],
    [7, 12, 9, 6, 14, 13, 0, 15, 3, 1, 2, 11, 4, 5, 8, 10],
    [13, 10, 6, 4, 0, 1, 5, 8, 14, 3, 9, 12, 2, 15, 11, 7],
    [3, 15, 12, 7, 8, 5, 11, 6, 4, 2, 13, 1, 10, 0, 9, 14],
    [11, 7, 9, 15, 6, 12, 5, 4, 0, 2, 1, 13, 8, 10, 3, 14],
    [8, 6, 11, 3, 12, 0, 5, 10, 2, 13, 15, 9, 7, 14, 4, 1],
    [15, 14, 7, 10, 4, 12, 9, 3, 5, 13, 8, 0, 6, 11, 2, 1],
    [3, 0, 11, 14, 6, 7, 12, 2, 9, 13, 10, 5, 4, 8, 15, 1],
    [10, 15, 4, 8, 5, 9, 11, 13, 1, 0, 3, 7, 12, 14, 6, 2],
    [7, 0, 8, 5, 12, 11, 1, 14, 10, 9, 3, 6, 4, 15, 13, 2],
    [4, 8, 0, 15, 13, 7, 5, 12, 6, 3, 14, 2, 10, 1, 9, 11],
    [8, 3, 2, 1, 11, 5, 12, 4, 13, 9, 0, 7, 10, 15, 14, 6],
    [2, 8, 0, 9, 13, 10, 14, 1, 7, 5, 4, 11, 3, 15, 6, 12],
]

C = [
    [14, 4, 0, 11, 12, 8, 7, 10, 15, 6, 13, 1, 5, 3, 9, 2],
    [15, 11, 9, 5, 7, 3, 8, 6, 13, 4, 10, 12, 2, 11, 0, 1],
    [2, 8, 2, 5, 1, 12, 13, 9, 10, 6, 3, 0, 7, 14, 11, 4],
    [9, 3, 7, 10, 6, 8, 5, 12, 15, 4, 14, 11, 2, 13, 0, 1],
    [10, 6, 5, 9, 12, 15, 1, 13, 14, 8, 2, 4, 3, 11, 6, 0],
    [11, 0, 8, 3, 12, 7, 2, 1, 14, 5, 9, 4, 15, 6, 13, 10],
    [5, 3, 6, 1, 0, 10, 15, 8, 13, 4, 11, 14, 2, 12, 7, 9],
    [14, 7, 5, 1, 8, 3, 0, 10, 4, 15, 9, 11, 13, 12, 5, 6],
    [8, 11, 2, 0, 13, 4, 12, 3, 5, 9, 7, 14, 1, 10, 6, 15],
    [13, 5, 1, 11, 8, 4, 10, 13, 12, 2, 9, 7, 3, 15, 0, 6],
    [9, 3, 5, 14, 11, 10, 2, 4, 13, 7, 6, 0, 1, 3, 12, 8],
    [4, 7, 13, 2, 7, 12, 15, 1, 9, 5, 6, 11, 0, 8, 14, 10],
    [2, 1, 8, 15, 7, 10, 6, 9, 4, 3, 5, 11, 13, 0, 14, 12],
    [8, 9, 15, 3, 7, 12, 11, 9, 5, 4, 6, 2, 13, 1, 10, 14],
    [2, 0, 14, 8, 15, 9, 12, 13, 3, 5, 11, 1, 7, 10, 4, 6],
    [6, 7, 11, 8, 13, 6, 3, 12, 5, 9, 14, 0, 15, 4, 10, 1],
    [3, 15, 8, 7, 14, 9, 6, 2, 12, 1, 13, 5, 10, 0, 4, 11],
    [10, 2, 7, 0, 11, 9, 12, 4, 6, 3, 5, 13, 15, 14, 8, 1],
    [3, 6, 2, 13, 8, 5, 9, 12, 4, 1, 7, 15, 0, 10, 14, 11],
    [7, 4, 0, 8, 14, 12, 3, 10, 13, 11, 6, 2, 15, 9, 1, 5],
    [3, 2, 14, 11, 9, 10, 6, 5, 12, 1, 0, 4, 13, 15, 7, 8],
    [8, 9, 11, 12, 3, 13, 4, 0, 1, 15, 14, 2, 6, 5, 10, 7],
    [10, 2, 1, 8, 11, 7, 14, 3, 5, 9, 6, 0, 15, 13, 4, 12],
    [5, 10, 15, 0, 1, 13, 2, 12, 4, 8, 9, 6, 3, 14, 7, 11],
    [9, 8, 13, 4, 7, 11, 6, 10, 3, 12, 1, 14, 0, 5, 2, 15],
    [7, 14, 13, 11, 9, 0, 10, 4, 5, 15, 3, 1, 12, 2, 6, 8],
    [1, 3, 7, 9, 12, 11, 13, 4, 2, 8, 0, 14, 6, 5, 10, 15],
    [4, 3, 7, 10, 5, 14, 13, 8, 15, 6, 9, 11, 12, 1, 2, 0],
    [9, 3, 11, 14, 10, 8, 2, 7, 0, 1, 13, 5, 15, 12, 4, 6],
    [7, 15, 11, 5, 1, 9, 13, 10, 0, 12, 14, 2, 8, 3, 6, 4],
    [8, 9, 14, 15, 13, 6, 10, 2, 0, 3, 7, 12, 1, 5, 4, 11],
    [7, 10, 2, 9, 6, 8, 15, 13, 14, 1, 5, 0, 11, 12, 3, 4],
]


def F(input, round):
    MC_out = [-1 for i in range(16)]
    a = 0
    b = 4
    c = 8
    d = 12
    MC_out[a] = input[a] ^ input[c] ^ input[d]
    MC_out[b] = input[b] ^ input[d]
    MC_out[c] = input[c]
    MC_out[d] = input[d]
    a = 1
    b = 5
    c = 9
    d = 13
    MC_out[a] = input[a] ^ input[c] ^ input[d]
    MC_out[b] = input[b] ^ input[d]
    MC_out[c] = input[c]
    MC_out[d] = input[d]
    a = 2
    b = 6
    c = 10
    d = 14
    MC_out[a] = input[a] ^ input[c] ^ input[d]
    MC_out[b] = input[b] ^ input[d]
    MC_out[c] = input[c]
    MC_out[d] = input[d]
    a = 3
    b = 7
    c = 11
    d = 15
    MC_out[a] = input[a] ^ input[c] ^ input[d]
    MC_out[b] = input[b] ^ input[d]
    MC_out[c] = input[c]
    MC_out[d] = input[d]

    for i in [4, 5, 6, 7]:
        MC_out[i] ^= C[round][i]
    for i in range(16):
        MC_out[i] ^= K[round][i]

    P_out = [-1 for i in range(16)]
    P = [15, 12, 13, 14, 10, 9, 8, 11, 6, 5, 4, 7, 1, 2, 3, 0]
    for i in range(16):
        P_out[i] = MC_out[P[i]]


    S_out = [0 for i in range(16)]
    for i in range(16):
        S_out[i] = S[P_out[i]]

    #print(S,K,C)
    return S_out


if __name__ == '__main__':
    #with open("result.txt", "w") as f:
        #pass

    TIMES = 2**10
    invalid = 0
    R = 8

    C = [[0x0 for i in range(16)] for j in range(R)]
    for i in range(R):
        usednum = []
        while len(usednum) < 16:
            num = random.randint(0, 15)
            if num in usednum:
                continue
            C[i][len(usednum)] = num
            usednum.append(num)
    K = [[0x0 for i in range(16)] for j in range(R)]
    for i in range(R):
        usednum = []
        while len(usednum) < 16:
            num = random.randint(0, 15)
            if num in usednum:
                continue
            K[i][len(usednum)] = num
            usednum.append(num)


    end_state = 4
    start = time.time()
    counter = 0
    for thistime in range(TIMES):

        a40,a41,b40,b41,d40,d41,e40,e41 = [random.randint(0, 15) for i in range(8)]
        c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15 = [random.randint(0, 15) for i in range(16)]

        if a40 == a41 or b40 == b41 or d40 == d41 or e40 == e41:
            invalid += 1
            continue

        XVALUEa0 = dict()
        XVALUEa1 = dict()
        for x in range(16):
            inp = [c0, c1, c2, x,
                   c4, c5, a40, b40,
                   c8, c9, c10, c11,
                   c12, c13, c14, b40]
            for r in range(0, R):
                out = F(inp, r)
                inp = out
            XVALUEa0[x] = out[end_state]

            inp = [c0, c1, c2, x,
                   c4, c5, a41, b41,
                   c8, c9, c10, c11,
                   c12, c13, c14, b41]
            for r in range(0, R):
                out = F(inp, r)
                inp = out
            XVALUEa1[x] = out[end_state]

        period = -1
        XValuexor = dict()
        for x in XVALUEa0.keys():
            XValuexor[x] = XVALUEa0[x] ^ XVALUEa1[x]
        for s in range(1, 16):
            x0 = 0
            x1 = x0 ^ s
            out0 = XValuexor[x0]
            out1 = XValuexor[x1]
            if out0 == out1:
                success = 1
                for x0 in range(1, 16):
                    x1 = x0 ^ s
                    out0 = XValuexor[x0]
                    out1 = XValuexor[x1]
                    if out0 != out1:
                        success = 0
                if success == 1:
                    print("pass, s={:x}".format(s))
                    # print("i={:x}".format(i))
                    counter += 1
                    break

        # print("count: {}/{}".format(counter, 256))
        #with open("result.txt", "a+") as f:
            #f.write("{}\n".format(counter))
    print(time.time()-start)
    print("invalid:{}".format(invalid))
    print("final test number:{}".format(TIMES - invalid))
    print("probability:", counter/(TIMES - invalid))
    print('counter',counter)




