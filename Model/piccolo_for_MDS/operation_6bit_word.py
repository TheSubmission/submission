filename = 'model2.cvc'


def KEY_SUM(sum_r, sum_xor, num_word_per_branch, num_pr):
    str_num_pr = '0bin' + bin(num_pr)[2:].zfill(10)
    res = 'ASSERT(BVLE(BVPLUS(10'
    for r in range(sum_r):
        for i in range(sum_xor):
            for d in range(num_word_per_branch):
                res += ',0bin000000000@XOR_key_%s_%s_%s' % (str(i), str(d), str(r))
    res += '), %s ));\n' % str_num_pr

    with open(filename, 'a') as f:
        f.write(res)

    return 0

# limiting the rule of R to occur at most 4 times
def period_SUM(sum_r, sum_roundfunc, num_word_per_branch):
    res = 'ASSERT(BVLE(BVPLUS(10'
    for r in range(sum_r):
        for i in range(sum_roundfunc):
            for d in range(num_word_per_branch):
                res += ',0bin000000000@period_%s_%s_%s' % (str(i), str(d), str(r))
    res += '), 0bin0000000100 ));\n'

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def define_value(name, num_branch, num_r, num_word_per_branch):
    res = '%s_%s_%s_%s : BITVECTOR(6);\n' % (name, str(num_branch), str(num_word_per_branch), str(num_r))
    return res

def define_value_linear(name, num_branch, num_r, num_word_per_branch):
    res = '%s_%s_%s_%s : BITVECTOR(1);\n' % (name, str(num_branch), str(num_word_per_branch), str(num_r))
    return res

def generate_round_state(num_r, num_branch, num_word_per_branch):
    res = ''
    for i in range(num_branch):
        for d in range(num_word_per_branch):
            res += define_value('x', i, num_r, d)
            res += define_value('y', i, num_r, d)
    if num_r == 0:
        res += 'end : BITVECTOR(1);\n'
        res += 'ASSERT(end = 0bin1);\n'

        for i in range(num_branch):
            for d in range(num_word_per_branch):
                res += 'ASSERT(x_%s_%s_%s[5:5] | x_%s_%s_%s[4:4] | x_%s_%s_%s[3:3] | x_%s_%s_%s[1:1] = 0bin0);\n' % (str(i), str(d), str(num_r), str(i), str(d), str(num_r), str(i), str(d), str(num_r), str(i), str(d), str(num_r))

        tmp = ''
        for i in range(num_branch):
            for d in range(num_word_per_branch):
                tmp += '(x_%s_%s_0 = 0bin000001) OR ' % (str(i), str(d))
        tmp = tmp[:-4:]
        res += 'ASSERT(' + tmp + ');\n'


        tmp = ''
        for i in range(num_branch):
            for d in range(num_word_per_branch):
                tmp += '(x_%s_%s_0 = 0bin000100) OR ' % (str(i), str(d))
        tmp = tmp[:-4:]
        res += 'ASSERT(' + tmp + ');\n'



    with open(filename, 'a') as f:
        f.write(res)


def XOR(num_r, num_xor, num_word_per_branch):
    res = ''
    for d in range(num_word_per_branch):
        res += define_value('XOR_IN1', num_xor, num_r, d)
        res += define_value('XOR_IN2', num_xor, num_r, d)
        res += define_value('XOR_OUT', num_xor, num_r, d)
        res += define_value_linear('XOR_key', num_xor, num_r, d)


    for d in range(num_word_per_branch):
        # ?:out[5] =  in1[5] or in2[5]
        res += 'ASSERT(XOR_OUT_%s_%s_%s[5:5] = XOR_IN1_%s_%s_%s[5:5] | XOR_IN2_%s_%s_%s[5:5]);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # R(0s):out[4] =  in1[4] or in2[4]
        res += 'ASSERT(XOR_OUT_%s_%s_%s[4:4] = XOR_IN1_%s_%s_%s[4:4] | XOR_IN2_%s_%s_%s[4:4]);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # R(x):out[3] =  in1[3] or in2[3]
        res += 'ASSERT(XOR_OUT_%s_%s_%s[3:3] = XOR_IN1_%s_%s_%s[3:3] | XOR_IN2_%s_%s_%s[3:3]);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # x:out[2] =  in1[2] ^ in2[2]
        res += 'ASSERT(XOR_OUT_%s_%s_%s[2:2] = BVXOR(XOR_IN1_%s_%s_%s[2:2] , XOR_IN2_%s_%s_%s[2:2]));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

 
        # 00+00 = 00
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s_%s[1:0] = 0bin00 => XOR_OUT_%s_%s_%s[1:0] = 0bin00);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 00+01 = 01
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s_%s[1:0] = 0bin01 => XOR_OUT_%s_%s_%s[1:0] = 0bin01);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s[1:0] = 0bin00 AND XOR_IN1_%s_%s_%s[1:0] = 0bin01 => XOR_OUT_%s_%s_%s[1:0] = 0bin01);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 00+10 = 10
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s_%s[1:0] = 0bin10 => XOR_OUT_%s_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s[1:0] = 0bin00 AND XOR_IN1_%s_%s_%s[1:0] = 0bin10 => XOR_OUT_%s_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 00+11 = 11
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s_%s[1:0] = 0bin11);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s[1:0] = 0bin00 AND XOR_IN1_%s_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s_%s[1:0] = 0bin11);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 01+01 = 00
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin01 AND XOR_IN2_%s_%s_%s[1:0] = 0bin01 => XOR_OUT_%s_%s_%s[1:0] = 0bin00);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 01+10 = 11+k=0 or 00+k=1
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin01 AND XOR_IN2_%s_%s_%s[1:0] = 0bin10 => (XOR_OUT_%s_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s_%s = 0bin0) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s_%s = 0bin1));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s[1:0] = 0bin01 AND XOR_IN1_%s_%s_%s[1:0] = 0bin10 => (XOR_OUT_%s_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s_%s = 0bin0) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s_%s = 0bin1));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 01+11 = 10
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin01 AND XOR_IN2_%s_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s[1:0] = 0bin01 AND XOR_IN1_%s_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 10+10 = 10+k=0 or 00+k=1
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin10 AND XOR_IN2_%s_%s_%s[1:0] = 0bin10 => (XOR_OUT_%s_%s_%s[1:0] = 0bin10 AND XOR_key_%s_%s_%s = 0bin0) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s_%s = 0bin1));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 10+11 = 11+k=0 or 01+k=1 or 00+k=1
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin10 AND XOR_IN2_%s_%s_%s[1:0] = 0bin11 => (XOR_OUT_%s_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s_%s = 0bin0) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin01 AND XOR_key_%s_%s_%s = 0bin1) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s_%s = 0bin1));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s[1:0] = 0bin10 AND XOR_IN1_%s_%s_%s[1:0] = 0bin11 => (XOR_OUT_%s_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s_%s = 0bin0) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin01 AND XOR_key_%s_%s_%s = 0bin1) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s_%s = 0bin1));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

        # 11+11 = 10+k=0 or 00+k=1
        res += 'ASSERT(XOR_IN1_%s_%s_%s[1:0] = 0bin11 AND XOR_IN2_%s_%s_%s[1:0] = 0bin11 => (XOR_OUT_%s_%s_%s[1:0] = 0bin10 AND XOR_key_%s_%s_%s = 0bin0) OR (XOR_OUT_%s_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s_%s = 0bin1));\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0



def XOR_linear(num_r, num_xor, num_word_per_branch):
    res = ''
    for d in range(num_word_per_branch):
        res += define_value_linear('XOR_IN1', num_xor, num_r, d)
        res += define_value_linear('XOR_IN2', num_xor, num_r, d)
        res += define_value_linear('XOR_OUT', num_xor, num_r, d)

        res += 'ASSERT(XOR_IN1_%s_%s_%s = XOR_IN2_%s_%s_%s);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))
        res += 'ASSERT(XOR_IN2_%s_%s_%s = XOR_OUT_%s_%s_%s);\n' % (str(num_xor), str(d), str(num_r), str(num_xor), str(d), str(num_r))


    with open(filename,'a') as f:
        f.write(res)

    return 0


def ROUNDFUNC(num_r, num_roundfunc, num_word_per_branch):
    res = ''
    for d in range(num_word_per_branch):
        res += define_value('ROUNDFUNC_IN', num_roundfunc, num_r, d)
        res += define_value('ROUNDFUNC_OUT', num_roundfunc, num_r, d)
        res += define_value_linear('period', num_roundfunc, num_r, d)

        res += 'ASSERT(IF ROUNDFUNC_IN_%s_%s_%s = 0bin000000 THEN ROUNDFUNC_OUT_%s_%s_%s = 0bin000000 ELSE (IF ROUNDFUNC_IN_%s_%s_%s = 0bin010000 THEN ROUNDFUNC_OUT_%s_%s_%s = 0bin010000 ELSE (IF ROUNDFUNC_IN_%s_%s_%s = 0bin000100 OR ROUNDFUNC_IN_%s_%s_%s = 0bin001000 OR ROUNDFUNC_IN_%s_%s_%s = 0bin001100 THEN ROUNDFUNC_OUT_%s_%s_%s = 0bin001000 ELSE (IF ROUNDFUNC_IN_%s_%s_%s = 0bin000001 OR ROUNDFUNC_IN_%s_%s_%s = 0bin000010 OR ROUNDFUNC_IN_%s_%s_%s = 0bin000011 THEN ROUNDFUNC_OUT_%s_%s_%s = 0bin000010 ELSE (IF ROUNDFUNC_IN_%s_%s_%s = 0bin000101 OR ROUNDFUNC_IN_%s_%s_%s = 0bin000110 OR ROUNDFUNC_IN_%s_%s_%s = 0bin000111 THEN (ROUNDFUNC_OUT_%s_%s_%s = 0bin010000 AND period_%s_%s_%s = 0bin1) OR (ROUNDFUNC_OUT_%s_%s_%s = 0bin100000 AND period_%s_%s_%s = 0bin0) ELSE ROUNDFUNC_OUT_%s_%s_%s = 0bin100000 ENDIF) ENDIF) ENDIF) ENDIF) ENDIF);\n' % (str(num_roundfunc), str(d), str(num_r),str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r), str(num_roundfunc), str(d), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0

def COPY(num_r, num_copy, num_word_per_branch):

    res = ''
    for d in range(num_word_per_branch):
        res += define_value('COPY_IN', num_copy, num_r, d)
        res += define_value('COPY_OUT1', num_copy, num_r, d)
        res += define_value('COPY_OUT2', num_copy, num_r, d)

        res += 'ASSERT(COPY_OUT1_%s_%s_%s = COPY_IN_%s_%s_%s);\n' %(str(num_copy), str(d), str(num_r), str(num_copy), str(d), str(num_r))
        res += 'ASSERT(COPY_OUT2_%s_%s_%s = COPY_IN_%s_%s_%s);\n' %(str(num_copy), str(d), str(num_r), str(num_copy), str(d), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def MC(num_r, num_mc, num_word_per_branch, matrix, num_xor):
    res = ''

    num_col = int(num_word_per_branch//4)

    for d in range(num_word_per_branch):
        res += define_value('MC_IN', num_mc, num_r, d)
        res += define_value('MC_OUT', num_mc, num_r, d)

    for i in range(12*num_col):
        XOR(num_r, num_xor+i, 1)
    for d in range(num_col):
        tmp = 'ASSERT(BVLE(BVPLUS(10'
        for i in range(12):
            tmp += ',0bin000000000@XOR_key_{0}_{1}_{2}'.format(str(num_xor+i), str(0), str(num_r))
        tmp += '), 0bin0000000001 ));\n'
        res += tmp
        #res += '%TAG!!;\n'

    for d in range(num_col):
        for i in range(16):
            res += define_value('TMP%s', num_mc, num_r, i) % str(d)
            res += define_value_linear('period%s', num_mc, num_r, i) % str(d)


        for row in range(4):
            for col in range(4):
                if matrix[row][col] == 0:
                    res += 'ASSERT(TMP%s_%s_%s_%s = 0bin000000);\n' % (str(d), str(num_mc), str(4*row+col), str(num_r))
                elif matrix[row][col] == 1:
                    res += 'ASSERT(TMP%s_%s_%s_%s = MC_IN_%s_%s_%s);\n' % (str(d), str(num_mc), str(4*row+col), str(num_r), str(num_mc), str(4*d+col), str(num_r))

                else:

                    res += 'ASSERT(MC_IN_{0}_{1}_{2} = 0bin000000 => TMP{3}_{0}_{4}_{2} = 0bin000000);\n'.format(str(num_mc),str(4*d+col),str(num_r),str(d),str(4*row+col))
                    res += 'ASSERT(MC_IN_{0}_{1}_{2} = 0bin010000 => TMP{3}_{0}_{4}_{2} = 0bin010000);\n'.format(str(num_mc),str(4*d+col),str(num_r),str(d),str(4*row+col))
                    res += 'ASSERT(MC_IN_{0}_{1}_{2} = 0bin000100 OR MC_IN_{0}_{1}_{2} = 0bin001000 OR MC_IN_{0}_{1}_{2} = 0bin001100 => TMP{3}_{0}_{4}_{2} = 0bin001000);\n'.format(str(num_mc),str(4*d+col),str(num_r),str(d),str(4*row+col))
                    res += 'ASSERT(MC_IN_{0}_{1}_{2} = 0bin000001 OR MC_IN_{0}_{1}_{2} = 0bin000010 OR MC_IN_{0}_{1}_{2} = 0bin000011 => TMP{3}_{0}_{4}_{2} = 0bin000010);\n'.format(str(num_mc),str(4*d+col),str(num_r),str(d),str(4*row+col))
                    res += 'ASSERT(MC_IN_{0}_{1}_{2} = 0bin000101 OR MC_IN_{0}_{1}_{2} = 0bin000110 OR MC_IN_{0}_{1}_{2} = 0bin000111 => (TMP{3}_{0}_{4}_{2} = 0bin010000 AND period{3}_{0}_{4}_{2} = 0bin1) OR (TMP{3}_{0}_{4}_{2} = 0bin100000 AND period{3}_{0}_{4}_{2} = 0bin0));\n'.format(str(num_mc),str(4*d+col),str(num_r),str(d),str(4*row+col))
                    res += 'ASSERT(MC_IN_{0}_{1}_{2} /= 0bin000000 AND MC_IN_{0}_{1}_{2} /= 0bin010000 AND MC_IN_{0}_{1}_{2} /= 0bin000100 AND MC_IN_{0}_{1}_{2} /= 0bin001000 AND MC_IN_{0}_{1}_{2} /= 0bin001100 AND MC_IN_{0}_{1}_{2} /= 0bin000001 AND MC_IN_{0}_{1}_{2} /= 0bin000010 AND MC_IN_{0}_{1}_{2} /= 0bin000011 AND MC_IN_{0}_{1}_{2} /= 0bin000101 AND MC_IN_{0}_{1}_{2} /= 0bin000110 AND MC_IN_{0}_{1}_{2} /= 0bin000111 => TMP{3}_{0}_{4}_{2} = 0bin100000);\n'.format(str(num_mc),str(4*d+col),str(num_r),str(d),str(4*row+col))


        for row in range(4):
            res += 'ASSERT(XOR_IN1_%s_0_%s = TMP%s_%s_%s_%s);\n' % (str(num_xor + row * 3 + d * 12), str(num_r), str(d), str(num_mc), str(row * 4), str(num_r))
            res += 'ASSERT(XOR_IN2_%s_0_%s = TMP%s_%s_%s_%s);\n' % (str(num_xor + row * 3 + d * 12), str(num_r), str(d), str(num_mc), str(row * 4 + 1), str(num_r))
            res += 'ASSERT(XOR_IN1_%s_0_%s = XOR_OUT_%s_0_%s);\n' % (str(num_xor + row * 3 + 1 + d * 12), str(num_r), str(num_xor + row * 3 + d * 12), str(num_r))
            res += 'ASSERT(XOR_IN2_%s_0_%s = TMP%s_%s_%s_%s);\n' % (str(num_xor + row * 3 + 1 + d * 12), str(num_r), str(d), str(num_mc), str(row * 4 + 2), str(num_r))
            res += 'ASSERT(XOR_IN1_%s_0_%s = XOR_OUT_%s_0_%s);\n' % (str(num_xor + row * 3 + 2 + d * 12), str(num_r), str(num_xor + row * 3 + 1 + d * 12), str(num_r))
            res += 'ASSERT(XOR_IN2_%s_0_%s = TMP%s_%s_%s_%s);\n' % (str(num_xor + row * 3 + 2 + d * 12), str(num_r), str(d), str(num_mc), str(row * 4 + 3), str(num_r))
            res += 'ASSERT(MC_OUT_%s_%s_%s = XOR_OUT_%s_0_%s);\n' % (str(num_mc), str(d * 4 + row), str(num_r), str(num_xor + row * 3 + 2 + d * 12), str(num_r))


    with open(filename, 'a') as f:
        f.write(res)

    return 0


def END(end_r, num_branch, num_word_per_branch):
    res = 'ASSERT('
    for i in range(num_branch):
        for d in range(num_word_per_branch):
            res += '(y_%s_%s_%s = 0bin000110) OR (y_%s_%s_%s = 0bin000111) OR (y_%s_%s_%s[5:4] = 0bin01) OR ' % (str(i), str(d), str(end_r), str(i), str(d), str(end_r), str(i), str(d), str(end_r))
    res = res[:-4:]
    res += ');\n'
    res += '%tag;\n'

    with open(filename,'a') as f:
        f.write(res)

    return 0



if __name__ == '__main__':
    with open(filename,'w') as f:
        f.write('')

    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')
