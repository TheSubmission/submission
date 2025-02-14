import operation_6bit_word
import os
filename = operation_6bit_word.filename

if __name__ == '__main__':
    with open(filename, 'w') as f:
        f.write('')

    num_R = 4
    num_branch = 4
    num_word = 16
    num_word_per_branch = int(num_word // num_branch)  # 4
    matrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]

    num_pr = num_word - 16
    num_roundfunc = 4
    num_mc = 2


    res = ''
    for r in range(num_R-1):
        operation_6bit_word.generate_round_state(r, num_branch, num_word_per_branch)

        # for showing the distinguisher
        if r == 0 and num_R == 4:
            res += 'ASSERT(x_0_0_0 = 0bin000000);\n'
            res += 'ASSERT(x_0_1_0 = 0bin000000);\n'
            res += 'ASSERT(x_0_2_0 = 0bin000000);\n'
            res += 'ASSERT(x_0_3_0 = 0bin000000);\n'
            res += 'ASSERT(x_1_0_0 = 0bin000000);\n'
            res += 'ASSERT(x_1_1_0 = 0bin000000);\n'
            res += 'ASSERT(x_1_2_0 = 0bin000000);\n'
            res += 'ASSERT(x_1_3_0 = 0bin000000);\n'
            res += 'ASSERT(x_2_0_0 = 0bin000001);\n'
            res += 'ASSERT(x_2_1_0 = 0bin000001);\n'
            res += 'ASSERT(x_2_2_0 = 0bin000000);\n'
            res += 'ASSERT(x_2_3_0 = 0bin000000);\n'
            res += 'ASSERT(x_3_0_0 = 0bin000100);\n'
            res += 'ASSERT(x_3_1_0 = 0bin000100);\n'
            res += 'ASSERT(x_3_2_0 = 0bin000100);\n'
            res += 'ASSERT(x_3_3_0 = 0bin000100);\n'
            res += 'ASSERT(x_1_0_4[5:4] = 0bin01);\n'
            res += 'ASSERT(x_1_1_4[5:4] = 0bin01);\n'
            res += 'ASSERT(x_1_2_4[5:4] = 0bin01);\n'
            res += 'ASSERT(x_1_3_4[5:4] = 0bin01);\n'

        operation_6bit_word.COPY(r, 0, num_word_per_branch)
        operation_6bit_word.ROUNDFUNC(r, 0, num_word_per_branch)
        operation_6bit_word.MC(r, 0, num_word_per_branch, matrix, 0)
        operation_6bit_word.ROUNDFUNC(r, 1, num_word_per_branch)
        for d in range(num_word_per_branch):
            res += 'ASSERT(x_0_%s_%s = COPY_IN_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s_%s = y_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s_%s = ROUNDFUNC_IN_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_0_%s_%s = MC_IN_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(MC_OUT_0_%s_%s = ROUNDFUNC_IN_1_%s_%s);\n' % (str(d), str(r), str(d), str(r))

        operation_6bit_word.XOR(r, 12, num_word_per_branch)
        for d in range(num_word_per_branch):
            res += 'ASSERT(x_1_%s_%s = XOR_IN1_12_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_1_%s_%s = XOR_IN2_12_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(y_1_%s_%s = XOR_OUT_12_%s_%s);\n' % (str(d), str(r), str(d), str(r))

        operation_6bit_word.COPY(r, 1, num_word_per_branch)
        operation_6bit_word.ROUNDFUNC(r, 2, num_word_per_branch)
        operation_6bit_word.MC(r, 1, num_word_per_branch, matrix, 13) 
        operation_6bit_word.ROUNDFUNC(r, 3, num_word_per_branch)
        for d in range(num_word_per_branch):
            res += 'ASSERT(x_2_%s_%s = COPY_IN_1_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(COPY_OUT1_1_%s_%s = y_2_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(COPY_OUT2_1_%s_%s = ROUNDFUNC_IN_2_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_2_%s_%s = MC_IN_1_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(MC_OUT_1_%s_%s = ROUNDFUNC_IN_3_%s_%s);\n' % (str(d), str(r), str(d), str(r))

        operation_6bit_word.XOR(r, 25, num_word_per_branch)
        for d in range(num_word_per_branch):
            res += 'ASSERT(x_3_%s_%s = XOR_IN1_25_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_3_%s_%s = XOR_IN2_25_%s_%s);\n' % (str(d), str(r), str(d), str(r))
            res += 'ASSERT(y_3_%s_%s = XOR_OUT_25_%s_%s);\n' % (str(d), str(r), str(d), str(r))


        #nextround
        res += 'ASSERT(x_0_0_%s = y_1_0_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_0_1_%s = y_1_1_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_0_2_%s = y_3_2_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_0_3_%s = y_3_3_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_1_0_%s = y_2_0_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_1_1_%s = y_2_1_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_1_2_%s = y_0_2_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_1_3_%s = y_0_3_%s);\n' % (str(r + 1), str(r))

        res += 'ASSERT(x_2_0_%s = y_3_0_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_2_1_%s = y_3_1_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_2_2_%s = y_1_2_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_2_3_%s = y_1_3_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_3_0_%s = y_0_0_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_3_1_%s = y_0_1_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_3_2_%s = y_2_2_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_3_3_%s = y_2_3_%s);\n' % (str(r + 1), str(r))


    r = num_R - 1
    operation_6bit_word.generate_round_state(r, num_branch, num_word_per_branch)
    operation_6bit_word.generate_round_state(num_R, num_branch, num_word_per_branch)

    operation_6bit_word.COPY(r, 0, num_word_per_branch)
    operation_6bit_word.ROUNDFUNC(r, 0, num_word_per_branch)
    operation_6bit_word.MC(r, 0, num_word_per_branch, matrix, 0)
    operation_6bit_word.ROUNDFUNC(r, 1, num_word_per_branch)
    for d in range(num_word_per_branch):
        res += 'ASSERT(x_0_%s_%s = COPY_IN_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(COPY_OUT1_0_%s_%s = y_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(COPY_OUT2_0_%s_%s = ROUNDFUNC_IN_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_0_%s_%s = MC_IN_0_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(MC_OUT_0_%s_%s = ROUNDFUNC_IN_1_%s_%s);\n' % (str(d), str(r), str(d), str(r))

    operation_6bit_word.XOR(r, 12, num_word_per_branch)
    for d in range(num_word_per_branch):
        res += 'ASSERT(x_1_%s_%s = XOR_IN1_12_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_1_%s_%s = XOR_IN2_12_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(y_1_%s_%s = XOR_OUT_12_%s_%s);\n' % (str(d), str(r), str(d), str(r))

    operation_6bit_word.COPY(r, 1, num_word_per_branch)
    operation_6bit_word.ROUNDFUNC(r, 2, num_word_per_branch)
    operation_6bit_word.MC(r, 1, num_word_per_branch, matrix, 13)
    operation_6bit_word.ROUNDFUNC(r, 3, num_word_per_branch)
    for d in range(num_word_per_branch):
        res += 'ASSERT(x_2_%s_%s = COPY_IN_1_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(COPY_OUT1_1_%s_%s = y_2_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(COPY_OUT2_1_%s_%s = ROUNDFUNC_IN_2_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_2_%s_%s = MC_IN_1_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(MC_OUT_1_%s_%s = ROUNDFUNC_IN_3_%s_%s);\n' % (str(d), str(r), str(d), str(r))

    operation_6bit_word.XOR(r, 25, num_word_per_branch)
    for d in range(num_word_per_branch):
        res += 'ASSERT(x_3_%s_%s = XOR_IN1_25_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_3_%s_%s = XOR_IN2_25_%s_%s);\n' % (str(d), str(r), str(d), str(r))
        res += 'ASSERT(y_3_%s_%s = XOR_OUT_25_%s_%s);\n' % (str(d), str(r), str(d), str(r))

    # nextround
    res += 'ASSERT(x_0_0_%s = y_1_0_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_0_1_%s = y_1_1_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_0_2_%s = y_3_2_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_0_3_%s = y_3_3_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_1_0_%s = y_2_0_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_1_1_%s = y_2_1_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_1_2_%s = y_0_2_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_1_3_%s = y_0_3_%s);\n' % (str(r + 1), str(r))

    res += 'ASSERT(x_2_0_%s = y_3_0_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_2_1_%s = y_3_1_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_2_2_%s = y_1_2_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_2_3_%s = y_1_3_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_3_0_%s = y_0_0_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_3_1_%s = y_0_1_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_3_2_%s = y_2_2_%s);\n' % (str(r + 1), str(r))
    res += 'ASSERT(x_3_3_%s = y_2_3_%s);\n' % (str(r + 1), str(r))

    with open(filename, 'a') as f:
        f.write(res)

    operation_6bit_word.END(r, num_branch, num_word_per_branch)


    str_num_pr = '0bin' + bin(num_pr)[2:].zfill(10)
    res = 'ASSERT(BVLE(BVPLUS(10'
    for r in range(num_R):
        for i in range(26):
            if i == 12 or i == 25:
                for d in range(num_word_per_branch):
                    res += ',0bin000000000@XOR_key_%s_%s_%s' % (str(i), str(d), str(r))
            else:
                res += ',0bin000000000@XOR_key_%s_0_%s' % (str(i), str(r))
    res += '), %s ));\n' % str_num_pr

    with open(filename, 'a') as f:
        f.write(res)

    operation_6bit_word.period_SUM(num_R, num_roundfunc, num_mc)

    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')
