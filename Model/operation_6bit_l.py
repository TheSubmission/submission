
filename = 'model2.cvc'

# calculating the number of collisions
def KEY_SUM(sum_r, sum_xor, num_pr):
    str_num_pr = '0bin' + bin(num_pr)[2:].zfill(10)
    res = 'ASSERT(BVLE(BVPLUS(10'
    for r in range(sum_r):
        for i in range(sum_xor):
            res += ',0bin000000000@XOR_key_%s_%s' % (str(i), str(r))
    res += '), %s ));\n' % str_num_pr

    with open(filename, 'a') as f:
        f.write(res)

    return 0

# limiting the number of the rule of R: x+a, x+R(x), x+R(a)+a -> 0s
def period_SUM(sum_r, sum_roundfunc):
    res = 'ASSERT(BVLE(BVPLUS(10'
    for r in range(sum_r):
        for i in range(sum_roundfunc):
            res += ',0bin000000000@period_%s_%s' % (str(i), str(r))
    res += '), 0bin0000000001 ));\n'

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def initial(r, num_branch):
    res = ''
    for d in range(num_branch):
        res += '%s_%s_%s : BITVECTOR(1);\n' % ("xlinearfirstmask", str(d), str(r))
    res += "MASKSUM: BITVECTOR(6);\n"
    res += "ASSERT(MASKSUM = 0bin000001);\n"
    res += 'ASSERT(MASKSUM = BVPLUS(6, '
    for d in range(num_branch - 1):
        res += '0bin00000@%s_%s_%s, ' % ("xlinearfirstmask", str(d), str(r))
    res += '0bin00000@%s_%s_%s));\n' % ("xlinearfirstmask", str(num_branch - 1), str(r))

    for d in range(num_branch):
        res += 'ASSERT((NOT(x_{0}_{1} = 0bin000110) AND NOT(x_{0}_{1} = 0bin000111) AND NOT(x_{0}_{1}[5:4] = 0bin01)) => xlinearfirstmask_{0}_{1} = 0bin0);\n'.format(d, r)

    for d in range(num_branch):
        res += "ASSERT(xlinearfirstmask_{0}_{1} = 0bin1) => (xlinear_{0}_{1}[0:0] = 0bin1);\n".format(d, r)

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def define_value(name, d, num_r):
    res = '%s_%s_%s : BITVECTOR(6);\n' % (name, str(d), str(num_r))
    return res

def define_value_linear(name, d, num_r):
    res = '%s_%s_%s : BITVECTOR(1);\n' % (name, str(d), str(num_r))
    return res

def generate_round_state(num_r, num_branch, use_x_a=0):
    res = ''
    for d in range(num_branch):
        res += define_value('x', d, num_r)
        res += define_value('y', d, num_r)

    # initial constraints
    if num_r == 0:
        res += 'end : BITVECTOR(1);\n'
        res += 'ASSERT(end = 0bin1);\n'

        for d in range(num_branch):
            res += 'ASSERT(x_%s_%s[5:5] | x_%s_%s[4:4] | x_%s_%s[3:3] | x_%s_%s[1:1] = 0bin0);\n' % (str(d), str(num_r), str(d), str(num_r), str(d), str(num_r), str(d), str(num_r))

        tmp = ''
        for d in range(num_branch - 1):
            tmp += '(x_%s_0 = 0bin000001) OR ' % str(d)
        tmp += '(x_%s_0 = 0bin000001)' % str(num_branch - 1)
        res += 'ASSERT(' + tmp + ');\n'

        # we can choose use x or x+a in the first round
        if use_x_a == 1:
            tmp = ''
            for d in range(num_branch - 1):
                tmp += '(x_%s_0 = 0bin000100) OR (x_%s_0 = 0bin000101) OR ' % (str(d), str(d))
            tmp += '(x_%s_0 = 0bin000100) OR (x_%s_0 = 0bin000101)' % (str(num_branch - 1), str(num_branch - 1))
            res += 'ASSERT(' + tmp + ');\n'
        else:
            tmp = ''
            for d in range(num_branch - 1):
                tmp += '(x_%s_0 = 0bin000100) OR' % str(d)
            tmp += '(x_%s_0 = 0bin000100)' % str(num_branch - 1)
            res += 'ASSERT(' + tmp + ');\n'

        for d in range(num_branch):
            res += define_value_linear('tag', d, 0)
            res += 'ASSERT(x_%s_0 = 0bin000100 OR x_%s_0 = 0bin000101 => tag_%s_0 = 0bin1);\n' % (str(d), str(d), str(d))

        res += 'ASSERT(BVLE(BVPLUS(10'
        for r in range(1):
            for d in range(num_branch):
                res += ',0bin000000000@tag_%s_%s' % (str(d), str(r))
        res += '), 0bin0000000001 ));\n'

    with open(filename, 'a') as f:
        f.write(res)


def generate_round_state_linear(num_r_linear, num_branch):
    res = ''
    for d in range(num_branch):
        res += define_value_linear('xlinear', d, num_r_linear)
        res += define_value_linear('ylinear', d, num_r_linear)
    tmp = ''
    for d in range(num_branch):
        tmp += '(xlinear_%s_%s = 0bin0) AND ' % (str(d), str(num_r_linear))
    res += 'ASSERT(' + tmp[:-5:] + ' => end = 0bin0);\n'

    tmp = ''
    for d in range(num_branch):
        tmp += '(ylinear_%s_%s = 0bin0) AND ' % (str(d), str(num_r_linear))
    res += 'ASSERT(' + tmp[:-5:] + ' => end = 0bin0);\n'

    with open(filename,'a') as f:
        f.write(res)

    return 0



def XOR(num_r, num_xor):
    res = ''
    res += define_value('XOR_IN1', num_xor, num_r)
    res += define_value('XOR_IN2', num_xor, num_r)
    res += define_value('XOR_OUT', num_xor, num_r)
    res += define_value_linear('XOR_key', num_xor, num_r)

    # ?:out[5] =  in1[5] or in2[5]
    res += 'ASSERT(XOR_OUT_%s_%s[5:5] = XOR_IN1_%s_%s[5:5] | XOR_IN2_%s_%s[5:5]);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # R(0s):out[4] =  in1[4] or in2[4]
    res += 'ASSERT(XOR_OUT_%s_%s[4:4] = XOR_IN1_%s_%s[4:4] | XOR_IN2_%s_%s[4:4]);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # R(x):out[3] =  in1[3] or in2[3]
    res += 'ASSERT(XOR_OUT_%s_%s[3:3] = XOR_IN1_%s_%s[3:3] | XOR_IN2_%s_%s[3:3]);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # x:out[2] =  in1[2] ^ in2[2]
    res += 'ASSERT(XOR_OUT_%s_%s[2:2] = BVXOR(XOR_IN1_%s_%s[2:2] , XOR_IN2_%s_%s[2:2]));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 00+00 = 00
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s[1:0] = 0bin00 => XOR_OUT_%s_%s[1:0] = 0bin00);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 00+01 = 01
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s[1:0] = 0bin01 => XOR_OUT_%s_%s[1:0] = 0bin01);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
    res += 'ASSERT(XOR_IN2_%s_%s[1:0] = 0bin00 AND XOR_IN1_%s_%s[1:0] = 0bin01 => XOR_OUT_%s_%s[1:0] = 0bin01);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 00+10 = 10
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s[1:0] = 0bin10 => XOR_OUT_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
    res += 'ASSERT(XOR_IN2_%s_%s[1:0] = 0bin00 AND XOR_IN1_%s_%s[1:0] = 0bin10 => XOR_OUT_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 00+11 = 11
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin00 AND XOR_IN2_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s[1:0] = 0bin11);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
    res += 'ASSERT(XOR_IN2_%s_%s[1:0] = 0bin00 AND XOR_IN1_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s[1:0] = 0bin11);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 01+01 = 00
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin01 AND XOR_IN2_%s_%s[1:0] = 0bin01 => XOR_OUT_%s_%s[1:0] = 0bin00);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 01+10 = 11+k=0 or 00+k=1
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin01 AND XOR_IN2_%s_%s[1:0] = 0bin10 => (XOR_OUT_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s = 0bin0) OR (XOR_OUT_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s = 0bin1));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
    res += 'ASSERT(XOR_IN2_%s_%s[1:0] = 0bin01 AND XOR_IN1_%s_%s[1:0] = 0bin10 => (XOR_OUT_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s = 0bin0) OR (XOR_OUT_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s = 0bin1));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 01+11 = 10
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin01 AND XOR_IN2_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
    res += 'ASSERT(XOR_IN2_%s_%s[1:0] = 0bin01 AND XOR_IN1_%s_%s[1:0] = 0bin11 => XOR_OUT_%s_%s[1:0] = 0bin10);\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 10+10 = 10+k=0 or 00+k=1
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin10 AND XOR_IN2_%s_%s[1:0] = 0bin10 => (XOR_OUT_%s_%s[1:0] = 0bin10 AND XOR_key_%s_%s = 0bin0) OR (XOR_OUT_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s = 0bin1));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 10+11 = 11+k=0 or 01+k=1 or 00+k=1
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin10 AND XOR_IN2_%s_%s[1:0] = 0bin11 => (XOR_OUT_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s = 0bin0) OR (XOR_OUT_%s_%s[1:0] = 0bin01 AND XOR_key_%s_%s = 0bin1) OR (XOR_OUT_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s = 0bin1));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))
    res += 'ASSERT(XOR_IN2_%s_%s[1:0] = 0bin10 AND XOR_IN1_%s_%s[1:0] = 0bin11 => (XOR_OUT_%s_%s[1:0] = 0bin11 AND XOR_key_%s_%s = 0bin0) OR (XOR_OUT_%s_%s[1:0] = 0bin01 AND XOR_key_%s_%s = 0bin1) OR (XOR_OUT_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s = 0bin1));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    # 11+11 = 10+k=0 or 00+k=1
    res += 'ASSERT(XOR_IN1_%s_%s[1:0] = 0bin11 AND XOR_IN2_%s_%s[1:0] = 0bin11 => (XOR_OUT_%s_%s[1:0] = 0bin10 AND XOR_key_%s_%s = 0bin0) OR (XOR_OUT_%s_%s[1:0] = 0bin00 AND XOR_key_%s_%s = 0bin1));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0



def XOR_linear(num_r, num_xor):
    res = ''
    res += define_value_linear('XOR_IN1', num_xor, num_r)
    res += define_value_linear('XOR_IN2', num_xor, num_r)
    res += define_value_linear('XOR_OUT', num_xor, num_r)

    res += 'ASSERT(XOR_OUT_%s_%s[0:0] = (XOR_IN1_%s_%s[0:0] & XOR_IN2_%s_%s[0:0]));\n' % (str(num_xor), str(num_r), str(num_xor), str(num_r), str(num_xor), str(num_r))

    with open(filename,'a') as f:
        f.write(res)

    return 0


def ROUNDFUNC(num_r, num_roundfunc):
    res = ''
    res += define_value('ROUNDFUNC_IN', num_roundfunc, num_r)
    res += define_value('ROUNDFUNC_OUT', num_roundfunc, num_r)
    res += define_value_linear('period', num_roundfunc, num_r)

    res += 'ASSERT(IF ROUNDFUNC_IN_%s_%s = 0bin000000 THEN ROUNDFUNC_OUT_%s_%s = 0bin000000 ELSE (IF ROUNDFUNC_IN_%s_%s = 0bin010000 THEN ROUNDFUNC_OUT_%s_%s = 0bin010000 ELSE (IF ROUNDFUNC_IN_%s_%s = 0bin000100 OR ROUNDFUNC_IN_%s_%s = 0bin001000 OR ROUNDFUNC_IN_%s_%s = 0bin001100 THEN ROUNDFUNC_OUT_%s_%s = 0bin001000 ELSE (IF ROUNDFUNC_IN_%s_%s = 0bin000001 OR ROUNDFUNC_IN_%s_%s = 0bin000010 OR ROUNDFUNC_IN_%s_%s = 0bin000011 THEN ROUNDFUNC_OUT_%s_%s = 0bin000010 ELSE (IF ROUNDFUNC_IN_%s_%s = 0bin000101 OR ROUNDFUNC_IN_%s_%s = 0bin000110 OR ROUNDFUNC_IN_%s_%s = 0bin000111 THEN (ROUNDFUNC_OUT_%s_%s = 0bin010000 AND period_%s_%s = 0bin1) OR (ROUNDFUNC_OUT_%s_%s = 0bin100000 AND period_%s_%s = 0bin0) ELSE ROUNDFUNC_OUT_%s_%s = 0bin100000 ENDIF) ENDIF) ENDIF) ENDIF) ENDIF);\n' % (str(num_roundfunc), str(num_r),str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r), str(num_roundfunc), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def ROUNDFUNC_linear(num_r, num_roundfunc):
    res = ''
    res += define_value_linear('ROUNDFUNC_IN', num_roundfunc, num_r)
    res += define_value_linear('ROUNDFUNC_OUT', num_roundfunc, num_r)

    res += 'ASSERT(ROUNDFUNC_OUT_%s_%s = 0bin0);\n' % (str(num_roundfunc), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def COPY(num_r, num_copy):
    res = ''
    res += define_value('COPY_IN', num_copy, num_r)
    res += define_value('COPY_OUT1', num_copy, num_r)
    res += define_value('COPY_OUT2', num_copy, num_r)

    res += 'ASSERT(COPY_OUT1_%s_%s = COPY_IN_%s_%s);\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r))
    res += 'ASSERT(COPY_OUT2_%s_%s = COPY_IN_%s_%s);\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0


def COPY_linear(num_r, num_copy):
    res = ''
    res += define_value_linear('COPY_IN', num_copy, num_r)
    res += define_value_linear('COPY_OUT1', num_copy, num_r)
    res += define_value_linear('COPY_OUT2', num_copy, num_r)

    res += 'ASSERT((COPY_IN_%s_%s = COPY_OUT1_%s_%s) AND (COPY_IN_%s_%s = COPY_OUT2_%s_%s));\n' % (str(num_copy), str(num_r), str(num_copy), str(num_r), str(num_copy), str(num_r), str(num_copy), str(num_r))

    with open(filename, 'a') as f:
        f.write(res)

    return 0

def END(end_r, num_branch):
    res = 'ASSERT('
    for d in range(num_branch-1):
        res += '(y_%s_%s = 0bin000110) OR (y_%s_%s = 0bin000111) OR (y_%s_%s[5:4] = 0bin01)' % (str(d), str(end_r), str(d), str(end_r), str(d), str(end_r))
        res += ' OR '
    d = num_branch-1
    res += '(y_%s_%s = 0bin000110) OR (y_%s_%s = 0bin000111) OR (y_%s_%s[5:4] = 0bin01));\n' % (str(d), str(end_r), str(d), str(end_r), str(d), str(end_r))

    with open(filename,'a') as f:
        f.write(res)

    return 0






if __name__ == '__main__':
    with open(filename,'w') as f:
        f.write('')

    generate_round_state(0, 4)
    generate_round_state(1, 4)


    XOR(1,3)
    ROUNDFUNC(0, 0)
    END(1, 4)
    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')
