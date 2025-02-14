import operation_6bit_l
import os

filename = operation_6bit_l.filename

if __name__ == '__main__':
    with open(filename, 'w') as f:
        f.write('')

    num_branch = 8

    num_R_color = 10
    num_R_linear = 0


    num_R_sum = num_R_color
    num_pr = num_branch - 8
    num_xor = 4
    num_roundfunc = 4

    res = ''


    operation_6bit_l.generate_round_state(0, num_branch)
    for r in range(num_R_color):
        operation_6bit_l.generate_round_state(r+1, num_branch)

        #S4
        operation_6bit_l.COPY(r, 0)
        operation_6bit_l.ROUNDFUNC(r, 0)
        res += 'ASSERT(x_4_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_0_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_0_%s = y_4_%s);\n' % (str(r), str(r))

        #S5
        operation_6bit_l.COPY(r, 1)
        operation_6bit_l.ROUNDFUNC(r, 1)
        res += 'ASSERT(x_5_%s = COPY_IN_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_1_%s = ROUNDFUNC_IN_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_1_%s = y_5_%s);\n' % (str(r), str(r))

        #S6
        operation_6bit_l.COPY(r, 2)
        operation_6bit_l.ROUNDFUNC(r, 2)
        res += 'ASSERT(x_6_%s = COPY_IN_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_2_%s = ROUNDFUNC_IN_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_2_%s = y_6_%s);\n' % (str(r), str(r))

        #S7
        operation_6bit_l.COPY(r, 3)
        operation_6bit_l.ROUNDFUNC(r, 3)
        res += 'ASSERT(x_7_%s = COPY_IN_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_3_%s = ROUNDFUNC_IN_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_3_%s = y_7_%s);\n' % (str(r), str(r))

        #S0
        operation_6bit_l.XOR(r, 0)
        res += 'ASSERT(x_0_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_3_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_0_%s = y_0_%s);\n' % (str(r), str(r))

        #S1
        operation_6bit_l.XOR(r, 1)
        res += 'ASSERT(x_1_%s = XOR_IN1_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_2_%s = XOR_IN2_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_1_%s = y_1_%s);\n' % (str(r), str(r))

        #S2
        operation_6bit_l.XOR(r, 2)
        res += 'ASSERT(x_2_%s = XOR_IN1_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_1_%s = XOR_IN2_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_2_%s = y_2_%s);\n' % (str(r), str(r))

        #S3
        operation_6bit_l.XOR(r, 3)
        res += 'ASSERT(x_3_%s = XOR_IN1_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_0_%s = XOR_IN2_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_3_%s = y_3_%s);\n' % (str(r), str(r))

        #nextround:
        for i in range(num_branch):
            res += 'ASSERT(x_%s_%s = y_%s_%s);\n' % (str(i), str(r+1), str((i - 1) % num_branch), str(r))

    operation_6bit_l.generate_round_state_linear(num_R_color, num_branch)
    for r in range(num_R_color, num_R_linear+num_R_color):
        operation_6bit_l.generate_round_state_linear(r+1, num_branch)
        if r == num_R_color:
            operation_6bit_l.initial(r, num_branch)

        #S4
        operation_6bit_l.COPY_linear(r, 0)
        operation_6bit_l.ROUNDFUNC_linear(r, 0)
        res += 'ASSERT(ylinear_4_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_0_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_0_%s = xlinear_4_%s);\n' % (str(r), str(r))

        #S5
        operation_6bit_l.COPY_linear(r, 1)
        operation_6bit_l.ROUNDFUNC_linear(r, 1)
        res += 'ASSERT(ylinear_5_%s = COPY_IN_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_1_%s = ROUNDFUNC_IN_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_1_%s = xlinear_5_%s);\n' % (str(r), str(r))

        #S6
        operation_6bit_l.COPY_linear(r, 2)
        operation_6bit_l.ROUNDFUNC_linear(r, 2)
        res += 'ASSERT(ylinear_6_%s = COPY_IN_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_2_%s = ROUNDFUNC_IN_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_2_%s = xlinear_6_%s);\n' % (str(r), str(r))

        #S7
        operation_6bit_l.COPY_linear(r, 3)
        operation_6bit_l.ROUNDFUNC_linear(r, 3)
        res += 'ASSERT(ylinear_7_%s = COPY_IN_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT1_3_%s = ROUNDFUNC_IN_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(COPY_OUT2_3_%s = xlinear_7_%s);\n' % (str(r), str(r))

        #S0
        operation_6bit_l.XOR_linear(r, 0)
        res += 'ASSERT(ylinear_0_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_3_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_0_%s = xlinear_0_%s);\n' % (str(r), str(r))

        #S1
        operation_6bit_l.XOR_linear(r, 1)
        res += 'ASSERT(ylinear_1_%s = XOR_IN1_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_2_%s = XOR_IN2_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_1_%s = xlinear_1_%s);\n' % (str(r), str(r))

        #S2
        operation_6bit_l.XOR_linear(r, 2)
        res += 'ASSERT(ylinear_2_%s = XOR_IN1_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_1_%s = XOR_IN2_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_2_%s = xlinear_2_%s);\n' % (str(r), str(r))

        #S3
        operation_6bit_l.XOR_linear(r, 3)
        res += 'ASSERT(ylinear_3_%s = XOR_IN1_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(ROUNDFUNC_OUT_0_%s = XOR_IN2_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_3_%s = xlinear_3_%s);\n' % (str(r), str(r))

        # nextround:
        for i in range(num_branch):
            res += 'ASSERT(xlinear_%s_%s = ylinear_%s_%s);\n' % (str(i), str(r + 1), str((i - 1) % num_branch), str(r))


    with open(filename, 'a') as f:
        f.write(res)



    operation_6bit_l.KEY_SUM(num_R_sum, num_xor, num_pr)
    operation_6bit_l.period_SUM(num_R_sum, num_roundfunc)

    if num_R_linear == 0:
        operation_6bit_l.END(num_R_color-1, num_branch)

    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')



