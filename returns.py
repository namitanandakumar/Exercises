import pandas as pd
import numpy as np

#Deleted extra columns for the yearly returns file in Excel and renamed the others.

df = pd.read_csv("~/Desktop/year.csv")

def good(x):
    return max(x['sp'], x['tbill'])

def bad(x):
    return min(x['sp'], x['tbill'])


df['wrong'] = df.apply(bad, axis=1)
df['right'] = df.apply(good, axis=1)

avgwrong = np.mean(df['wrong'])
avgright = np.mean(df['right'])

probs = pd.DataFrame(range(50,101,1))
probs = probs/100
probs.columns = ['p']

def ret(x):
    return ((x['p'])*(avgright) + (1-x['p'])*(avgwrong))*100

def allret(x):
    return ((x['p'])*(df['right']*100) + (1-x['p'])*(df['wrong'])*100)

probs['return'] = probs.apply(ret, axis=1)

allrets = pd.DataFrame(probs.apply(allret, axis=1))

probs['stddev'] = allrets.std(axis=1)

#print probs

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
probs.to_excel(writer, sheet_name='Sheet1')
writer.save()
