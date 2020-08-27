import subprocess
from multiprocessing import Process
import logging
import time
from datetime import datetime
import twint as tw

print('Initialising twint config')
#tc.Output = f'tw-{datetime.now().strftime("%Y%m%d-%H%M%S")}-newsoutlets.csv'  # Set filename to include current date/time
NEWSOUTLETS = ['CNN', 'MSNBC', 'FoxNews', 'WSJ', 'BBC', 'NPR']

def scrape_tweets(tc, username):
    print('Scrape tweets called')
    tc.Output = f'{username}-{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
    tc.Store_csv = True
    print('Username set')
    tc.Username = username
    print('Searching tweets')
    tw.run.Search(tc)
    print('Search complete')

if __name__ == '__main__':
    processes = []

    for i in range(len(NEWSOUTLETS)):
        t = tw.Config()
        p = Process(target=scrape_tweets, args=(t, NEWSOUTLETS[i]))
        p.start()
        processes.append(p)
        
    for p in processes:
        p.join()
# list_files = subprocess.run(['mongoimport.exe', '-dtest', '-ctest', '--drop', '--headerline', '--type=csv', 'data.csv'], shell=True)
# print("The exit code was: %d" % scrape_tweets.returncode)