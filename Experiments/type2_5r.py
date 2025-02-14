import itertools
import random
import time
from tqdm import tqdm


S = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,]

#K0 = [random.randint(0, 255) for _ in range(20)]
#K1 = [random.randint(0, 255) for _ in range(20)]
#C0 = [random.randint(0, 255) for _ in range(20)]
#C1 = [random.randint(0, 255) for _ in range(20)]

def F0(input, round,K0,C0):
    output = S[input^K0[round]]^C0[round]
    return output

def F1(input, round,K1,C1):
    output = S[input^K1[round]]^C1[round]
    return output

def ROUND(in0,in1,in2,in3,round,K0,K1,C0,C1):
    out0 = in1 ^ F0(in0, round,K0,C0)
    out1 = in2
    out2 = in3 ^ F1(in2, round,K1,C1)
    out3 = in0
    return out0,out1,out2,out3

def one_a(x,a,c0,c1,order):
    numbers = [0,1,2,3]
    res = [-1] *4
    combinations = list(itertools.permutations(numbers, 2))
    res[combinations[order][0]] = x
    res[combinations[order][1]] = a
    complement = list(set(numbers) - set(combinations[order]))
    res[complement[0]] = c0
    res[complement[1]] = c1

    return res
    


if __name__ == '__main__':

    #ax = 0x4a
    #ay = 0x81
    X0,X1,X2,X3 = [-1]*256,[-1]*256,[-1]*256,[-1]*256
    Y0,Y1,Y2,Y3 = [-1]*256,[-1]*256,[-1]*256,[-1]*256
    f0,f1,f2,f3 = [-1]*256,[-1]*256,[-1]*256,[-1]*256

    #c0 = 0x77
    #c1 = 0xa1

    R = 5

    K0 = [random.randint(1, 15) for i in range(20)]
    C0 = [random.randint(1, 15) for i in range(20)]
    K1 = [random.randint(1, 15) for i in range(20)]
    C1 = [random.randint(1, 15) for i in range(20)]

    r1 = range(1)
    r2 = range(1)
    Arange = list(itertools.product(r1,r2))
    print(len(Arange))

    for ax,ay in tqdm(Arange):
        ax,ay = [random.randint(0,255) for i in range(2)]
        c0,c1 = [random.randint(0,255) for i in range(2)]
        if ax == ay:
            continue

        for order in range(1):
            for xy in range(256):
                #x0,x1,x2,x3 = one_a(xy,ax,c0,c1,order)
                #y0,y1,y2,y3 = one_a(xy,ay,c0,c1,order)
                x0, x1, x2, x3 = c0,c1,ax,xy
                y0, y1, y2, y3 = c0,c1,ay,xy
                for r in range(R):
                    x0,x1,x2,x3 = ROUND(x0,x1,x2,x3,r,K0,K1,C0,C1)
                    y0,y1,y2,y3 = ROUND(y0,y1,y2,y3,r,K0,K1,C0,C1)

                    #print(x0, x1, x2, x3)
                    #print(y0, y1, y2, y3)
                X0[xy],X1[xy],X2[xy],X3[xy] = x0,x1,x2,x3
                Y0[xy],Y1[xy],Y2[xy],Y3[xy] = y0,y1,y2,y3

            for i in range(256):
                f0[i],f1[i],f2[i],f3[i] = X0[i]^Y0[i],X1[i]^Y1[i],X2[i]^Y2[i],X3[i]^Y3[i]

            #print(f0)

            for s in range(1,256):
                counter = [0,0,0,0]
                for x in range(256):
                    if f0[x] == f0[x^s]:
                        counter[0] += 1
                    if f1[x] == f1[x^s]:
                        counter[1] += 1
                    if f2[x] == f2[x^s]:
                        counter[2] += 1
                    if f3[x] == f3[x^s]:
                        counter[3] += 1


                for i in range(4):
                    if counter[i] == 256:
                        print('period: %s, branch: %s' % (str(s), str(i)))
                        print('input0:', c0, c1, ax, 'x')
                        print('input0:', c0, c1, ay, 'x')
                        print('keys are: ', K0,K1)
                        print('Round constants are', C0,C1)

    













    
    
    
    
