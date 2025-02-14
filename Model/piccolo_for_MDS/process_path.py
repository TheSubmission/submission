import re

filename = 'res.txt'

patternx = re.compile(r'x\w+ = 0b(\d+|\w+)')
patterny = re.compile(r'y\w+ = 0b(\d+|\w+)')
patternxor = re.compile(r'XOR\w+ = 0b(\d+|\w+)')
patternsbox = re.compile(r'SBOX\w+ = 0b(\d+|\w+)')
patternc = re.compile(r'COPY\w+ = 0b(\d+|\w+)')
patternshift = re.compile(r'SHIFT\w+ = 0b(\d+|\w+)')
patternand = re.compile(r'AND\w+ = 0b(\d+|\w+)')
patternmc = re.compile(r'MC\w+ = 0b(\d+|\w+)')
xlist = []
ylist = []
xorlist = []
sboxlist = []
clist = []
shiftlist = []
andlist = []
mclist = []


with open(filename, 'r',encoding = 'utf-8') as f:
    text = f.readlines()
    for line in text:
        x = patternx.search(line)
        y = patterny.search(line)
        xor = patternxor.search(line)
        sbox = patternsbox.search(line)
        copy = patternc.search(line)
        shift = patternshift.search(line)
        And = patternand.search(line)
        mc = patternmc.search(line)

        if x:
            xlist.append(x.group())
        if y:
            ylist.append(y.group())
        if xor:
            xorlist.append(xor.group())
        if sbox:
            sboxlist.append(sbox.group())
        if copy:
            clist.append(copy.group())
        if shift:
            shiftlist.append(shift.group())
        if And:
            andlist.append(And.group())
        if mc:
            mclist.append(mc.group())

sorted_xlist = sorted(xlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[1]), int(re.split('_|=',s)[2])))
print(sorted_xlist,'\n')

sorted_ylist = sorted(ylist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[1]), int(re.split('_|=',s)[2])))
print(sorted_ylist,'\n')

sorted_xorlist = sorted(xorlist, key=lambda s: (int(re.split('_|=',s)[4]), int(re.split('_|=',s)[2]), int(re.split('_|=',s)[3])))
#print(sorted_xorlist,'\n')

sorted_sboxlist = sorted(sboxlist, key=lambda s: (int(re.split('_|=',s)[4]), int(re.split('_|=',s)[2]), int(re.split('_|=',s)[3])))
#print(sorted_sboxlist,'\n')

sorted_clist = sorted(clist, key=lambda s: (int(re.split('_|=',s)[4]), int(re.split('_|=',s)[2]), int(re.split('_|=',s)[3])))
#print(sorted_clist,'\n')

sorted_shiftlist = sorted(shiftlist, key=lambda s: (int(re.split('_|=',s)[4]), int(re.split('_|=',s)[2]), int(re.split('_|=',s)[3])))
#print(sorted_shiftlist,'\n')

sorted_andlist = sorted(andlist, key=lambda s: (int(re.split('_|=',s)[4]), int(re.split('_|=',s)[2]), int(re.split('_|=',s)[3])))
#print(sorted_andlist, '\n')

sorted_mclist = sorted(mclist, key=lambda s: (int(re.split('_|=',s)[4]), int(re.split('_|=',s)[2]), int(re.split('_|=',s)[3])))
print(sorted_mclist, '\n')


