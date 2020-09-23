'''
This file was my main code dump as I experimented with data and implementing
the ORB strat.  It takes user input, parses data into pandas df, calculates
opening range breakouts, and collects peaks/troughs once it has broken out of 
the orb.
'''

import pandas as pd
from datetime import datetime, timezone
import glob	# bash style file lookup
import pyzip
import time
import os


#################### User input
cwd = os.getcwd()+'/lib/'
# cwd = '/Volumes/Seagate Backup Plus Drive/'

# TODO validate
ticker = input("Enter ticker: ").upper()
start_date = input("Enter start date (M/D/YYYY): ")
end_date = input("Enter end date (M/D/YYYY): ")
print()

# Auto-fill ticker for testing
if ticker == '':
	ticker = 'TSLA'

# Auto-fill dates for testing
if start_date == '':
	start_date = '5/20/2020'
	end_date = '2020-6-5'


#################### Open file
if not os.path.exists(cwd):
	raise FileNotFoundError('Path does not exist: ', cwd)

path = glob.glob(cwd+'{}_*.txt'.format(ticker))
if len(path) > 1:
	raise LookupError("Found multiple files matching ticker: ", ticker)
elif len(path) < 1:
	raise FileNotFoundError('Could not find file matching ticker: ', ticker)

start_time = time.time()

''' Commented code can be used to read zips.  Takes longer at run time but it 
works if hard disk space is an issue. '''
# loc='/Users/Daniel/Desktop/Nighthawk/lib/combined/zip/clean_zip.zip'
# df = pd.read_csv(loc, compression='zip')

df = pd.read_csv(path[0])
# print("\n--- %s seconds to read file ---" % (time.time() - start_time))
# print('\n\n', df.head())


#################### Structure dataframe
df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
df['datetime'] = pd.to_datetime(df.datetime);   # convert col to datetime type
df.set_index('datetime', inplace=True)

# Calculate daily ORB
opening = df.between_time('9:30', '9:45')
gp = opening.groupby(pd.Grouper(freq='B'))
mx = gp.high.max()
mn = gp.low.min()
orb = pd.concat([mx, mn], axis=1)

# Print orb for input date range
test = orb.loc[start_date:end_date]
# print(test)


#################### math
def getPeaks(df_day, trues):
	if( len(trues)%2 == 1 ):
		trues.append(df_day.tail(1).index)
	x = []
	y = []
	print("--- Peaks ---")
	for i in range(0, len(trues)-1):
		y.append( df_day.high[trues[i]:trues[i+1]].max() )
		x.append( df_day.high[trues[i]:trues[i+1]].idxmax() )

	peaks = pd.DataFrame(y, index=x, columns=['high'])
	print(peaks)
	return peaks

df['next_high'] = df.high.shift(-1)


gp = opening.groupby(pd.Grouper(freq='B'))
after_orb = df.between_time('9:45', '23:59')
gp2 = after_orb.groupby(pd.Grouper(freq='B'))

# print(gp.high.max())

print('------ 7-1-10 ------') #checking missing times
print( df.high['2010-07-01'] )

# print(gp.high)
# print(orb.high)

# print(df['2020-5-20'])
dt = ''
for day, frame in gp:
	# Get orb boundary
	mx = frame['high'].max()

	day = str(day).split()[0]
	print('------ day: ', day, "------")
	print('------ max: ', mx, "------")
	
	dt = pd.to_datetime(day+' 00:00:00')
	try:
		df_day = gp2.get_group(dt)
	except:
		print("Holiday?")
		continue
	# print('------ df_day -------')
	# print(df_day)

	df_day['cross'] = (
    	((df_day.high >= mx) & (df_day.next_high < mx)) |
    	((df_day.next_high > mx) & (df_day.high <= mx)) |
    	(df_day.high == mx))
	# print("Num crosses: ", df.cross.sum())

	

	# gp2 = df.between_time('9:45', '23:59').groupby(pd.Grouper(freq='B'))
	# df2 = gp2.get_group(dt)
	# print(df2)
	trues = df_day[df_day.cross == True].index
	getPeaks(df_day, trues)

	# test single day 13 peaks
	if day == '2010-07-08':
		break

pd.set_option('display.max_rows', None)

