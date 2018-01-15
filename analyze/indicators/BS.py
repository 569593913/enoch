def surport(listK):
    line = []
    v = None
    preI = 0;
    nextI = 0;
    i = 0
    for k in listK:
        #画线
        if (
            get(i-1,listK).low>k.low and
            get(i-2,listK).low>k.low and
            get(i-3,listK).low>k.low and
            get(i+1,listK).low>k.low and
            get(i+2,listK).low>k.low and
            get(i+3,listK).low>k.low
        ):
            if v!=None and v!=k.low:
                 line[-1][1] = None
            v = k.low
#         if v!=None and (v>k.low or (k.low-v)/v > 0.35):
#             v = None
        line.append([k.date,v])
        i += 1
    return line

def barrier(listK):
    line = []
    v = None
    preI = 0;
    nextI = 0;
    i = 0
    for k in listK:
        #画线
        if (
            get(i-1,listK).high<k.high and
            get(i-2,listK).high<k.high and
            get(i-3,listK).high<k.high and
            get(i+1,listK).high<k.high and
            get(i+2,listK).high<k.high and
            get(i+3,listK).high<k.high
        ):
            if v!=None and v!=k.low:
                 line[-1][1] = None
            v = k.high
#         if v!=None and (v<k.high or (v-k.high)/k.high > 0.35):
#             v = None
        line.append([k.date,v])
        i += 1
    return line
def get(i,listK):
    ln = len(listK)
    if i<0:
        i = 0
    if i>=ln:
        i = ln-1
    return listK[i]

def HLRatio(index,period,listK):
    if index < 0:
        index = 0
    if index >= len(listK):
        index = len(listK) - 1
    mx = 0
    mn = 10000000
    i = index - period if index > period else 0
    v = 0
    while i <= index:
        v = listK[i].close
        if v > mx:
            mx = v
        if v < mn:
            mn = v
        i += 1
    return (mx-v)/v,(mn-v)/v