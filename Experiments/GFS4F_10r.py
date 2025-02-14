import copy
import time
from tqdm import tqdm
import random

S1 = [
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

S2 = [244, 215, 8, 117, 92, 25, 102, 113, 246, 36, 48, 225, 68, 132, 81, 208, 107, 52, 55, 89, 53, 141, 21, 165, 71, 79, 192, 106, 116, 26, 161, 217, 73, 213, 184, 49, 235, 138, 218, 206, 24, 22, 129, 232, 5, 64, 175, 108, 78, 34, 86, 4, 32, 168, 154, 195, 179, 44, 60, 243, 56, 125, 58, 198, 166, 70, 219, 149, 65, 203, 95, 180, 236, 88, 33, 59, 38, 11, 152, 35, 186, 205, 157, 171, 40, 45, 181, 240, 146, 147, 46, 80, 14, 1, 231, 227, 28, 17, 248, 77, 96, 122, 30, 105, 67, 202, 187, 156, 83, 253, 99, 13, 185, 15, 196, 228, 167, 140, 229, 31, 54, 245, 193, 75, 177, 91, 112, 160, 162, 76, 216, 251, 249, 98, 188, 93, 151, 207, 176, 118, 201, 242, 137, 197, 211, 100, 19, 20, 115, 173, 94, 2, 27, 189, 62, 47, 190, 220, 124, 0, 97, 239, 131, 109, 7, 234, 134, 41, 29, 121, 114, 210, 84, 63, 111, 74, 250, 90, 183, 222, 200, 247, 182, 110, 159, 136, 144, 145, 101, 158, 148, 178, 10, 18, 57, 139, 6, 87, 142, 104, 252, 226, 135, 82, 224, 9, 199, 103, 61, 172, 69, 153, 130, 169, 174, 194, 233, 237, 127, 204, 50, 155, 51, 12, 255, 254, 66, 85, 163, 120, 3, 42, 16, 123, 39, 191, 238, 23, 212, 241, 126, 164, 37, 170, 128, 133, 214, 143, 150, 221, 209, 230, 223, 119, 72, 43]

S3 = [145, 7, 228, 159, 155, 41, 82, 213, 98, 140, 132, 71, 170, 29, 25, 248, 126, 99, 114, 129, 90, 138, 151, 72, 80, 23, 166, 148, 229, 223, 86, 17, 1, 28, 35, 19, 175, 240, 194, 186, 206, 63, 91, 134, 123, 125, 163, 87, 54, 58, 143, 136, 69, 221, 68, 89, 198, 214, 254, 20, 109, 30, 174, 146, 237, 167, 13, 245, 179, 115, 15, 31, 57, 195, 22, 164, 177, 156, 116, 241, 216, 6, 173, 44, 150, 34, 239, 53, 9, 243, 144, 59, 238, 83, 8, 133, 157, 18, 0, 56, 189, 101, 119, 203, 40, 36, 217, 103, 65, 67, 168, 188, 182, 85, 27, 135, 176, 95, 200, 75, 152, 3, 149, 190, 226, 231, 220, 249, 2, 55, 227, 79, 131, 88, 201, 74, 39, 12, 142, 104, 106, 10, 252, 172, 118, 100, 207, 94, 212, 97, 102, 247, 230, 45, 51, 78, 124, 37, 105, 26, 202, 117, 46, 139, 178, 255, 4, 49, 130, 92, 169, 246, 38, 161, 73, 93, 171, 162, 165, 187, 209, 232, 62, 107, 192, 76, 242, 110, 112, 77, 160, 52, 108, 196, 147, 219, 158, 224, 222, 42, 50, 204, 235, 47, 185, 253, 48, 84, 208, 184, 60, 197, 120, 66, 128, 21, 122, 111, 137, 211, 153, 244, 154, 5, 236, 251, 191, 180, 250, 193, 225, 70, 210, 205, 61, 183, 234, 121, 64, 24, 96, 233, 215, 14, 43, 181, 113, 32, 141, 16, 218, 199, 33, 81, 127, 11]

S4 = [91, 39, 147, 28, 63, 121, 202, 69, 88, 159, 254, 14, 122, 127, 41, 61, 227, 212, 255, 13, 156, 82, 34, 168, 106, 169, 195, 123, 112, 97, 240, 172, 152, 86, 83, 184, 25, 237, 164, 170, 165, 36, 15, 200, 16, 238, 53, 244, 118, 242, 23, 150, 134, 207, 186, 252, 176, 173, 119, 163, 19, 55, 225, 51, 52, 219, 126, 199, 32, 167, 10, 226, 38, 6, 60, 213, 204, 205, 179, 241, 153, 154, 194, 3, 209, 160, 181, 220, 31, 43, 40, 166, 0, 175, 20, 114, 109, 208, 224, 197, 115, 116, 143, 201, 64, 95, 33, 79, 158, 17, 107, 146, 92, 193, 1, 129, 90, 248, 66, 188, 102, 96, 138, 98, 108, 56, 214, 2, 54, 140, 161, 198, 130, 148, 235, 182, 72, 246, 42, 21, 5, 89, 7, 211, 136, 80, 84, 12, 215, 243, 206, 217, 75, 78, 233, 76, 229, 99, 250, 144, 74, 103, 73, 141, 125, 190, 105, 230, 157, 234, 101, 57, 81, 155, 45, 59, 22, 245, 183, 50, 187, 47, 94, 37, 68, 48, 85, 26, 191, 253, 228, 247, 174, 223, 128, 100, 67, 131, 192, 70, 77, 218, 216, 4, 185, 171, 203, 87, 222, 18, 133, 65, 124, 151, 93, 49, 30, 210, 249, 178, 145, 232, 62, 27, 251, 44, 71, 8, 142, 149, 35, 113, 117, 11, 231, 104, 189, 162, 239, 177, 58, 111, 139, 236, 110, 29, 24, 137, 132, 9, 135, 196, 221, 46, 120, 180]

K1 = [0x3B, 0x07, 0x68, 0x54, 0xC1, 0x5E, 0x58, 0x2D, 0x2B, 0xBB, 0xBD, 0xC8, 0xBC, 0x72, 0x65, 0x54, 0xAE, 0x0F, 0xEA, 0x2F, 0xF9]
K2 = [0xDF, 0xE3, 0x76, 0x4A, 0x86, 0x5F, 0x63, 0xF6, 0xCA, 0xA5, 0x99, 0x0C, 0x24, 0x79, 0xB0, 0x18, 0x59, 0x36, 0x80, 0x35, 0x62]
K3 = [196, 237, 239, 40, 52, 160, 87, 219, 11, 154, 168, 6, 188, 244, 94, 24, 215, 240, 82, 195, 91, 0, 97, 3, 204, 185, 175, 142, 104, 191, 252]
K4 = [144, 14, 21, 137, 209, 62, 18, 115, 246, 159, 23, 15, 79, 192, 238, 213, 179, 47, 193, 231, 149, 61, 124, 1, 46, 90, 202]


C1 = [0x8D, 0xB1, 0xDE, 0xE2, 0x77, 0x4B, 0x92, 0xAE, 0x3B, 0x07, 0x68, 0x54, 0xC1, 0xEB, 0xD1, 0x2F, 0xDA, 0x12, 0xBB, 0x4B, 0xF8]
C2 = [0x19, 0x8C, 0xB0, 0xDF, 0xE3, 0x76, 0x4A, 0x93, 0xAF, 0x3A, 0x06, 0x69, 0x55, 0xC0, 0xFC, 0x78, 0x03, 0xF0, 0x5A, 0x41, 0x25]
C3 = [223, 148, 192, 88, 203, 40, 104, 228, 124, 246, 110, 46, 210, 243, 116, 53, 1, 189, 84, 93, 38, 76, 181, 91, 227, 50, 8, 63, 213, 231, 67, 197]
C4 = [118, 188, 80, 109, 229, 245, 68, 240, 90, 43, 61, 165, 32, 6, 56, 174, 150, 13, 146, 138, 20, 119]


a0 = 0x84
a1 = 0x6f

c0 = 0x2F
c1 = 0x9B
c2 = 0xC3
c3 = 0x7D
c4 = 0x29
c5 = 0xDE
c6 = 0x37
c7 = 0x9F

def F0(input, round):
    output = S1[input ^ K1[round]] ^ C1[round]
    return output
def F1(input, round):
    output = S2[input ^ K2[round]] ^ C2[round]
    return output

def F2(input, round):
    output = S3[input ^ K3[round]] ^ C3[round]
    return output

def F3(input, round):
    output = S4[input ^ K4[round]] ^ C4[round]
    return output

def F(in0, in1, in2, in3, in4, in5, in6, in7, round):
    out0 = in7
    out1 = in0 ^ F3(in7, round)
    out2 = in1 ^ F2(in6, round)
    out3 = in2 ^ F1(in5, round)
    out4 = in3 ^ F0(in4, round)
    out5 = in4
    out6 = in5
    out7 = in6
    return out0, out1, out2, out3, out4, out5, out6, out7


if __name__ == '__main__':
    with open("result.txt", "w") as f:
        pass

    TIMES = 4
    invalid = 0
    for thistime in tqdm(range(TIMES)):
        usednum = []
        while len(usednum) < 256:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        S1 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 256:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        S2 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 256:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        S3 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 256:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        S4 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        K1 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        K2 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        K3 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        K4 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        C1 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        C2 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        C3 = copy.deepcopy(usednum)
        usednum = []
        while len(usednum) < 20:
            num = random.randint(0, 255)
            if num in usednum:
                continue
            else:
                usednum.append(num)
        C4 = copy.deepcopy(usednum)

        start = time.time()
        counter = 0
        for a0 in range(1):
            a0 = random.randint(0, 255)
            for a1 in range(1):
                a1 = random.randint(0, 255)
                if a0 == a1:
                    invalid += 1
                    continue
                c0 = random.randint(0, 255)
                c1 = random.randint(0, 255)
                c2 = random.randint(0, 255)
                c3 = random.randint(0, 255)
                c4 = random.randint(0, 255)
                c5 = random.randint(0, 255)
                c6 = random.randint(0, 255)
                c7 = random.randint(0, 255)
                XVALUEa0 = dict()
                XVALUEa1 = dict()
                for x in range(256):
                    roundout0 = x
                    roundout1 = a0
                    roundout2 = c2
                    roundout3 = c3
                    roundout4 = c4
                    roundout5 = c5
                    roundout6 = c6
                    roundout7 = c7
                    for r in range(10):
                        input0 = roundout0
                        input1 = roundout1
                        input2 = roundout2
                        input3 = roundout3
                        input4 = roundout4
                        input5 = roundout5
                        input6 = roundout6
                        input7 = roundout7
                        roundout0, roundout1, roundout2, roundout3, roundout4, roundout5, roundout6, roundout7 = F(
                            input0, input1, input2, input3, input4, input5, input6, input7, r)
                    XVALUEa0[x] = roundout0

                    roundout0 = x
                    roundout1 = a1
                    roundout2 = c2
                    roundout3 = c3
                    roundout4 = c4
                    roundout5 = c5
                    roundout6 = c6
                    roundout7 = c7
                    for r in range(10):
                        input0 = roundout0
                        input1 = roundout1
                        input2 = roundout2
                        input3 = roundout3
                        input4 = roundout4
                        input5 = roundout5
                        input6 = roundout6
                        input7 = roundout7
                        roundout0, roundout1, roundout2, roundout3, roundout4, roundout5, roundout6, roundout7 = F(
                            input0,
                            input1,
                            input2,
                            input3,
                            input4,
                            input5,
                            input6,
                            input7,
                            r)
                    XVALUEa1[x] = roundout0

                period = -1
                XValuexor = dict()
                for x in XVALUEa0.keys():
                    XValuexor[x] = XVALUEa0[x] ^ XVALUEa1[x]
                for s in range(1, 256):
                    x0 = 0
                    x1 = x0 ^ s
                    out0 = XValuexor[x0]
                    out1 = XValuexor[x1]
                    if out0 == out1:
                        success = 1
                        for x0 in range(1, 256):
                            x1 = x0 ^ s
                            out0 = XValuexor[x0]
                            out1 = XValuexor[x1]
                            if out0 != out1:
                                success = 0
                        if success == 1:
                            counter += 1
                            print("find period")

        # print(time.time()-start)
    print("invalid:{}".format(invalid))
    print("final test number:{}".format(TIMES - invalid))



