import re

filename = 'res.txt'

patternx = re.compile(r'x_\w+ = 0(x|b)(\d+|\w+)')
patterny = re.compile(r' y_\w+ = 0(x|b)(\d+|\w+)')
patternxlinear = re.compile(r'xlinear\w+ = 0(x|b)(\d+|\w+)')
patternylinear = re.compile(r'ylinear\w+ = 0(x|b)(\d+|\w+)')
patternxor = re.compile(r'XOR\w+ = 0(x|b)(\d+|\w+)')
patternpr = re.compile(r'XOR_key\w+ = 0(x|b)(\d+|\w+)')
patternr = re.compile(r'ROUNDFUNC\w+ = 0(x|b)(\d+|\w+)')
patternc = re.compile(r'COPY\w+ = 0(x|b)(\d+|\w+)')
xlist = []
ylist = []
xlinearlist = []
ylinearlist = []
xorlist = []
prlist = []
rlist = []
clist = []


with open(filename, 'r',encoding = 'utf-8') as f:
    text = f.readlines()
    for line in text:
        x = patternx.search(line)
        y = patterny.search(line)
        xlinear = patternxlinear.search(line)
        ylinear = patternylinear.search(line)
        xor = patternxor.search(line)
        pr =  patternpr.search(line)
        roundfunc = patternr.search(line)
        copy = patternc.search(line)
        if x:
            xlist.append(x.group())
        if y:
            ylist.append(y.group())
        if xlinear:
            xlinearlist.append(xlinear.group())
        if ylinear:
            ylinearlist.append(ylinear.group())
        if xor:
            xorlist.append(xor.group())
        if pr:
            prlist.append(pr.group())
        if roundfunc:
            rlist.append(roundfunc.group())
        if copy:
            clist.append(copy.group())

#print(xlist)
sorted_xlist = sorted(xlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_xlist,'\n')

sorted_ylist = sorted(ylist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_ylist,'\n')

sorted_xlinearlist = sorted(xlinearlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_xlinearlist,'\n')

sorted_ylinearlist = sorted(ylinearlist, key=lambda s: (int(re.split('_|=',s)[2]), int(re.split('_|=',s)[1])))
print(sorted_ylinearlist,'\n')

sorted_xorlist = sorted(xorlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
#print(sorted_xorlist,'\n')

sorted_prlist = sorted(prlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
print(sorted_prlist,'\n')

sorted_rlist = sorted(rlist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
#print(sorted_rlist,'\n')

sorted_clist = sorted(clist, key=lambda s: (int(re.split('_|=',s)[3]), int(re.split('_|=',s)[2])))
#print(sorted_clist,'\n')


