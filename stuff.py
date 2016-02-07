data1 = pandas.io.parsers.read_csv("https://raw.githubusercontent.com/april1452/craigslove/master/CSVs/a1-a11.csv",quotechar='"')
data2 = pandas.io.parsers.read_csv("https://raw.githubusercontent.com/april1452/craigslove/master/CSVs/d1-d11.csv",quotechar='"')

statusdict = {}
for s in data1['status']:
    if s==s:
        if s in statusdict:
            statusdict[s] = statusdict[s]+1
        else:
            statusdict[s] = 1
for s in data2['status']:
    if s==s:
        if s in statusdict:
            statusdict[s] = statusdict[s]+1
        else:
            statusdict[s] = 1
            
print(statusdict)

ages=[]
for s in data1['age']:
    if s==s and s >=18 and s < 200:
        ages.append(s)
for s in data2['age']:
    if s==s and s >=18 and s < 200:
        ages.append(s)


plt.hist(ages, bins=102,range=(18,110))
xlim([18,110])
show()
