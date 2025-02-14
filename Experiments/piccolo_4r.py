import itertools
import time
import random
from tqdm import tqdm
import numpy as np


def split_byte(x):
    if x < 0 or x > 255:
        raise ValueError("Input must be an integer between 0 and 255")
    a = (x >> 4) & 0x0F
    b = x & 0x0F

    return a, b


def combine_nibbles(a, b):

    if a < 0 or a > 15 or b < 0 or b > 15:
        raise ValueError("Both a and b must be integers between 0 and 15")
    x = (a << 4) | b
    return x


def gf_multiply(a, b, mod_poly=0b10011):
    p = 0
    while b > 0:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x10:
            a ^= mod_poly
        b >>= 1
    return p


def gf_add(a, b):
    return a ^ b


M = np.array([
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
], dtype=int)


def matrix_vector_multiply(M, x):
    result = [0] * 4
    for i in range(4):
        for j in range(4):
            result[i] = gf_add(result[i], gf_multiply(M[i, j], x[j]))
    return result

#S = [0xe, 0x4, 0xb, 0x2, 0x3, 0x8, 0x0, 0x9, 0x1, 0xa, 0x7, 0xf, 0x6, 0xc, 0x5, 0xd]

WK0 = [128, 106, 43, 139, 75, 187, 246, 231, 193, 239, 217, 162, 251, 227, 119, 195, 3, 62, 204, 18, 52, 228, 94, 44, 244, 211, 139, 31, 194, 87]
WK1 = [27, 134, 138, 211, 51, 7, 41, 132, 206, 8, 153, 253, 207, 18, 158, 151, 235, 89, 33, 40, 165, 79, 134, 106, 51, 143, 254, 243, 196, 89]
WK2 = [246, 147, 52, 120, 168, 58, 85, 83, 238, 89, 129, 206, 166, 12, 6, 37, 250, 64, 206, 55, 28, 250, 181, 46, 176, 237, 129, 25, 245, 128]
WK3 = [41, 93, 29, 156, 193, 23, 122, 118, 9, 101, 81, 136, 46, 204, 232, 89, 215, 14, 54, 139, 50, 106, 22, 101, 1, 138, 210, 17, 183, 147]

RK0 = [114, 77, 37, 196, 9, 147, 129, 171, 96, 225, 101, 2, 195, 13, 7, 57, 197, 239, 128, 2, 159, 102, 106, 248, 100, 172, 79, 114, 103, 204]
RK1 = [108, 168, 223, 219, 211, 109, 181, 55, 50, 168, 147, 2, 81, 134, 118, 249, 46, 254, 76, 34, 123, 155, 221, 182, 87, 13, 42, 126, 26, 0]
RK2 = [163, 88, 158, 237, 129, 142, 159, 194, 223, 211, 109, 140, 214, 60, 60, 106, 216, 108, 187, 36, 139, 173, 225, 245, 43, 232, 220, 226, 167, 23]
RK3 = [223, 94, 223, 228, 201, 223, 245, 41, 136, 15, 124, 24, 18, 93, 119, 186, 174, 143, 125, 180, 148, 111, 170, 217, 89, 187, 125, 50, 70, 99]


def ROUND(in0,in1,in2,in3,in4,in5,in6,in7,in8,in9,in10,in11,in12,in13,in14,in15,round,S,WK0,WK1,WK2,WK3,RK0,RK1,RK2,RK3):
    in0 = in0 ^ split_byte(WK0[round])[0]
    in1 = in1 ^ split_byte(WK0[round])[1]
    in2 = in2 ^ split_byte(WK1[round])[0]
    in3 = in3 ^ split_byte(WK1[round])[1]
    min1 = [S[in0], S[in1], S[in2], S[in3]]
    mout1 = matrix_vector_multiply(M, min1)

    in8 = in8 ^ split_byte(WK2[round])[0]
    in9 = in9 ^ split_byte(WK2[round])[1]
    in10 = in10 ^ split_byte(WK3[round])[0]
    in11 = in11 ^ split_byte(WK3[round])[1]
    min2 = [S[in8], S[in9], S[in10], S[in11]]
    mout2 = matrix_vector_multiply(M, min2)

    out0 = in4 ^ S[mout1[0]] ^ split_byte(RK0[round])[0]
    out1 = in5 ^ S[mout1[1]] ^ split_byte(RK0[round])[1]
    out2 = in14 ^ S[mout2[2]] ^ split_byte(RK3[round])[0]
    out3 = in15 ^ S[mout2[3]] ^ split_byte(RK3[round])[1]
    out4 = in8
    out5 = in9
    out6 = in2
    out7 = in3
    out8 = in12 ^ S[mout2[0]] ^ split_byte(RK2[round])[0]
    out9 = in13 ^ S[mout2[1]] ^ split_byte(RK2[round])[1]
    out10 = in6 ^ S[mout1[2]] ^ split_byte(RK1[round])[0]
    out11 = in7 ^ S[mout1[3]] ^ split_byte(RK1[round])[1]
    out12 = in0
    out13 = in1
    out14 = in10
    out15 = in11

    return out0,out1,out2,out3,out4,out5,out6,out7,out8,out9,out10,out11,out12,out13,out14,out15



if __name__ == '__main__':
    #ax = 0x4a
    #ay = 0x81
    X0,X1,X2,X3 = [-1]*65536,[-1]*65536,[-1]*65536,[-1]*65536
    Y0,Y1,Y2,Y3 = [-1]*65536,[-1]*65536,[-1]*65536,[-1]*65536
    f0,f1,f2,f3 = [-1]*65536,[-1]*65536,[-1]*65536,[-1]*65536

    R = 4
    end_pos = [4,5,6,7]

    C = 0
    invalid = 0
    Arange = range(1)
    print(len(Arange))

    WK0 = [random.randint(1, 255) for i in range(20)]
    WK1 = [random.randint(1, 255) for i in range(20)]
    WK2 = [random.randint(1, 255) for i in range(20)]
    WK3 = [random.randint(1, 255) for i in range(20)]
    RK0 = [random.randint(1, 255) for i in range(20)]
    RK1 = [random.randint(1, 255) for i in range(20)]
    RK2 = [random.randint(1, 255) for i in range(20)]
    RK3 = [random.randint(1, 255) for i in range(20)]

    #WK0 =[231, 82, 175, 57, 211, 153, 254, 18, 45, 116, 146, 129, 231, 38, 120, 52, 10, 47, 171, 69]
    #WK1 = [34, 86, 59, 234, 156, 190, 175, 10, 215, 227, 205, 73, 82, 85, 255, 96, 188, 87, 61, 202]
    #WK2 = [247, 119, 117, 93, 161, 241, 110, 211, 203, 176, 213, 108, 199, 28, 43, 13, 199, 192, 153, 142]
    #WK3 = [42, 200, 186, 57, 71, 123, 67, 140, 222, 144, 1, 23, 215, 152, 149, 176, 35, 51, 151, 21]
    #RK0 = [193, 247, 8, 199, 201, 229, 228, 203, 87, 90, 123, 44, 171, 170, 20, 222, 220, 91, 56, 198]
    #RK1 = [13, 23, 118, 193, 47, 240, 215, 75, 110, 191, 171, 110, 113, 185, 212, 247, 123, 142, 154, 11]
    #RK2 = [98, 236, 90, 10, 199, 111, 129, 69, 88, 193, 226, 148, 60, 198, 155, 94, 75, 60, 50, 252]
    #RK3 = [29, 41, 151, 13, 10, 159, 201, 201, 133, 134, 127, 222, 151, 60, 191, 130, 129, 245, 141, 36]

    for ax in Arange:

        S = [0xe, 0x4, 0xb, 0x2, 0x3, 0x8, 0x0, 0x9, 0x1, 0xa, 0x7, 0xf, 0x6, 0xc, 0x5, 0xd]

        c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13 = [random.randint(0, 15) for i in range(14)]
        a0x = random.randint(0,15)
        a0y = random.randint(0,15)
        a1x = random.randint(0,15)
        a1y = random.randint(0,15)

        if a0x == a0y or a1x == a1y:
            invalid += 1
            continue
        for order in range(1):
            for xy in range(65536):
                xy0 = (xy >> 12) & 0x000F
                xy1 = (xy >> 8) & 0x000F
                xy2 = (xy >> 4) & 0x000F
                xy3 = xy & 0x000F
                x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = c0,c1,c2,c3,c4,c5,c6,c7,a0x,a1x,c8,c9,xy0,xy1,xy2,xy3
                y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = c0,c1,c2,c3,c4,c5,c6,c7,a0y,a1y,c8,c9,xy0,xy1,xy2,xy3
                #x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = 10, 6, 7, 11, 10, 8, 7, 13, 11, 15, 3, 14,xy0,xy1,xy2,xy3
                #y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = 10, 6, 7, 11, 10, 8, 7, 13, 15, 4, 3, 14,xy0,xy1,xy2,xy3

                for r in range(R):
                    x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15 = ROUND(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,r,S,WK0,WK1,WK2,WK3,RK0,RK1,RK2,RK3)
                    y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15 = ROUND(y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15,r,S,WK0,WK1,WK2,WK3,RK0,RK1,RK2,RK3)

                    #print(x7,y7)

                X0[xy],X1[xy],X2[xy],X3[xy] = (((((x0<<4) | x1) << 4) | x2) << 4) | x3, (((((x4<<4) | x5) << 4) | x6) << 4) | x7, (((((x8<<4) | x9) << 4) | x10) << 4) | x11, (((((x12<<4) | x13) << 4) | x14) << 4) | x15
                Y0[xy],Y1[xy],Y2[xy],Y3[xy] = (((((y0<<4) | y1) << 4) | y2) << 4) | y3, (((((y4<<4) | y5) << 4) | y6) << 4) | y7, (((((y8<<4) | y9) << 4) | y10) << 4) | y11, (((((y12<<4) | y13) << 4) | y14) << 4) | y15

            for i in range(65536):
                f0[i],f1[i],f2[i],f3[i] = X0[i]^Y0[i],X1[i]^Y1[i],X2[i]^Y2[i],X3[i]^Y3[i]

            for s in tqdm(range(1,65536)):
                for i in range(len(end_pos)):
                    counter = 0
                    if end_pos[i] < 4:
                        for x in range(65536):
                            if (f0[x] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F == (f0[x^s] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F:
                                counter += 1

                    if 4 <= end_pos[i] < 8:
                        for x in range(65536):
                            if (f1[x] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F == (f1[x^s] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F:
                                counter += 1

                    if 8 <= end_pos[i] < 12:
                        for x in range(65536):
                            if (f2[x] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F == (f2[x^s] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F:
                                counter += 1

                    if end_pos[i] >= 12:
                        for x in range(65536):
                            if (f3[x] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F == (f3[x^s] >> ((end_pos[i]%4)*(-4) + 12)) & 0x000F:
                                counter += 1

                    if counter == 65536:
                        print('period: %s, branch: %s' % (str(s), str(end_pos[i])))
                        print('input0 is: ', c0, c1, c2, c3, c4, c5, c6, c7, a0x, a1x, c8, c9, 'x', 'x', 'x','x')
                        print('input1 is: ', c0, c1, c2, c3, c4, c5, c6, c7, a0y, a1y, c8, c9, 'x', 'x', 'x','x')
                        print('Sbox is: ', S)
                        C += 1

    print('keys are: ', WK0,WK1,WK2,WK3,RK0,RK1,RK2,RK3)
    print(C / (len(Arange) - invalid))
    print(C)
    













    
    
    
    
