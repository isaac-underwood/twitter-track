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
    tc.Limit = 50
    tw.run.Search(tc)
    print('Search complete. Adding to database')
    insert_data(tc.Output)


def insert_data(filename):
    list_files = subprocess.run(['mongoimport.exe', '-dtest', '-ctest',
                                '--headerline', '--type=csv', filename],
                                shell=True)


if __name__ == '__main__':
    processes = []
    t = tw.Config()
    scrape_tweets(t, NEWSOUTLETS[0])

    # Create processes for each news outlet and assign them
    # to scrape_tweets function
    # for i in range(len(NEWSOUTLETS)):
    #     t = tw.Config()
    #     p = Process(target=scrape_tweets, args=(t, NEWSOUTLETS[i]))
    #     p.start()  # Start process (scrape_tweets(tc, {username}))
    #     processes.append(p)  # Append process to list of processes

    # for p in processes:
    #     p.join()

    # list_files = subprocess.run(['mongoimport.exe', '-dtest', '-ctest',
    #                             '--headerline', '--type=csv', 'data.csv'],
    #                             shell=True)
    # print("The exit code was: %d" % list_files.returncode)
