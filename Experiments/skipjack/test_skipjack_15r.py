import copy
import random
import skipjackB
import skipjackA


for time in range(2 ** 1):
    print("time:" + str(time + 1))
    initial_key = random.getrandbits(128)
    print("initial_key:" + hex(initial_key))
    round_keys = skipjackA.generate_round_keys(initial_key, 16)
    alpha0 = random.getrandbits(16)
    while True:
        alpha1 = random.getrandbits(16)
        if alpha1 != alpha0:
            break
    c1 = random.getrandbits(16)
    c2 = random.getrandbits(16)
    list_branch0_0 = [0] * (2 ** 16)
    list_branch0_1 = [0] * (2 ** 16)
    list_branch1_0 = [0] * (2 ** 16)
    list_branch1_1 = [0] * (2 ** 16)
    list_branch01_xor_0 = [0] * (2 ** 16)
    list_branch01_xor_1 = [0] * (2 ** 16)
    list_xor = [0] * (2 ** 16)
    for x in range(2 ** 16):
        for b in range(2):
            if b == 0:
                plaintext = [c1, x, alpha0, c2]
                ciphertext = skipjackA.skipjackA(plaintext, round_keys, 4)
                ciphertext = skipjackB.skipjackB(ciphertext, round_keys, 8)
                ciphertext = skipjackA.skipjackA3(ciphertext, round_keys, 3)
                list_branch0_0[x] = ciphertext[0]
                list_branch1_0[x] = ciphertext[1]
                list_branch01_xor_0[x] = list_branch0_0[x] ^ list_branch1_0[x]
            else:
                plaintext = [c1, x, alpha1, c2]
                ciphertext = skipjackA.skipjackA(plaintext, round_keys, 4)
                ciphertext = skipjackB.skipjackB(ciphertext, round_keys, 8)
                ciphertext = skipjackA.skipjackA3(ciphertext, round_keys, 3)
                list_branch0_1[x] = ciphertext[0]
                list_branch1_1[x] = ciphertext[1]
                list_branch01_xor_1[x] = list_branch0_1[x] ^ list_branch1_1[x]
    for x in range(2 ** 16):
        list_xor[x] = list_branch01_xor_0[x] ^ list_branch01_xor_1[x]
    for s in range(1, 2 ** 16):
        equal = 0
        s_list = [0] * (2 ** 16)
        for element in range(2 ** 1):
            if list_xor[element] == list_xor[s ^ element]:
                equal = equal + 1
            else:
                continue
        if equal == 2 ** 1:
            print("period:" + str(s))
            s_list[s] = s_list[s] + 1
    print("plaintext:")
    print("c1:" + hex(c1))
    print("x")
    print("alpha:" + hex(alpha0) + " " + hex(alpha1))
    print("c2:" + hex(c2))
