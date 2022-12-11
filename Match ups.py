import random
import csv

results = []
###Replace the name of the chart here:
mainf = open('allstarMatchups no ValDG.csv','r')
reader = csv.reader(mainf,delimiter=',')
for row in reader: 
    results.append(row)
mainf.close()

Charnum = len(results)
Chars = [results[i][0] for i in range(Charnum)]
Charpicks = [1/Charnum for i in range(Charnum)]
#print(Chars,Charpicks)
Values = [[float(results[i][j+1])-5 for j in range(Charnum)] for i in range(Charnum)]
#print(Values)

from matplotlib import pyplot as plt

Simul_num = 300000

###adjust colors on the graph here, these are not colorblind friendly
colors = ['#505050','#f00000','#00f000','#0000f0',
          '#707000','#f09000','#f0f000','#90f000',
          '#007070','#00f0f0','#0090f0','#00f090',
          '#900090','#f000f0','#9000f0','#f00090',
          '#f0f090','#f090f0','#90f0f0','#f0f090','#90f0f0','#f090f0',
          '#500000','#005000','#000050',
          '#509000','#505000','#905000',
          '#005050','#009050','#005090',
          '#500050','#900050','#500090',
          '#101090','#109010','#901010','#101090','#901010','#109010',]

###These setings are mostly good enough
x = [i for i in range(int(Simul_num/1000))]
y = [[0 for i in range(int(Simul_num/1000))] for j in range(Charnum)]
ym =[[1/Charnum for i in range(int(Simul_num/1000))] for j in range(Charnum)]
sums = [1/Charnum for i in range(int(Simul_num))]

def Loop(ct):
    rng1 = random.random()
    rng2 = random.random()

    choice1 = -1
    choice2 = -1
    
    for i in range(Charnum):
        if rng1 > sum(Charpicks[0:i]):
            
            choice1 += 1
            continue
        else:
            break
    #print(choice1)

    for i in range(Charnum):
        if rng2 > sum(Charpicks[0:i]):
            choice2 += 1
            continue
        else:
            break
    #print(choice2)

    #print(choice1,Chars[choice1],'vs',choice2,Chars[choice2],'=',Values[choice1][choice2])


    change = Values[choice1][choice2]/1000
    ###Change the low pick rate threshold here, the lower it is,
    # the more extreme the results are, the higher, the less accurate
    # it becomes, suggested 0.2 / Character number, for 12 chars it's 1.7% = 0.017
    AlwaysPick = 0.017
    Charpicks[choice1]+=change
    if Charpicks[choice1] <= AlwaysPick:
        Charpicks[choice1] = AlwaysPick
    Charpicks[choice2]-=change
    if Charpicks[choice2] <= AlwaysPick:
        Charpicks[choice2] = AlwaysPick
    #ChPicks[5] == 0
    #Charpicks[6] == 0

    for i in range(len(Charpicks)):
        Charpicks[i] /= sum(Charpicks)

    first = 100
    if ct > first:
        for k in range(Charnum):
            sums[k] += Charpicks[k]
        
    if ct % 1000 == 0:
        for k in range(Charnum):
            y[k][int(ct/1000)] = Charpicks[k]
            if ct > first:
                ym[k][int(ct/1000)] = sums[k]/(ct-first)
    #print(ChPicks)
    
for i in range(Simul_num):
    Loop(i)
for i in range(Charnum):
    print(str(round(ym[i][-1]*100,2))+'%',': '+Chars[i])

for i in range(Charnum):
    plt.plot(x,y[i],color=colors[i]+'40')
    plt.plot(x,ym[i],label=Chars[i],color=colors[i])
plt.legend(bbox_to_anchor =(1.2, 1))
plt.show()
