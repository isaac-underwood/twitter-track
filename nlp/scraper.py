import subprocess
import os
import glob
from multiprocessing import Process
import logging
import time
from datetime import datetime
import twint as tw

print('Initialising twint config')
#tc.Output = f'tw-{datetime.now().strftime("%Y%m%d-%H%M%S")}-newsoutlets.csv'  # Set filename to include current date/time
NEWSOUTLETS = ['nytimes', 'CNN', 'BBC', 'MSNBC', 'NPR', 'FoxNews', 'WSJ']
DPATH = os.getcwd() + '/data'  # Equates to ./data


# Checks if the directory for a user exists in /data and creates if not
def check_dir_exists(name):
    try:
        os.makedirs(os.path.join(DPATH, name))  # Create directory in ./data
        print(f'> Created directory in /data for {name}')
    except FileExistsError:  # Folder already exists
        pass


# Finds the latest created file and obtains/returns datetime from filename
def get_last_scraped(username):
    # Get all csv files in data/username directory
    list_of_files = glob.iglob(f'{os.path.join(DPATH, username)}/*.csv')
    # Get latest created file
    try:
        latest_scraped = max(list_of_files, key=os.path.getctime)
        filename = latest_scraped.rsplit('\\', 1)[1]  # Split to get filename
        dstring = filename.split('.', 1)[0]  # Split to get rid of .csv

        # Convert strftime to datetime
        last_date_time = datetime.strptime(dstring, '%Y%m%d-%H%M%S')
        return str(last_date_time)
    except ValueError:
        pass


# Searches and extracts tweets for a given user
def scrape_tweets(tc, username):
    check_dir_exists(username)
    current_time = datetime.now()
    tc.Output = os.path.join(DPATH, username,
                             current_time.strftime("%Y%m%d-%H%M%S")) + '.csv'
    tc.Store_csv = True

    # Set Since option to only scrape since last scraped
    last_scraped = get_last_scraped(username)
    # Check if there was a last time, if not don't set a Since
    if last_scraped is not None:
        tc.Since = get_last_scraped(username)

    tc.Username = username
    print(f'> Searching tweets by the user {username}')
    tw.run.Search(tc)
    print(f'> Search under {username} complete. Adding data to database')
    insert_data(tc.Output)


# Adds objects to database using mongoimport from a given CSV file
def insert_data(filename):
    # Run mongoimport tool to import data to database
    list_files = subprocess.run(['mongoimport.exe', '-dtest', '-ctest',
                                '--headerline', '--type=csv', filename],
                                shell=True)


if __name__ == '__main__':
    processes = []
    t = tw.Config()
    # Create processes for each news outlet and assign them
    # to scrape_tweets function
    for i in range(len(NEWSOUTLETS)):
        t = tw.Config()
        p = Process(target=scrape_tweets, args=(t, NEWSOUTLETS[i]))
        p.start()  # Start process (scrape_tweets(tc, {username}))
        processes.append(p)  # Append process to list of processes

    for p in processes:
        p.join()

    # list_files = subprocess.run(['mongoimport.exe', '-dtest', '-ctest',
    #                             '--headerline', '--type=csv', 'data.csv'],
    #                             shell=True)
    # print("The exit code was: %d" % list_files.returncode)
