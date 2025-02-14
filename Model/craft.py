import operation_6bit_l
import os

filename = operation_6bit_l.filename

if __name__ == '__main__':
    with open(filename, 'w') as f:
        f.write('')

    num_branch = 16

    num_R_color = 7
    num_R_linear = 0

    num_R_sum = num_R_color
    num_pr = num_branch - 16
    num_xor = 12
    num_roundfunc = 16

    # the state in the model is:
    # 0   1    2    3
    # 4   5    6    7
    # 8   9   10  11
    # 12 13 14  15

    res = ''

    operation_6bit_l.generate_round_state(0, num_branch)

    # for showing the distinguisher
    if num_R_color == 7:
        res += 'ASSERT(x_%s_0 = 0bin000100);\n' % str(0)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(1)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(2)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(3)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(4)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(5)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(6)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(7)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(8)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(9)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(10)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(11)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(12)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(13)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(14)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(15)
        res += 'ASSERT(x_%s_7[5:4] = 0bin01);\n' % str(4)

    if num_R_color == 11:
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(0)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(1)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(2)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(3)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(4)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(5)
        res += 'ASSERT(x_%s_0 = 0bin000100);\n' % str(6)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(7)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(8)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(9)
        res += 'ASSERT(x_%s_0 = 0bin000000);\n' % str(10)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(11)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(12)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(13)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(14)
        res += 'ASSERT(x_%s_0 = 0bin000001);\n' % str(15)
        res += 'ASSERT(x_%s_11[5:4] = 0bin01);\n' % str(6)

    for r in range(num_R_color):
        operation_6bit_l.generate_round_state(r+1, num_branch)

        res += 'ASSERT(x_0_0 = 0bin000100 OR x_1_0 = 0bin000100 OR x_2_0 = 0bin000100 OR x_3_0 = 0bin000100 OR x_4_0 = 0bin000100 OR x_5_0 = 0bin000100 OR x_6_0 = 0bin000100 OR x_7_0 = 0bin000100);\n'


        res += 'ASSERT('
        for i in range(num_branch-1):
            res += 'ROUNDFUNC_IN_%s_0 = 0bin000101 OR ' % str(i)
        res += 'ROUNDFUNC_IN_15_0 = 0bin000101);\n'
        res += '%tag;\n'


        if r < num_R_color - 1:
            #MC
            #S0
            operation_6bit_l.XOR(r, 0)
            operation_6bit_l.XOR(r, 1)
            res += 'ASSERT(x_0_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_0_%s = XOR_IN1_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_1_%s = ROUNDFUNC_IN_15_%s);\n' % (str(r), str(r))

            #S4
            operation_6bit_l.XOR(r, 2)
            res += 'ASSERT(x_4_%s = XOR_IN1_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_IN_10_%s = XOR_OUT_2_%s);\n' % (str(r), str(r))

            #S8
            operation_6bit_l.COPY(r, 0)
            res += 'ASSERT(x_8_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s = ROUNDFUNC_IN_6_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))

            #S12
            operation_6bit_l.COPY(r, 1)
            operation_6bit_l.COPY(r, 2)
            res += 'ASSERT(x_12_%s = COPY_IN_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_1_%s = COPY_IN_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_1_%s = XOR_IN2_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_2_%s = ROUNDFUNC_IN_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_2_%s = XOR_IN2_1_%s);\n' % (str(r), str(r))

            #S1
            operation_6bit_l.XOR(r, 3)
            operation_6bit_l.XOR(r, 4)
            res += 'ASSERT(x_1_%s = XOR_IN1_3_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_3_%s = XOR_IN1_4_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_4_%s = ROUNDFUNC_IN_12_%s);\n' % (str(r), str(r))

            #S5
            operation_6bit_l.XOR(r, 5)
            res += 'ASSERT(x_5_%s = XOR_IN1_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_IN_9_%s = XOR_OUT_5_%s);\n' % (str(r), str(r))

            #S9
            operation_6bit_l.COPY(r, 3)
            res += 'ASSERT(x_9_%s = COPY_IN_3_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_3_%s = ROUNDFUNC_IN_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_3_%s = XOR_IN2_3_%s);\n' % (str(r), str(r))

            #S13
            operation_6bit_l.COPY(r, 4)
            operation_6bit_l.COPY(r, 5)
            res += 'ASSERT(x_13_%s = COPY_IN_4_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_4_%s = COPY_IN_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_4_%s = XOR_IN2_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_5_%s = ROUNDFUNC_IN_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_5_%s = XOR_IN2_4_%s);\n' % (str(r), str(r))


            #S2
            operation_6bit_l.XOR(r, 6)
            operation_6bit_l.XOR(r, 7)
            res += 'ASSERT(x_2_%s = XOR_IN1_6_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_6_%s = XOR_IN1_7_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_7_%s = ROUNDFUNC_IN_13_%s);\n' % (str(r), str(r))

            #S6
            operation_6bit_l.XOR(r, 8)
            res += 'ASSERT(x_6_%s = XOR_IN1_8_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_IN_8_%s = XOR_OUT_8_%s);\n' % (str(r), str(r))

            #S10
            operation_6bit_l.COPY(r, 6)
            res += 'ASSERT(x_10_%s = COPY_IN_6_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_6_%s = ROUNDFUNC_IN_4_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_6_%s = XOR_IN2_6_%s);\n' % (str(r), str(r))

            #S14
            operation_6bit_l.COPY(r, 7)
            operation_6bit_l.COPY(r, 8)
            res += 'ASSERT(x_14_%s = COPY_IN_7_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_7_%s = COPY_IN_8_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_7_%s = XOR_IN2_8_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_8_%s = ROUNDFUNC_IN_3_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_8_%s = XOR_IN2_7_%s);\n' % (str(r), str(r))



            #S3
            operation_6bit_l.XOR(r, 9)
            operation_6bit_l.XOR(r, 10)
            res += 'ASSERT(x_3_%s = XOR_IN1_9_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_9_%s = XOR_IN1_10_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_10_%s = ROUNDFUNC_IN_14_%s);\n' % (str(r), str(r))

            #S7
            operation_6bit_l.XOR(r, 11)
            res += 'ASSERT(x_7_%s = XOR_IN1_11_%s);\n' % (str(r), str(r))
            res += 'ASSERT(ROUNDFUNC_IN_11_%s = XOR_OUT_11_%s);\n' % (str(r), str(r))

            #S11
            operation_6bit_l.COPY(r, 9)
            res += 'ASSERT(x_11_%s = COPY_IN_9_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_9_%s = ROUNDFUNC_IN_7_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_9_%s = XOR_IN2_9_%s);\n' % (str(r), str(r))

            #S15
            operation_6bit_l.COPY(r, 10)
            operation_6bit_l.COPY(r, 11)
            res += 'ASSERT(x_15_%s = COPY_IN_10_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_10_%s = COPY_IN_11_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_10_%s = XOR_IN2_11_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_11_%s = ROUNDFUNC_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_11_%s = XOR_IN2_10_%s);\n' % (str(r), str(r))


            for i in range(num_branch):
                operation_6bit_l.ROUNDFUNC(r, i)
                res += 'ASSERT(ROUNDFUNC_OUT_%s_%s = y_%s_%s);\n'% (str(i), str(r), str(i), str(r))

        else:

            operation_6bit_l.XOR(r, 0)
            operation_6bit_l.XOR(r, 1)
            res += 'ASSERT(x_0_%s = XOR_IN1_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_0_%s = XOR_IN1_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_1_%s = y_15_%s);\n' % (str(r), str(r))

            #S4
            operation_6bit_l.XOR(r, 2)
            res += 'ASSERT(x_4_%s = XOR_IN1_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(y_10_%s = XOR_OUT_2_%s);\n' % (str(r), str(r))

            #S8
            operation_6bit_l.COPY(r, 0)
            res += 'ASSERT(x_8_%s = COPY_IN_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_0_%s = y_6_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_0_%s = XOR_IN2_0_%s);\n' % (str(r), str(r))

            #S12
            operation_6bit_l.COPY(r, 1)
            operation_6bit_l.COPY(r, 2)
            res += 'ASSERT(x_12_%s = COPY_IN_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_1_%s = COPY_IN_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_1_%s = XOR_IN2_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_2_%s = y_1_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_2_%s = XOR_IN2_1_%s);\n' % (str(r), str(r))

            #S1
            operation_6bit_l.XOR(r, 3)
            operation_6bit_l.XOR(r, 4)
            res += 'ASSERT(x_1_%s = XOR_IN1_3_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_3_%s = XOR_IN1_4_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_4_%s = y_12_%s);\n' % (str(r), str(r))

            #S5
            operation_6bit_l.XOR(r, 5)
            res += 'ASSERT(x_5_%s = XOR_IN1_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(y_9_%s = XOR_OUT_5_%s);\n' % (str(r), str(r))

            #S9
            operation_6bit_l.COPY(r, 3)
            res += 'ASSERT(x_9_%s = COPY_IN_3_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_3_%s = y_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_3_%s = XOR_IN2_3_%s);\n' % (str(r), str(r))

            #S13
            operation_6bit_l.COPY(r, 4)
            operation_6bit_l.COPY(r, 5)
            res += 'ASSERT(x_13_%s = COPY_IN_4_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_4_%s = COPY_IN_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_4_%s = XOR_IN2_5_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_5_%s = y_2_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_5_%s = XOR_IN2_4_%s);\n' % (str(r), str(r))


            #S2
            operation_6bit_l.XOR(r, 6)
            operation_6bit_l.XOR(r, 7)
            res += 'ASSERT(x_2_%s = XOR_IN1_6_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_6_%s = XOR_IN1_7_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_7_%s = y_13_%s);\n' % (str(r), str(r))

            #S6
            operation_6bit_l.XOR(r, 8)
            res += 'ASSERT(x_6_%s = XOR_IN1_8_%s);\n' % (str(r), str(r))
            res += 'ASSERT(y_8_%s = XOR_OUT_8_%s);\n' % (str(r), str(r))

            #S10
            operation_6bit_l.COPY(r, 6)
            res += 'ASSERT(x_10_%s = COPY_IN_6_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_6_%s = y_4_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_6_%s = XOR_IN2_6_%s);\n' % (str(r), str(r))

            #S14
            operation_6bit_l.COPY(r, 7)
            operation_6bit_l.COPY(r, 8)
            res += 'ASSERT(x_14_%s = COPY_IN_7_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_7_%s = COPY_IN_8_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_7_%s = XOR_IN2_8_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_8_%s = y_3_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_8_%s = XOR_IN2_7_%s);\n' % (str(r), str(r))



            #S3:
            operation_6bit_l.XOR(r, 9)
            operation_6bit_l.XOR(r, 10)
            res += 'ASSERT(x_3_%s = XOR_IN1_9_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_9_%s = XOR_IN1_10_%s);\n' % (str(r), str(r))
            res += 'ASSERT(XOR_OUT_10_%s = y_14_%s);\n' % (str(r), str(r))

            #S7
            operation_6bit_l.XOR(r, 11)
            res += 'ASSERT(x_7_%s = XOR_IN1_11_%s);\n' % (str(r), str(r))
            res += 'ASSERT(y_11_%s = XOR_OUT_11_%s);\n' % (str(r), str(r))

            #S11
            operation_6bit_l.COPY(r, 9)
            res += 'ASSERT(x_11_%s = COPY_IN_9_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_9_%s = y_7_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_9_%s = XOR_IN2_9_%s);\n' % (str(r), str(r))

            #S15
            operation_6bit_l.COPY(r, 10)
            operation_6bit_l.COPY(r, 11)
            res += 'ASSERT(x_15_%s = COPY_IN_10_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_10_%s = COPY_IN_11_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_10_%s = XOR_IN2_11_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT1_11_%s = y_0_%s);\n' % (str(r), str(r))
            res += 'ASSERT(COPY_OUT2_11_%s = XOR_IN2_10_%s);\n' % (str(r), str(r))


        #nextround:
        for i in range(num_branch):
            res += 'ASSERT(x_%s_%s = y_%s_%s);\n' % (str(i), str(r+1), str(i), str(r))



    with open(filename, 'a') as f:
        f.write(res)



    operation_6bit_l.KEY_SUM(num_R_sum, num_xor, num_pr)
    operation_6bit_l.period_SUM(num_R_sum-1, num_roundfunc)

    if num_R_linear == 0:
        operation_6bit_l.END(num_R_color-1, num_branch)


    with open(filename, 'a') as f:
        f.write('QUERY(FALSE);\nCOUNTEREXAMPLE;\n')



