import operation_6bit_l
import os

filename = operation_6bit_l.filename

if __name__ == '__main__':
    with open(filename, 'w') as f:
        f.write('')

    num_branch = 4

    num_R_color = 14
    num_R_linear = 1 # there is one round combination of the tail.
    rA_begin = 4 #begin with the ?-th rule of Function A.

    num_R_sum = num_R_color
    num_pr = num_branch - 4
    num_xor = 1
    num_roundfunc = 1


    res = ''

    operation_6bit_l.generate_round_state(0, num_branch)

    # for showing the distinguisher: AAAABBBBBBBBA...
    if num_R_color == 14:
        res += 'ASSERT(x_0_0 = 0bin000000);\n'
        res += 'ASSERT(x_1_0 = 0bin000000);\n'
        res += 'ASSERT(x_2_0 = 0bin000001);\n'
        res += 'ASSERT(x_3_0 = 0bin000100);\n'

    for r in range(num_R_color):
        operation_6bit_l.generate_round_state(r+1, num_branch)
        # skipjackA
        if r in range(rA_begin) or r in range(rA_begin+8, rA_begin+16):
            operation_6bit_l.ROUNDFUNC(r, 0)
            operation_6bit_l.COPY(r, 0)
            res += 'ASSERT(x_0_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_0_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s = y_0_%s);\n'% (str(r), str(r))

            operation_6bit_l.XOR(r, 0)
            res += 'ASSERT(x_1_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(y_1_%s = XOR_OUT_0_%s);\n' % (str(r), str(r))

            res += 'ASSERT(x_2_%s = y_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(x_3_%s = y_3_%s);\n' % (str(r), str(r))

        # skipjackB
        if r in range(rA_begin, rA_begin+8) or r in range(rA_begin+16, rA_begin+24):
            operation_6bit_l.ROUNDFUNC(r, 0)
            operation_6bit_l.COPY(r, 0)
            res += 'ASSERT(x_0_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_0_%s = y_0_%s);\n' % (str(r), str(r))

            operation_6bit_l.XOR(r, 0)
            res += 'ASSERT(x_3_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s= XOR_IN2_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(y_3_%s = XOR_OUT_0_%s);\n' % (str(r), str(r))

            res += 'ASSERT(x_1_%s = y_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(x_2_%s = y_2_%s);\n' % (str(r), str(r))

        #nextround:
        for i in range(num_branch):
            res += 'ASSERT(x_%s_%s = y_%s_%s);\n' % (str(i), str(r+1), str((i+1) % num_branch), str(r))

    operation_6bit_l.generate_round_state_linear(num_R_color, num_branch)
    #operation_6bit_l.initial(num_R_color, num_branch)
    for r in range(num_R_color, num_R_linear+num_R_color):
        operation_6bit_l.generate_round_state_linear(r+1, num_branch)
        if r == num_R_color:
            operation_6bit_l.initial(r, num_branch)

        # skipjackA
        if r in range(rA_begin) or r in range(rA_begin+8, rA_begin+16):
            operation_6bit_l.ROUNDFUNC_linear(r, 0)
            operation_6bit_l.COPY_linear(r, 0)
            res += 'ASSERT(ylinear_0_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_0_%s = xlinear_0_%s);\n' % (str(r), str(r))

            operation_6bit_l.XOR_linear(r, 0)
            res += 'ASSERT(ylinear_1_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(xlinear_1_%s = XOR_OUT_0_%s);\n' % (str(r), str(r))

            res += 'ASSERT(ylinear_2_%s = xlinear_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ylinear_3_%s = xlinear_3_%s);\n' % (str(r), str(r))

        if r in range(rA_begin, rA_begin + 8) or r in range(rA_begin + 16, rA_begin + 24):
            operation_6bit_l.ROUNDFUNC_linear(r, 0)
            operation_6bit_l.COPY_linear(r, 0)
            res += 'ASSERT(ylinear_0_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_0_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s = xlinear_0_%s);\n' % (str(r), str(r))

            operation_6bit_l.XOR_linear(r, 0)
            res += 'ASSERT(ylinear_3_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(xlinear_3_%s = XOR_OUT_0_%s);\n' % (str(r), str(r))

            res += 'ASSERT(xlinear_1_%s = ylinear_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(xlinear_2_%s = ylinear_2_%s);\n' % (str(r), str(r))

        # nextround:
        for i in range(num_branch):
            res += 'ASSERT(xlinear_%s_%s = ylinear_%s_%s);\n' % (str(i), str(r + 1), str((i + 1) % num_branch), str(r))


    with open(filename, 'a') as f:
        f.write(res)
        # for showing the distinguisher
        res= ""
        if num_R_color == 14:
            res += 'ASSERT(x_0_0 = 0bin000000);\n'
            res += 'ASSERT(x_1_0 = 0bin000000);\n'
            res += 'ASSERT(x_2_0 = 0bin000001);\n'
            res += 'ASSERT(x_3_0 = 0bin000100);\n'
        f.write(res)

    operation_6bit_l.KEY_SUM(num_R_sum, num_xor, num_pr)
    operation_6bit_l.period_SUM(num_R_sum, num_roundfunc)

    if num_R_linear == 0:
        operation_6bit_l.END(num_R_color-1, num_branch)

    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')



