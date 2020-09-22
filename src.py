from ftplib import FTP
import gzip
import pandas as pd
import sys, os

# function that splits file and location in gzip content

def get_data(s):     # a function that splits a string in two based on the last space
    e = s.rfind(' ') # looking for last space from the right
    l = len(s)       # measuring lenght of line
    return [s[0:e],s[e+1:l]]

# main variables

user = 'anonymous'
pwd = ''
src = 'ftp.uk.debian.org'
path = 'debian/dists/stable/main/'
arch = sys.argv[1] # getting architecture from arguments
f = 'Contents-'+arch+'.gz' # filename definition

# connecting to FTP in ACTV mode

ftp = FTP(src, user, pwd)
ftp.cwd(path)
ftp.set_pasv(False)

# downloading gz file

print('searching gz file...')
print('\b')

try: 
    with open(f,'wb') as fp:
        ftp.retrbinary('RETR '+f+'', fp.write)
        print('gz file downloaded.')
except:
    print('gz file not found.')

# opening gz file and storing it in memory as Pandas DataFrame

lst = list()

with gzip.open(f,'rt',encoding='utf-8') as cnt:
    for l in cnt:
        lst.append(get_data(l[:-1])) # appending each line of the gz file except last char '\n'
        
df = pd.DataFrame(lst,columns=['FILES','PACKAGE'])

top10 = df.groupby('PACKAGE')\
        .agg('count')\
        .sort_values(by='FILES',ascending=False)\
        .head(10)\
        .reset_index(drop=False)\

# print output
            
# count = 0
# print(' PACKAGE ','\t\t\t', ' FILES ')
# for index, row in top10.iterrows():
#     count += 1
#     print('\b')
#     print(count, row['PACKAGE'], '\t' , row['FILES'])

tab = list()
titles = ['PACKAGE','FILES']

for index,row in top10.iterrows():
    tab.append([row['PACKAGE'],row['FILES']])

data = [titles] + tab

print('\b')
for i,d in enumerate(data):
    line = '|'.join(str(x).ljust(35) for x in d)
    print(line)
    if i == 0:
        print('-' * len(line))