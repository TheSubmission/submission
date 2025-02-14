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


    res = ''


    operation_6bit_l.generate_round_state(0, num_branch)

    # for showing the distinguisher
    if num_R_color == 10:
        for num in range(0, 6):
            res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(num)

    for r in range(num_R_color):

        operation_6bit_l.generate_round_state(r+1, num_branch)

        for x in range(8):
            operation_6bit_l.ROUNDFUNC(r, x)
            operation_6bit_l.COPY(r, x)
            res += 'ASSERT(x_%s_%s = COPY_IN_%s_%s);\n' % (str(2*x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT1_%s_%s = ROUNDFUNC_IN_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT2_%s_%s = y_%s_%s);\n' % (str(x), str(r), str(2*x), str(r))

            operation_6bit_l.XOR(r, x)
            res += 'ASSERT(x_%s_%s = XOR_IN1_%s_%s);\n' % (str(2*x+1), str(r), str(x), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_%s_%s = XOR_IN2_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(y_%s_%s = XOR_OUT_%s_%s);\n' % (str(2*x+1), str(r), str(x), str(r))

        #nextround
        res += 'ASSERT(x_0_%s = y_1_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_1_%s = y_2_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_2_%s = y_11_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_3_%s = y_6_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_4_%s = y_3_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_5_%s = y_0_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_6_%s = y_9_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_7_%s = y_4_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_8_%s = y_7_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_9_%s = y_10_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_10_%s = y_13_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_11_%s = y_14_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_12_%s = y_5_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_13_%s = y_8_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_14_%s = y_15_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(x_15_%s = y_12_%s);\n' % (str(r + 1), str(r))


    operation_6bit_l.generate_round_state_linear(num_R_color, num_branch)
    for r in range(num_R_color, num_R_linear+num_R_color):
        operation_6bit_l.generate_round_state_linear(r+1, num_branch)
        if r == num_R_color:
            operation_6bit_l.initial(r, num_branch)

        for x in range(8):
            operation_6bit_l.ROUNDFUNC_linear(r, x)
            operation_6bit_l.COPY_linear(r, x)
            res += 'ASSERT(ylinear_%s_%s = COPY_IN_%s_%s);\n' % (str(2*x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT1_%s_%s = ROUNDFUNC_IN_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(COPY_OUT2_%s_%s = xlinear_%s_%s);\n' % (str(x), str(r), str(2*x), str(r))

            operation_6bit_l.XOR_linear(r, x)
            res += 'ASSERT(ylinear_%s_%s = XOR_IN1_%s_%s);\n' % (str(2*x+1), str(r), str(x), str(r))
            res += 'ASSERT(ROUNDFUNC_OUT_%s_%s = XOR_IN2_%s_%s);\n' % (str(x), str(r), str(x), str(r))
            res += 'ASSERT(xlinear_%s_%s = XOR_OUT_%s_%s);\n' % (str(2*x+1), str(r), str(x), str(r))

        #nextround
        res += 'ASSERT(xlinear_0_%s = ylinear_1_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_1_%s = ylinear_2_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_2_%s = ylinear_11_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_3_%s = ylinear_6_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_4_%s = ylinear_3_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_5_%s = ylinear_0_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_6_%s = ylinear_9_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_7_%s = ylinear_4_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_8_%s = ylinear_7_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_9_%s = ylinear_10_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_10_%s = ylinear_13_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_11_%s = ylinear_14_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_12_%s = ylinear_5_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_13_%s = ylinear_8_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_14_%s = ylinear_15_%s);\n' % (str(r + 1), str(r))
        res += 'ASSERT(xlinear_15_%s = ylinear_12_%s);\n' % (str(r + 1), str(r))


    with open(filename, 'a') as f:
        f.write(res)



    operation_6bit_l.KEY_SUM(num_R_sum, num_xor, num_pr)
    operation_6bit_l.period_SUM(num_R_sum, num_roundfunc)

    if num_R_linear == 0:
        operation_6bit_l.END(num_R_color-1, num_branch)

    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')



