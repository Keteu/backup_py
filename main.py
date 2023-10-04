'''
WE ASSUME THAT WE DON'T HAVE ANY OTHER FOLDERS INSIDE THE SOURCE -> WE WILL IMPLEMENT
THE ASSIGMENT ONLY ON ONE LEVEL, THUS WE DON'T HAVE SUBDIRECTORIES.
'''


import os
import hashlib
import time
from argparse import ArgumentParser

LOG = r"C:\Users\petru\Documents\test\log.txt"


def log(message):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(LOG, 'a') as f:
        f.write('[' + now + ']' + message + '\n')


'''
Compare two files using the HASH functions
'''
#define the hash function to use it


def hashFile(file):
    BUF_SIZE = 65536 #read the in 64kb chunks
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

#the compare method
def compare2file(file1, file2):
    if hashFile(file1).__eq__(hashFile(file2)):
        return True
    else:
        return False

#print(compare2file(r"C:\Users\petru\Documents\test\replica\auch.txt",r"C:\Users\petru\Documents\test\replica\gol.txt"))

'''
Compare two folders by 
1. check the length of the folders 
2. compare the names of the files
2. compare the files from the source and replica
'''

def compareFolders(source, replica):
    files_source = os.listdir(source)
    files_replica = os.listdir(replica)
    if len(files_source) != len(files_replica):
        return False

    if sorted(files_source) != sorted(files_replica):
        return False

    for file in files_source:
        if file in files_replica:
            if not compare2file(os.path.join(source, file), os.path.join(replica, file)):
                return False
        else:
            return True
    return True

'''
Define the args to be passed 
'''
arg_parser = ArgumentParser()
arg_parser.add_argument('source', help='absolute path of the source folder')
arg_parser.add_argument('replica', help='absolute path of the replica folder')
arg_parser.add_argument('interval', help='synchronization interval in seconds')
arg_parser.add_argument('log', help='absolute path of the log file')
args = arg_parser.parse_args()

source = args.source
replica = args.replica
interval = args.interval
log_file = args.log

log('Start')

while True:
    if compareFolders(source, replica):
        print('file is up to date')
        log('file is up to date')
        #sleep for interval in seconds
        time.sleep(int(interval))
        continue

    countSync = 0
    updateFile = 0
    deleteFile = 0

    source_file = os.listdir(source)
    replica_file = os.listdir(replica)

    for file in replica_file:
        if file in source_file:
            if compare2file(os.path.join(source, file), os.path.join(replica, file)):
                log(f'{file} is up to date')
                countSync += 1
            else:
                #copy the file from the source file to replica file
                updateFile += 1
                os.remove(os.path.join(replica, file))
                os.system('copy '+ os.path.join(source, file) + ' '+ replica)
                log(f'{file} is updated')
        if file not in source_file:
            #delete the file from the backup
            log(f'{file} is deleted')
            deleteFile += 1
            os.remove(os.path.join(replica, file))

    for file in source_file:
        if file not in replica_file:
            #copy file from source to replica
            updateFile += 1
            log(f'{file} is copied')
            os.system('copy '+ os.path.join(source, file) + ' '+ replica)

    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f'[{now}] sync: {countSync}; update: {updateFile}; delete: {deleteFile};')

    # sleep for interval in seconds
    time.sleep(int(interval))