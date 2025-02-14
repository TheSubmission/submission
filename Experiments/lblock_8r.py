import itertools
import time
import random
from tqdm import tqdm


S0 = [14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5]
S1 = [4, 11, 14, 9, 15, 13, 0, 10, 7, 12, 5, 6, 2, 8, 1, 3]
S2 = [1, 14, 7, 12, 15, 13, 0, 6, 11, 5, 9, 3, 2, 4, 8, 10]
S3 = [7, 6, 8, 11, 0, 15, 3, 14, 9, 10, 12, 13, 5, 2, 4, 1]
S4 = [14, 5, 15, 0, 7, 2, 12, 13, 1, 8, 4, 9, 11, 10, 6, 3]
S5 = [2, 13, 11, 12, 15, 14, 0, 9, 7, 10, 6, 3, 1, 8, 4, 5]
S6 = [11, 9, 4, 14, 0, 15, 10, 13, 6, 12, 5, 7, 3, 8, 1, 2]
S7 = [13, 10, 15, 0, 14, 4, 9, 11, 2, 1, 8, 3, 7, 5, 12, 6]

#K0 = [7, 7, 10, 6, 10, 9, 13, 2, 11, 8, 7, 15, 13, 6, 13, 10, 11, 7, 15, 15, 12, 11, 2, 11, 7, 5, 14, 9, 12, 14]
#K1 = [7, 8, 13, 13, 14, 9, 10, 14, 2, 10, 4, 11, 8, 11, 1, 6, 11, 13, 7, 3, 8, 15, 1, 14, 9, 5, 5, 11, 5, 9]
#K2 = [13, 3, 4, 15, 15, 4, 9, 12, 13, 10, 14, 10, 5, 11, 2, 11, 8, 12, 14, 10, 8, 11, 3, 9, 7, 11, 7, 11, 5, 2]
#K3 = [12, 5, 9, 2, 10, 7, 12, 4, 3, 2, 10, 2, 14, 13, 11, 11, 13, 1, 10, 12, 3, 9, 2, 6, 3, 5, 1, 14, 14, 12]
#K4 = [8, 5, 12, 9, 3, 10, 5, 1, 2, 13, 2, 5, 1, 5, 8, 9, 12, 15, 12, 8, 3, 7, 10, 10, 15, 6, 1, 13, 14, 10]
#K5 = [6, 10, 9, 8, 12, 7, 3, 10, 12, 14, 9, 15, 12, 5, 7, 6, 14, 9, 7, 10, 4, 6, 10, 7, 13, 15, 7, 4, 14, 5]
#K6 = [2, 7, 10, 5, 13, 3, 13, 14, 2, 14, 8, 8, 8, 7, 6, 3, 7, 13, 8, 15, 10, 14, 10, 15, 11, 2, 7, 3, 14, 2]
#K7 = [1, 14, 15, 14, 4, 7, 1, 10, 13, 8, 1, 11, 5, 3, 5, 12, 2, 14, 2, 3, 2, 13, 11, 2, 7, 14, 10, 3, 10, 12]


def F(input, round, tag, K0,K1,K2,K3,K4,K5,K6,K7):
    if tag == 0:
        output = S0[input^K0[round]]
    elif tag == 1:
        output = S1[input^K1[round]]
    elif tag == 2:
        output = S2[input^K2[round]]
    elif tag == 3:
        output = S3[input^K3[round]]
    elif tag == 4:
        output = S4[input^K4[round]]
    elif tag == 5:
        output = S5[input^K5[round]]
    elif tag == 6:
        output = S6[input^K6[round]]
    elif tag == 7:
        output = S7[input^K7[round]]
    else:
        print("error")
        output = 0
    return output

def ROUND(in0,in1,in2,in3,in4,in5,in6,in7,in8,in9,in10,in11,in12,in13,in14,in15,round, K0,K1,K2,K3,K4,K5,K6,K7):
    out0 = in10 ^ F(in1, round, 1, K0,K1,K2,K3,K4,K5,K6,K7)
    out1 = in11 ^ F(in3, round, 3, K0,K1,K2,K3,K4,K5,K6,K7)
    out2 = in12 ^ F(in0, round, 0, K0,K1,K2,K3,K4,K5,K6,K7)
    out3 = in13 ^ F(in2, round, 2, K0,K1,K2,K3,K4,K5,K6,K7)
    out4 = in14 ^ F(in5, round, 5, K0,K1,K2,K3,K4,K5,K6,K7)
    out5 = in15 ^ F(in7, round, 7, K0,K1,K2,K3,K4,K5,K6,K7)
    out6 = in8 ^ F(in4, round, 4, K0,K1,K2,K3,K4,K5,K6,K7)
    out7 = in9 ^ F(in6, round, 6, K0,K1,K2,K3,K4,K5,K6,K7)
    out8 = in0
    out9 = in1
    out10 = in2
    out11 = in3
    out12 = in4
    out13 = in5
    out14 = in6
    out15 = in7

    return out0,out1,out2,out3,out4,out5,out6,out7,out8,out9,out10,out11,out12,out13,out14,out15

def one_a(x,a,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,order):
    numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    res = [-1] * 16
    combinations = list(itertools.permutations(numbers, 2))
    res[combinations[order][0]] = x
    res[combinations[order][1]] = a
    complement = list(set(numbers) - set(combinations[order]))
    res[complement[0]] = c0
    res[complement[1]] = c1
    res[complement[2]] = c2
    res[complement[3]] = c3
    res[complement[4]] = c4
    res[complement[5]] = c5
    res[complement[6]] = c6
    res[complement[7]] = c7
    res[complement[8]] = c8
    res[complement[9]] = c9
    res[complement[10]] = c10
    res[complement[11]] = c11
    res[complement[12]] = c12
    res[complement[13]] = c13

    return res
    

if __name__ == '__main__':
    #ax = 0x4a
    #ay = 0x81
    X0,X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11,X12,X13,X14,X15 = [-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16
    Y0,Y1,Y2,Y3,Y4,Y5,Y6,Y7,Y8,Y9,Y10,Y11,Y12,Y13,Y14,Y15 = [-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16
    f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 = [-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16,[-1]*16


    c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15 = [random.randint(0,15) for i in range(16)]

    R = 8
    end_pos = 9
    invalid = 0
    K0 = [random.randint(1, 15) for i in range(20)]
    K1 = [random.randint(1, 15) for i in range(20)]
    K2 = [random.randint(1, 15) for i in range(20)]
    K3 = [random.randint(1, 15) for i in range(20)]
    K4 = [random.randint(1, 15) for i in range(20)]
    K5 = [random.randint(1, 15) for i in range(20)]
    K6 = [random.randint(1, 15) for i in range(20)]
    K7 = [random.randint(1, 15) for i in range(20)]

    r1 = range(2**0)
    r2 = range(2**0)
    Arange = list(itertools.product(r1,r2))
    print(len(Arange))
    for ax,ay in tqdm(Arange):
        ax0,ax1,ax2,ax3,ax4 = [random.randint(0,15) for i in range(5)]
        ay0,ay1,ay2,ay3,ay4 = [random.randint(0,15) for i in range(5)]
        if ax0 == ay0 or ax1 == ay1 or ax2 == ay2 or ax3 == ay3 or ax4 == ay4:
            invalid += 1
            continue
        for order in range(1):
            for xy in range(16):
                #x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15 = one_a(xy,ax0,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,order)
                #y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15 = one_a(xy,ay0,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,order)
                x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = c0,c1,c2,c3,c4,c5,xy,c7,c8,c9,c10,c11,c12,c13,c14,ax0
                y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15 = c0,c1,c2,c3,c4,c5,xy,c7,c8,c9,c10,c11,c12,c13,c14,ay0
                for r in range(R):
                    x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15 = ROUND(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,r, K0,K1,K2,K3,K4,K5,K6,K7)
                    y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15 = ROUND(y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15,r, K0,K1,K2,K3,K4,K5,K6,K7)

                X0[xy],X1[xy],X2[xy],X3[xy],X4[xy],X5[xy],X6[xy],X7[xy],X8[xy],X9[xy],X10[xy],X11[xy],X12[xy],X13[xy],X14[xy],X15[xy] = x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15
                Y0[xy],Y1[xy],Y2[xy],Y3[xy],Y4[xy],Y5[xy],Y6[xy],Y7[xy],Y8[xy],Y9[xy],Y10[xy],Y11[xy],Y12[xy],Y13[xy],Y14[xy],Y15[xy] = y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15

            for i in range(16):
                f0[i],f1[i],f2[i],f3[i],f4[i],f5[i],f6[i],f7[i],f8[i],f9[i],f10[i],f11[i],f12[i],f13[i],f14[i],f15[i] = X0[i]^Y0[i],X1[i]^Y1[i],X2[i]^Y2[i],X3[i]^Y3[i],X4[i]^Y4[i],X5[i]^Y5[i],X6[i]^Y6[i],X7[i]^Y7[i],X8[i]^Y8[i],X9[i]^Y9[i],X10[i]^Y10[i],X11[i]^Y11[i],X12[i]^Y12[i],X13[i]^Y13[i],X14[i]^Y14[i],X15[i]^Y15[i]

            F_end = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15]
            for s in range(1,16):
                counter = 0
                for x in range(16):
                    if F_end[end_pos][x] == F_end[end_pos][x^s]:
                        counter += 1

                if counter == 16:
                    print('period: %s, site %s' % (str(s), str(end_pos)))
                    print('input0 is ：', c0, c1, c2, c3, c4, c5, 'x', c7, c8, c9, c10, c11, c12, c13, c14, ax0)
                    print('input1 is ：', c0, c1, c2, c3, c4, c5, 'x', c7, c8, c9, c10, c11, c12, c13, c14, ax1)

    print('valid number', len(Arange)-invalid)
    print('keys are: ', K0,K1,K2,K3,K4,K5,K6,K7)













    
    
    
    
