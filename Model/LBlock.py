import operation_6bit_l
import os

filename = operation_6bit_l.filename

if __name__ == '__main__':
    with open(filename, 'w') as f:
        f.write('')

    num_branch = 16

    num_R_color = 10
    num_R_linear = 0

    num_R_sum = num_R_color
    num_pr = num_branch - 10
    num_xor = 8
    num_roundfunc = 8


    #LBlock
    res = ''


    operation_6bit_l.generate_round_state(0, num_branch)
    for r in range(num_R_color):
        operation_6bit_l.generate_round_state(r+1, num_branch)

        for x in range(8):
            operation_6bit_l.ROUNDFUNC(r, x)
            operation_6bit_l.COPY(r, x)
            res += 'ASSERT(x_%s_%s = COPY_IN_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT1_%s_%s = ROUNDFUNC_IN_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT2_%s_%s = y_%s_%s);\n' % (str(x), str(r), str(x), str(r))


        operation_6bit_l.XOR(r, 0)
        res += 'ASSERT(x_8_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_0_%s = ROUNDFUNC_OUT_4_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_0_%s = y_14_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 1)
        res += 'ASSERT(x_9_%s = XOR_IN1_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_1_%s = ROUNDFUNC_OUT_6_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_1_%s = y_15_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 2)
        res += 'ASSERT(x_10_%s = XOR_IN1_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_2_%s = ROUNDFUNC_OUT_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_2_%s = y_8_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 3)
        res += 'ASSERT(x_11_%s = XOR_IN1_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_3_%s = ROUNDFUNC_OUT_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_3_%s = y_9_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 4)
        res += 'ASSERT(x_12_%s = XOR_IN1_4_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_4_%s = ROUNDFUNC_OUT_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_4_%s = y_10_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 5)
        res += 'ASSERT(x_13_%s = XOR_IN1_5_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_5_%s = ROUNDFUNC_OUT_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_5_%s = y_11_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 6)
        res += 'ASSERT(x_14_%s = XOR_IN1_6_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_6_%s = ROUNDFUNC_OUT_5_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_6_%s = y_12_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR(r, 7)
        res += 'ASSERT(x_15_%s = XOR_IN1_7_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_7_%s = ROUNDFUNC_OUT_7_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_7_%s = y_13_%s);\n' % (str(r), str(r))

        #nextround:
        for i in range(num_branch):
            res += 'ASSERT(x_%s_%s = y_%s_%s);\n' % (str(i), str(r+1), str((i + 8) % num_branch), str(r))

    operation_6bit_l.generate_round_state_linear(num_R_color, num_branch)
    for r in range(num_R_color, num_R_linear+num_R_color):
        operation_6bit_l.generate_round_state_linear(r+1, num_branch)
        if r == num_R_color:
            operation_6bit_l.initial(r, num_branch)

        for x in range(8):
            operation_6bit_l.ROUNDFUNC_linear(r, x)
            operation_6bit_l.COPY_linear(r, x)
            res += 'ASSERT(ylinear_%s_%s = COPY_IN_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT1_%s_%s = ROUNDFUNC_IN_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT2_%s_%s = xlinear_%s_%s);\n' % (str(x), str(r), str(x), str(r))


        operation_6bit_l.XOR_linear(r, 0)
        res += 'ASSERT(ylinear_14_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_0_%s = ROUNDFUNC_OUT_4_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_0_%s = xlinear_8_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 1)
        res += 'ASSERT(ylinear_15_%s = XOR_IN1_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_1_%s = ROUNDFUNC_OUT_6_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_1_%s = xlinear_9_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 2)
        res += 'ASSERT(ylinear_8_%s = XOR_IN1_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_2_%s = ROUNDFUNC_OUT_1_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_2_%s = xlinear_10_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 3)
        res += 'ASSERT(ylinear_9_%s = XOR_IN1_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_3_%s = ROUNDFUNC_OUT_3_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_3_%s = xlinear_11_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 4)
        res += 'ASSERT(ylinear_10_%s = XOR_IN1_4_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_4_%s = ROUNDFUNC_OUT_0_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_4_%s = xlinear_12_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 5)
        res += 'ASSERT(ylinear_11_%s = XOR_IN1_5_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_5_%s = ROUNDFUNC_OUT_2_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_5_%s = xlinear_13_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 6)
        res += 'ASSERT(ylinear_12_%s = XOR_IN1_6_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_6_%s = ROUNDFUNC_OUT_5_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_6_%s = xlinear_14_%s);\n' % (str(r), str(r))

        operation_6bit_l.XOR_linear(r, 7)
        res += 'ASSERT(ylinear_13_%s = XOR_IN1_7_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_IN2_7_%s = ROUNDFUNC_OUT_7_%s);\n' % (str(r), str(r))
        res += 'ASSERT(XOR_OUT_7_%s = xlinear_15_%s);\n' % (str(r), str(r))

        # nextround:
        for i in range(num_branch):
            res += 'ASSERT(xlinear_%s_%s = ylinear_%s_%s);\n' % (str(i), str(r + 1), str((i + 8) % num_branch), str(r))


    with open(filename, 'a') as f:
        f.write(res)


    operation_6bit_l.KEY_SUM(num_R_sum, num_xor, num_pr)
    operation_6bit_l.period_SUM(num_R_sum, num_roundfunc)

    if num_R_linear == 0:
        operation_6bit_l.END(num_R_color-1, num_branch)


    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')



